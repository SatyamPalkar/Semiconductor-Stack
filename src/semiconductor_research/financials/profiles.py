"""Reviewed native-unit definitions; these are not harmonized industry metrics."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialProfile:
    name: str
    aliases: tuple[str, ...]
    currency: str
    scale: int
    prefix: str
    capital: tuple[str, ...]
    offsets: tuple[str, ...]
    fcf_extra: tuple[str, ...]
    capital_definition: str
    cash_definition: str
    cash_label: str = "free cash flow"


PROFILES = {
    "NVDA": FinancialProfile(
        "NVIDIA",
        ("nvidia", "nvda"),
        "USD",
        1_000_000,
        "FY",
        ("capital_purchases",),
        (),
        ("capital_principal",),
        "Purchases of property, equipment and intangible assets; excludes capital principal payments from this spending ratio.",
        "Operating cash flow less purchases AND principal payments related to property, equipment and intangible assets. NVIDIA release definition; non-GAAP measure.",
    ),
    "TSM": FinancialProfile(
        "TSMC",
        ("tsmc", "tsm"),
        "TWD",
        1000,
        "CY",
        ("capital_expenditures",),
        (),
        (),
        "Annual-report capital expenditures. TSMC disclosed scope; not NVIDIA’s PPE-and-intangibles definition.",
        "Analytical cash remaining: operating cash flow minus annual-report capital expenditures. Not a harmonized FCF measure; does not subtract other investing or financing flows.",
        "analytical cash remaining",
    ),
    "ASML": FinancialProfile(
        "ASML",
        ("asml",),
        "EUR",
        1_000_000,
        "CY",
        ("capital_purchases",),
        (),
        (),
        "Purchases of property, plant and equipment AND intangible assets, as disclosed in ASML’s annual report.",
        "Operating cash flow minus purchases of property, plant and equipment and intangible assets. ASML annual-report free cash flow definition; non-GAAP measure.",
    ),
    "MU": FinancialProfile(
        "Micron",
        ("micron", "mu"),
        "USD",
        1_000_000,
        "FY",
        ("capital_purchases", "capital_principal"),
        ("capital_asset_sales", "capital_grants"),
        (),
        "Net capital investment: PPE expenditures plus equipment purchase-contract payments, less PPE sale proceeds and government incentives. Micron reconciliation; not gross PPE spending.",
        "Operating cash flow minus net capital investment (PPE expenditures plus equipment purchase-contract payments, less PPE sale proceeds and government incentives). Micron adjusted free cash flow definition; non-GAAP measure.",
        "adjusted free cash flow",
    ),
    "TXN": FinancialProfile(
        "Texas Instruments",
        ("texas instruments", "txn"),
        "USD",
        1_000_000,
        "CY",
        ("capital_purchases",),
        (),
        (),
        "Capital expenditures as disclosed in TI’s cash-flow statement; not a harmonized cross-company scope.",
        "Operating cash flow minus capital expenditures. Texas Instruments release definition; non-GAAP measure.",
    ),
    "AMKR": FinancialProfile(
        "Amkor",
        ("amkor", "amkr"),
        "USD",
        1000,
        "CY",
        ("capital_purchases",),
        (),
        (),
        "Gross payments for property, plant and equipment; no offset for sale, insurance or grant proceeds.",
        "Analytical gross-PPE cash residual: operating cash flow minus gross PPE payments. Excludes sale, insurance and grant proceeds and finance-lease payments. This is NOT Amkor’s reported free cash flow reconciliation.",
        "analytical gross-PPE cash residual",
    ),
}
