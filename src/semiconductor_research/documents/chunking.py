def fact_chunks(facts: list[dict]) -> list[dict]:
    """Bounded, auditable financial row chunks; never split away period or units."""
    chunks = []
    for fact in facts:
        text = (
            f"NVIDIA {fact['fiscal_label']} annual {fact['metric'].replace('_', ' ')}: "
            f"{fact['value']:,} {fact['currency']} million. Reporting period ended {fact['period_end']}. "
            "US GAAP; unaudited earnings release. Cash outflows are positive magnitudes."
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
