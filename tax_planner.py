"""Legal tax planning helper.

This module estimates U.S.-style federal taxable income and highlights
compliant strategies that can reduce tax liability.

It is intentionally designed for tax *planning* and does not support or
encourage tax evasion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


STANDARD_DEDUCTION = {
    "single": 14600,
    "married_filing_jointly": 29200,
    "head_of_household": 21900,
}

# Simplified progressive brackets for example planning only
BRACKETS = {
    "single": [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (609350, 0.35),
        (float("inf"), 0.37),
    ],
    "married_filing_jointly": [
        (23200, 0.10),
        (94300, 0.12),
        (201050, 0.22),
        (383900, 0.24),
        (487450, 0.32),
        (731200, 0.35),
        (float("inf"), 0.37),
    ],
    "head_of_household": [
        (16550, 0.10),
        (63100, 0.12),
        (100500, 0.22),
        (191950, 0.24),
        (243700, 0.32),
        (609350, 0.35),
        (float("inf"), 0.37),
    ],
}


@dataclass
class TaxProfile:
    filing_status: str
    gross_income: float
    itemized_deductions: float = 0.0
    pre_tax_401k: float = 0.0
    hsa_contribution: float = 0.0
    ira_contribution: float = 0.0
    child_tax_credit: float = 0.0
    education_credit: float = 0.0


@dataclass
class TaxPlanResult:
    taxable_income: float
    estimated_tax_before_credits: float
    estimated_tax_after_credits: float
    legal_suggestions: List[str]


def _progressive_tax(income: float, filing_status: str) -> float:
    brackets = BRACKETS[filing_status]
    tax = 0.0
    lower_bound = 0.0

    for upper_bound, rate in brackets:
        if income <= lower_bound:
            break
        taxed_amount = min(income, upper_bound) - lower_bound
        tax += taxed_amount * rate
        lower_bound = upper_bound

    return max(tax, 0.0)


def estimate_tax(profile: TaxProfile) -> TaxPlanResult:
    if profile.filing_status not in STANDARD_DEDUCTION:
        raise ValueError(f"Unsupported filing status: {profile.filing_status}")

    deduction_used = max(
        STANDARD_DEDUCTION[profile.filing_status],
        profile.itemized_deductions,
    )

    above_the_line = profile.pre_tax_401k + profile.hsa_contribution + profile.ira_contribution
    taxable_income = max(profile.gross_income - above_the_line - deduction_used, 0.0)

    tax_before_credits = _progressive_tax(taxable_income, profile.filing_status)
    total_credits = max(profile.child_tax_credit + profile.education_credit, 0.0)
    tax_after_credits = max(tax_before_credits - total_credits, 0.0)

    suggestions: List[str] = []
    if profile.pre_tax_401k < 23000:
        suggestions.append("Increase traditional 401(k) contributions (up to annual IRS limit).")
    if profile.hsa_contribution < 4150:
        suggestions.append("If eligible, contribute more to an HSA for triple tax advantages.")
    if profile.itemized_deductions < STANDARD_DEDUCTION[profile.filing_status]:
        suggestions.append("Track deductible expenses; bunching deductions across years may help.")
    suggestions.append("Use only legal deductions/credits and keep documentation for all claims.")

    return TaxPlanResult(
        taxable_income=taxable_income,
        estimated_tax_before_credits=tax_before_credits,
        estimated_tax_after_credits=tax_after_credits,
        legal_suggestions=suggestions,
    )


if __name__ == "__main__":
    # Example usage
    profile = TaxProfile(
        filing_status="single",
        gross_income=95000,
        itemized_deductions=8000,
        pre_tax_401k=10000,
        hsa_contribution=2000,
        ira_contribution=3000,
        child_tax_credit=0,
        education_credit=1000,
    )

    result = estimate_tax(profile)
    print("Taxable income:", round(result.taxable_income, 2))
    print("Estimated tax (before credits):", round(result.estimated_tax_before_credits, 2))
    print("Estimated tax (after credits):", round(result.estimated_tax_after_credits, 2))
    print("Legal planning suggestions:")
    for tip in result.legal_suggestions:
        print(f"- {tip}")
