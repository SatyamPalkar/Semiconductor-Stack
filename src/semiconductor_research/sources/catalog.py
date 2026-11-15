from datetime import UTC, date, datetime

NVIDIA = {
    "key": "nvda-fy2025",
    "company": "NVDA",
    "title": "NVIDIA fourth-quarter and fiscal 2025 financial results",
    "publisher": "NVIDIA Newsroom",
    "url": "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2025",
    # Date-only publication: end of the publisher's day avoids intraday look-ahead.
    "published_at": datetime(2025, 2, 27, 7, 59, 59, tzinfo=UTC),
    "publication_date": "2025-02-26",
    "document_type": "earnings_release",
    "accounting_basis": "US GAAP; unaudited earnings release",
    "periods": [
        {"start": None, "end": date(2025, 1, 26), "label": "FY2025"},
        {"start": None, "end": date(2024, 1, 28), "label": "FY2024"},
    ],
}

COMPANIES = [
    {
        "ticker": "NVDA",
        "name": "NVIDIA",
        "role": "Fabless design & computing platforms",
        "layer": "Design",
        "coverage": "financial_pilot",
        "url": "https://investor.nvidia.com/",
    },
    {
        "ticker": "TSM",
        "name": "TSMC",
        "role": "Semiconductor foundry",
        "layer": "Fabrication",
        "coverage": "source_access_pending",
        "url": "https://investor.tsmc.com/",
    },
    {
        "ticker": "ASML",
        "name": "ASML",
        "role": "Lithography equipment",
        "layer": "Equipment",
        "coverage": "planned",
        "url": "https://www.asml.com/en/investors",
    },
    {
        "ticker": "MU",
        "name": "Micron",
        "role": "Memory products",
        "layer": "Memory",
        "coverage": "planned",
        "url": "https://investors.micron.com/",
    },
    {
        "ticker": "TXN",
        "name": "Texas Instruments",
        "role": "Analog & embedded processing",
        "layer": "Integrated manufacturing",
        "coverage": "planned",
        "url": "https://investor.ti.com/",
    },
    {
        "ticker": "AMKR",
        "name": "Amkor",
        "role": "Assembly, packaging & test",
        "layer": "Packaging",
        "coverage": "planned",
        "url": "https://ir.amkor.com/",
    },
]
