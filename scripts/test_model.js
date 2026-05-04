const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const { calculateScenario, extendWithFictionalProjection, interpolateRecords } = require("../assets/model.js");

const ROOT = path.resolve(__dirname, "..");
const APP_PATH = path.join(ROOT, "assets/app.js");
const CASHFLOW_PATH = path.join(ROOT, "data/website/allgemeine-rv-cashflows.json");
const INDEX_PATH = path.join(ROOT, "index.html");

function approx(actual, expected, tolerance = 1e-6) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    `Expected ${actual} to be within ${tolerance} of ${expected}`
  );
}

function testInterpolation() {
  assert.deepEqual(interpolateRecords([]), []);

  const records = [
    { year: 1960, scope: "Alte Bundesländer", contributionsMioEur: 6894, pensionOutlaysMioEur: 7286 },
    { year: 1965, scope: "Alte Bundesländer", contributionsMioEur: 11502, pensionOutlaysMioEur: 11525 }
  ];
  const interpolated = interpolateRecords(records);

  assert.equal(interpolated.length, 6);
  assert.equal(interpolated[0].year, 1960);
  assert.equal(interpolated[0].interpolated, false);
  assert.equal(interpolated[1].year, 1961);
  assert.equal(interpolated[1].scope, "Alte Bundesländer / rekonstruiert");
  assert.equal(interpolated[1].interpolated, true);
  approx(interpolated[1].contributionsMioEur, 7815.6);
  approx(interpolated[1].pensionOutlaysMioEur, 8133.8);
  assert.equal(interpolated.at(-1).year, 1965);
  assert.equal(interpolated.at(-1).interpolated, false);
}

function testHandCalculatedScenario() {
  const rows = calculateScenario([
    { year: 2000, scope: "Test", contributionsMioEur: 1000, pensionOutlaysMioEur: 2000 },
    { year: 2001, scope: "Test", contributionsMioEur: 1200, pensionOutlaysMioEur: 1800 }
  ], {
    contributionIncrease: 5,
    pensionReduction: 5,
    returnRate: 4,
    costRate: 1
  });

  approx(rows[0].extraContributionsMioEur, 50);
  approx(rows[0].pensionSavingsMioEur, 100);
  approx(rows[0].fundDepositMioEur, 150);
  approx(rows[0].annualReturnMioEur, 0);
  approx(rows[0].fundMioEur, 150);
  approx(rows[0].cumulativeBuildCostMioEur, 150);
  approx(rows[0].investmentGainMioEur, 0);

  approx(rows[1].extraContributionsMioEur, 60);
  approx(rows[1].pensionSavingsMioEur, 90);
  approx(rows[1].fundDepositMioEur, 150);
  approx(rows[1].annualReturnMioEur, 4.5);
  approx(rows[1].fundMioEur, 304.5);
  approx(rows[1].cumulativeBuildCostMioEur, 300);
  approx(rows[1].investmentGainMioEur, 4.5);
  approx(rows[1].returnCoverage, 4.5 / 1800);
}

function testNegativeReturnFloor() {
  const rows = calculateScenario([
    { year: 2000, scope: "Test", contributionsMioEur: 1000, pensionOutlaysMioEur: 0 },
    { year: 2001, scope: "Test", contributionsMioEur: 0, pensionOutlaysMioEur: 0 }
  ], {
    contributionIncrease: 10,
    pensionReduction: 0,
    returnRate: -500,
    costRate: 0
  });

  approx(rows[0].fundMioEur, 100);
  approx(rows[1].annualReturnMioEur, -99);
  approx(rows[1].fundMioEur, 1);
}

function testFictionalProjection() {
  assert.deepEqual(extendWithFictionalProjection([]), []);

  const records = [
    { year: 2020, scope: "Test", contributionsMioEur: 100, pensionOutlaysMioEur: 200 },
    { year: 2022, scope: "Test", contributionsMioEur: 121, pensionOutlaysMioEur: 242 }
  ];
  const extended = extendWithFictionalProjection(records, { trendStartYear: 2020, endYear: 2024 });

  assert.equal(extended.length, 4);
  assert.equal(extended[0].projected, undefined);
  assert.equal(extended[2].year, 2023);
  assert.equal(extended[2].scope, "Fiktive Fortschreibung");
  assert.equal(extended[2].projected, true);
  assert.equal(extended[2].dataStatus, "model_assumption");
  approx(extended[2].contributionGrowthRate, 0.1);
  approx(extended[2].pensionOutlayGrowthRate, 0.1);
  approx(extended[2].contributionsMioEur, 133.1);
  approx(extended[2].pensionOutlaysMioEur, 266.2);
  approx(extended[3].contributionsMioEur, 146.41);
  approx(extended[3].pensionOutlaysMioEur, 292.82);
}

