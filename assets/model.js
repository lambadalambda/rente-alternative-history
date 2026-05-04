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

  return {
    calculateScenario,
    interpolateRecords
  };
});
