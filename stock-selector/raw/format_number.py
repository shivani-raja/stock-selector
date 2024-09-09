# function to format large numbers for graph labels
def format_number(n):
    """formats large numbers to read nicely

    :return: formatted number
    """

    if abs(n) >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"  # billions
    elif abs(n) >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"  # millions
    elif abs(n) >= 1_000:
        return f"{n / 1_000:.1f}K"  # thousands
    else:
        return str(n)  # smaller numbers
