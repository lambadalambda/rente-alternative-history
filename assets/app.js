const DATA_URL = "data/website/allgemeine-rv-cashflows.json";

const presets = {
  mixed: { label: "Gemischtes Portfolio", returnRate: 4.0, costRate: 0.35 },
  world: { label: "Weltaktien-Vergleich", returnRate: 5.5, costRate: 0.3 },
  sp500: { label: "S&P-500-Vergleich", returnRate: 6.5, costRate: 0.35 },
  dax: { label: "DAX-Vergleich", returnRate: 5.8, costRate: 0.35 },
  stress: { label: "Stressszenario", returnRate: 2.0, costRate: 0.5 }
};

const controls = {
  preset: document.querySelector("#preset"),
  contributionIncrease: document.querySelector("#contributionIncrease"),
  pensionReduction: document.querySelector("#pensionReduction"),
  returnRate: document.querySelector("#returnRate"),
  costRate: document.querySelector("#costRate")
};

const output = {
  contributionIncreaseValue: document.querySelector("#contributionIncreaseValue"),
  pensionReductionValue: document.querySelector("#pensionReductionValue"),
  returnRateValue: document.querySelector("#returnRateValue"),
  costRateValue: document.querySelector("#costRateValue"),
  contributionReadout: document.querySelector("#contributionReadout"),
  pensionReadout: document.querySelector("#pensionReadout"),
  dataStatus: document.querySelector("#dataStatus"),
  fundKpi: document.querySelector("#fundKpi"),
  buildCostKpi: document.querySelector("#buildCostKpi"),
  netKpi: document.querySelector("#netKpi"),
  coverageKpi: document.querySelector("#coverageKpi"),
  chart: document.querySelector("#fundChart"),
  chartSummary: document.querySelector("#chartSummary"),
  dataTableBody: document.querySelector("#dataTableBody")
};

const numberFormat = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 1 });
const percentFormat = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 1, minimumFractionDigits: 1 });

let annualData = [];
let rawDataset = null;

function asPercent(value) {
  return `${percentFormat.format(value)} %`;
}

function formatMioAsMoney(valueMio) {
  const abs = Math.abs(valueMio);
  const sign = valueMio < 0 ? "-" : "";
  if (abs >= 1_000_000) {
    return `${sign}${numberFormat.format(abs / 1_000_000)} Bio. EUR`;
  }
  return `${sign}${numberFormat.format(abs / 1_000)} Mrd. EUR`;
}

function formatTableMoney(valueMio) {
  return `${numberFormat.format(valueMio / 1_000)} Mrd.`;
}

function interpolateRecords(records) {
  const sorted = [...records].sort((a, b) => a.year - b.year);
  const years = [];
  for (let i = 0; i < sorted.length - 1; i += 1) {
    const current = sorted[i];
    const next = sorted[i + 1];
    years.push({ ...current, interpolated: false });
    const gap = next.year - current.year;
    for (let step = 1; step < gap; step += 1) {
      const ratio = step / gap;
      years.push({
        year: current.year + step,
        scope: `${current.scope} / rekonstruiert`,
        contributionsMioEur: current.contributionsMioEur + (next.contributionsMioEur - current.contributionsMioEur) * ratio,
        pensionOutlaysMioEur: current.pensionOutlaysMioEur + (next.pensionOutlaysMioEur - current.pensionOutlaysMioEur) * ratio,
        interpolated: true
      });
    }
  }
  years.push({ ...sorted.at(-1), interpolated: false });
  return years;
}

function getScenario() {
  return {
    contributionIncrease: Number(controls.contributionIncrease.value),
    pensionReduction: Number(controls.pensionReduction.value),
    returnRate: Number(controls.returnRate.value),
    costRate: Number(controls.costRate.value),
    preset: presets[controls.preset.value] ?? presets.mixed
  };
}

