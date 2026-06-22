def compute_confidence_band(
    connected_sources: list[str],
    months_history: int,
) -> str:
    source_count = len(connected_sources)

    if source_count >= 4 and months_history >= 8:
        return "High"
    elif source_count >= 2 and months_history >= 4:
        return "Medium"
    else:
        return "Low"
