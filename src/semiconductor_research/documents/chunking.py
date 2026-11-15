def fact_chunks(
    facts: list[dict], company="NVIDIA", accounting_basis="US GAAP; unaudited earnings release"
) -> list[dict]:
    """Bounded, auditable financial row chunks; never split away period or units."""
    chunks = []
    for fact in facts:
        text = (
            f"{company} {fact['fiscal_label']} annual {fact['metric'].replace('_', ' ')}: "
            f"{fact['value']:,} {fact['currency']} at original unit scale {fact['unit_scale']}. Reporting period ended {fact['period_end']}. "
            f"{accounting_basis}. Cash outflows are positive magnitudes."
        )
        chunks.append(
            {
                "text": text,
                "locator": fact["locator"],
                "topic": fact["metric"],
                "period_end": fact["period_end"],
            }
        )
    return chunks