function calculateScenario(data, scenario) {
  let fund = 0;
  let cumulativeBuildCost = 0;

  return data.map((row) => {
    const netReturnRate = Math.max((scenario.returnRate - scenario.costRate) / 100, -0.99);
    const annualReturn = fund * netReturnRate;
    const extraContributions = row.contributionsMioEur * (scenario.contributionIncrease / 100);
    const pensionSavings = row.pensionOutlaysMioEur * (scenario.pensionReduction / 100);
    const deposit = extraContributions + pensionSavings;

    fund = fund + annualReturn + deposit;
    cumulativeBuildCost += deposit;

    return {
      ...row,
      fundDepositMioEur: deposit,
      extraContributionsMioEur: extraContributions,
      pensionSavingsMioEur: pensionSavings,
      annualReturnMioEur: annualReturn,
      fundMioEur: fund,
      cumulativeBuildCostMioEur: cumulativeBuildCost,
      investmentGainMioEur: fund - cumulativeBuildCost,
      returnCoverage: row.pensionOutlaysMioEur > 0 ? annualReturn / row.pensionOutlaysMioEur : 0
    };
  });
}

function updateControlLabels(scenario) {
  output.contributionIncreaseValue.textContent = asPercent(scenario.contributionIncrease);
  output.pensionReductionValue.textContent = asPercent(scenario.pensionReduction);
  output.returnRateValue.textContent = asPercent(scenario.returnRate);
  output.costRateValue.textContent = asPercent(scenario.costRate);
  output.contributionReadout.textContent = `+${asPercent(scenario.contributionIncrease)}`;
  output.pensionReadout.textContent = `-${asPercent(scenario.pensionReduction)}`;
}

function linePath(points, xScale, yScale, key) {
  return points.map((point, index) => {
    const command = index === 0 ? "M" : "L";
    return `${command} ${xScale(point.year).toFixed(2)} ${yScale(point[key]).toFixed(2)}`;
  }).join(" ");
}

function renderChart(rows) {
  const chart = output.chart;
  chart.replaceChildren();

  const width = 1000;
  const height = 420;
  const padding = { top: 40, right: 34, bottom: 56, left: 62 };
  const years = rows.map((row) => row.year);
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);
  const values = rows.flatMap((row) => [row.fundMioEur, row.cumulativeBuildCostMioEur, row.investmentGainMioEur]);
  const minValue = Math.min(0, ...values);
  const maxValue = Math.max(...values);
  const span = maxValue - minValue || 1;
  const xScale = (year) => padding.left + ((year - minYear) / (maxYear - minYear || 1)) * (width - padding.left - padding.right);
  const yScale = (value) => padding.top + ((maxValue - value) / span) * (height - padding.top - padding.bottom);
  const make = (name, attrs = {}) => {
    const node = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    return node;
  };

  const zero = make("line", {
    x1: padding.left,
    x2: width - padding.right,
    y1: yScale(0),
    y2: yScale(0),
    stroke: "rgba(21,18,15,.28)",
    "stroke-width": "2"
  });
  chart.append(zero);

  const fundPath = make("path", { d: linePath(rows, xScale, yScale, "fundMioEur"), class: "line-fund" });
  const costPath = make("path", { d: linePath(rows, xScale, yScale, "cumulativeBuildCostMioEur"), class: "line-cost" });
  const gainPath = make("path", { d: linePath(rows, xScale, yScale, "investmentGainMioEur"), class: "line-net" });
  chart.append(fundPath, costPath, gainPath);

  const legend = make("g", { class: "legend", transform: "translate(68 28)" });
  const items = [
    ["Fonds", "var(--accent)", false],
    ["Aufbaupreis", "var(--accent-2)", true],
    ["Kapitalertrag", "var(--accent-3)", false]
  ];
  items.forEach(([label, color, dashed], index) => {
    const x = index * 260;
    legend.append(make("line", {
      x1: x,
      x2: x + 44,
      y1: 0,
      y2: 0,
      stroke: color,
      "stroke-width": index === 2 ? 4 : 6,
      "stroke-dasharray": dashed ? "10 8" : "none",
      "stroke-linecap": "round"
    }));
    const text = make("text", { x: x + 56, y: 8 });
    text.textContent = label;
    legend.append(text);
  });
  chart.append(legend);

  const startLabel = make("text", { class: "axis-label", x: padding.left, y: height - 18 });
  startLabel.textContent = String(minYear);
  const endLabel = make("text", { class: "axis-label", x: width - padding.right - 58, y: height - 18 });
  endLabel.textContent = String(maxYear);
  const valueLabel = make("text", { class: "axis-label", x: padding.left, y: padding.top - 16 });
  valueLabel.textContent = formatMioAsMoney(maxValue);
  chart.append(startLabel, endLabel, valueLabel);
}