function testDefaultHeadlineRegression() {
  const dataset = JSON.parse(fs.readFileSync(CASHFLOW_PATH, "utf8"));
  const annualData = interpolateRecords(dataset.records);
  const rows = calculateScenario(annualData, {
    contributionIncrease: 5,
    pensionReduction: 5,
    returnRate: 4,
    costRate: 0.35
  });
  const last = rows.at(-1);

  assert.equal(rows.length, 65);
  assert.equal(rows[0].year, 1960);
  assert.equal(last.year, 2024);
  approx(rows[0].fundDepositMioEur, 709);
  approx(rows[1].annualReturnMioEur, 25.8785);
  approx(last.fundDepositMioEur, 32484.35, 0.01);
  approx(last.fundMioEur, 1820370.984191236, 0.01);
  approx(last.cumulativeBuildCostMioEur, 807352.025, 0.01);
  approx(last.investmentGainMioEur, 1013018.9591912361, 0.01);
  approx(last.returnCoverage, 0.1828362003042807, 1e-9);
}

function testProjectionHeadlineRegression() {
  const dataset = JSON.parse(fs.readFileSync(CASHFLOW_PATH, "utf8"));
  const annualData = interpolateRecords(dataset.records);
  const projectedData = extendWithFictionalProjection(annualData);
  const rows = calculateScenario(projectedData, {
    contributionIncrease: 5,
    pensionReduction: 5,
    returnRate: 4,
    costRate: 0.35
  });
  const firstProjected = rows.find((row) => row.projected);
  const last = rows.at(-1);

  assert.equal(rows.length, 81);
  assert.equal(firstProjected.year, 2025);
  assert.equal(last.year, 2040);
  assert.equal(last.projected, true);
  approx(firstProjected.contributionsMioEur, 318382.8056877517, 0.01);
  approx(firstProjected.pensionOutlaysMioEur, 359201.6498165075, 0.01);
  approx(last.fundMioEur, 4203117.833129523, 0.01);
  approx(last.cumulativeBuildCostMioEur, 1564402.0979806855, 0.01);
  approx(last.investmentGainMioEur, 2638715.735148838, 0.01);
}

function testBrowserScriptOrder() {
  const html = fs.readFileSync(INDEX_PATH, "utf8");
  const modelIndex = html.indexOf('src="assets/model.js"');
  const appIndex = html.indexOf('src="assets/app.js"');

  assert.ok(modelIndex > -1, "index.html must load assets/model.js");
  assert.ok(appIndex > -1, "index.html must load assets/app.js");
  assert.ok(modelIndex < appIndex, "assets/model.js must load before assets/app.js");
}

function testProjectionToggleMarkup() {
  const html = fs.readFileSync(INDEX_PATH, "utf8");
  const checkbox = html.match(/<input id="fictionalProjection"[^>]*>/);

  assert.ok(checkbox, "index.html must include the fictional projection checkbox");
  assert.equal(/\bchecked\b/.test(checkbox[0]), false, "projection checkbox must be off by default");
  assert.ok(html.includes("Fiktive Fortschreibung bis 2040 einrechnen"));
  assert.ok(html.includes("<title id=\"chartTitle\">"));
  assert.ok(html.includes("<desc id=\"chartDesc\">"));
}

function testChartAccessibilityRenderInvariant() {
  const app = fs.readFileSync(APP_PATH, "utf8");

  assert.ok(app.includes('make("title", { id: "chartTitle" })'), "renderChart must recreate the SVG title after replaceChildren");
  assert.ok(app.includes('make("desc", { id: "chartDesc" })'), "renderChart must recreate the SVG description after replaceChildren");
}

testInterpolation();
testHandCalculatedScenario();
testNegativeReturnFloor();
testFictionalProjection();
testDefaultHeadlineRegression();
testProjectionHeadlineRegression();
testBrowserScriptOrder();
testProjectionToggleMarkup();
testChartAccessibilityRenderInvariant();

console.log("model tests ok");
