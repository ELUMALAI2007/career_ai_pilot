"""
CareerPilot AI Formatters Module
Helper functions for formatting dates, numbers, currency, and string truncation.
"""

def format_percentage(val: float) -> str:
    """Formats float value as percentage string."""
    return f"{round(val, 1)}%"


def format_currency(val: float, currency_symbol: str = "₹") -> str:
    """Formats salary/package currency values."""
    return f"{currency_symbol}{val:,.2f}"


def truncate_text(text: str, max_chars: int = 100) -> str:
    """Truncates string to specified character limit."""
    if text and len(text) > max_chars:
        return text[:max_chars] + "..."
    return text or ""