function renderTable(rows) {
  const selectedYears = [1960, 1970, 1990, 2000, 2010, 2024];
  const rowsByYear = new Map(rows.map((row) => [row.year, row]));
  output.dataTableBody.replaceChildren();

  selectedYears.forEach((year) => {
    const row = rowsByYear.get(year);
    if (!row) return;
    const tr = document.createElement("tr");
    const cells = [
      String(row.year),
      formatTableMoney(row.contributionsMioEur),
      formatTableMoney(row.pensionOutlaysMioEur),
      formatTableMoney(row.extraContributionsMioEur),
      formatTableMoney(row.pensionSavingsMioEur),
      formatTableMoney(row.fundDepositMioEur),
      row.interpolated ? "interpoliert" : row.scope
    ];
    cells.forEach((text) => {
      const td = document.createElement("td");
      td.textContent = text;
      tr.append(td);
    });
    output.dataTableBody.append(tr);
  });
}

function render() {
  if (!annualData.length) return;
  const scenario = getScenario();
  updateControlLabels(scenario);
  const rows = calculateScenario(annualData, scenario);
  const last = rows.at(-1);

  output.fundKpi.textContent = formatMioAsMoney(last.fundMioEur);
  output.buildCostKpi.textContent = formatMioAsMoney(last.cumulativeBuildCostMioEur);
  output.netKpi.textContent = formatMioAsMoney(last.investmentGainMioEur);
  output.coverageKpi.textContent = asPercent(last.returnCoverage * 100);

  output.dataStatus.textContent = `Aktives Szenario: ${scenario.preset.label}, Datenreihe ab ${rows[0].year}, +${asPercent(scenario.contributionIncrease)} Beiträge, -${asPercent(scenario.pensionReduction)} Rentenausgaben, ${asPercent(scenario.returnRate - scenario.costRate)} nominale Nettorendite p.a.`;
  output.chartSummary.textContent = `Im Jahr ${last.year} steht ein Fonds von ${formatMioAsMoney(last.fundMioEur)} einem kumulierten Aufbaupreis von ${formatMioAsMoney(last.cumulativeBuildCostMioEur)} gegenüber. Daraus ergeben sich ${formatMioAsMoney(last.investmentGainMioEur)} Kapitalertrag über den eingezahlten Verzicht hinaus. Die Modellrendite des Jahres deckt ${asPercent(last.returnCoverage * 100)} der Rentenausgaben dieses Jahres.`;

  renderChart(rows);
  renderTable(rows);
}

function bindControls() {
  controls.preset.addEventListener("change", () => {
    const preset = presets[controls.preset.value] ?? presets.mixed;
    controls.returnRate.value = String(preset.returnRate);
    controls.costRate.value = String(preset.costRate);
    render();
  });

  Object.values(controls).forEach((control) => {
    control.addEventListener("input", render);
  });
}

async function init() {
  bindControls();
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    rawDataset = await response.json();
    annualData = interpolateRecords(rawDataset.records);
    render();
  } catch (error) {
    output.dataStatus.textContent = "Modelldaten konnten nicht geladen werden. Bitte die Website über einen lokalen Server öffnen.";
    output.chartSummary.textContent = `Fehler beim Laden von ${DATA_URL}: ${error.message}`;
  }
}

init();
