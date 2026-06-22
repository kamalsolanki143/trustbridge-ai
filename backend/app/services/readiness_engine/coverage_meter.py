TOTAL_DATA_SOURCES = 5
ALL_SOURCE_TYPES = {"gst", "aa", "upi", "invoice", "business"}


def compute_coverage(connected_sources: list[str]) -> dict:
    connected_set = set(connected_sources)
    connected = len(connected_set & ALL_SOURCE_TYPES)
    percentage = round((connected / TOTAL_DATA_SOURCES) * 100)
    return {
        "connected": connected,
        "total": TOTAL_DATA_SOURCES,
        "percentage": percentage,
    }
