(function exposeModel(root, factory) {
  const model = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = model;
  }
  root.RentenModel = model;
})(typeof globalThis !== "undefined" ? globalThis : this, function createModel() {
  function interpolateRecords(records) {
    if (!records.length) return [];

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

  function compoundAnnualGrowthRate(startValue, endValue, years) {
    if (years <= 0 || startValue <= 0 || endValue <= 0) return 0;
    return (endValue / startValue) ** (1 / years) - 1;
  }

  function extendWithFictionalProjection(records, options = {}) {
    if (!records.length) return [];

    const endYear = options.endYear ?? 2040;
    const trendStartYear = options.trendStartYear ?? 2014;
    const sorted = [...records].sort((a, b) => a.year - b.year).map((row) => ({ ...row }));
    const last = sorted.at(-1);
    if (last.year >= endYear) return sorted;

    const trendStart = sorted.find((row) => row.year === trendStartYear) ?? sorted[0];
    const trendYears = Math.max(last.year - trendStart.year, 1);
    const contributionGrowthRate = compoundAnnualGrowthRate(
      trendStart.contributionsMioEur,
      last.contributionsMioEur,
      trendYears
    );
    const pensionOutlayGrowthRate = compoundAnnualGrowthRate(
      trendStart.pensionOutlaysMioEur,
      last.pensionOutlaysMioEur,
      trendYears
    );
    const projectionBasis = `fiktive Fortschreibung mit nominalem ${trendStart.year}-${last.year}-Trend`;

    for (let year = last.year + 1; year <= endYear; year += 1) {
      const step = year - last.year;
      sorted.push({
        year,
        scope: "Fiktive Fortschreibung",
        contributionsMioEur: last.contributionsMioEur * (1 + contributionGrowthRate) ** step,
        pensionOutlaysMioEur: last.pensionOutlaysMioEur * (1 + pensionOutlayGrowthRate) ** step,
        interpolated: false,
        projected: true,
        projectionBasis,
        contributionGrowthRate,
        pensionOutlayGrowthRate,
        dataStatus: "model_assumption"
      });
    }

    return sorted;
  }

  return {
    calculateScenario,
    extendWithFictionalProjection,
    interpolateRecords
  };
});
