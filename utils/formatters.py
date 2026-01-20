def format_indian_currency(price):
    # Safety check
    if price is None:
        return ""

    # Convert to string (handles int input)
    price_str = str(price)

    # If number length is 3 or less, no formatting needed
    if len(price_str) <= 3:
        return price_str

    # Last 3 digits
    last_three = price_str[-3:]

    # Remaining digits before last 3
    remaining = price_str[:-3]

    # Split remaining digits into groups of 2
    groups = []
    while len(remaining) > 2:
        groups.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        groups.insert(0, remaining)

    # Join everything with commas
    return ",".join(groups) + "," + last_three
