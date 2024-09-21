def get_currency_symbol(currency):

    # define a currency symbols dictionary
    currency_symbols = {
        "USD": "$",  # US Dollar
        "GBP": "£",  # British Pound
        "EUR": "€",  # Euro
        "JPY": "¥",  # Japanese Yen
        "AUD": "A$",  # Australian Dollar
        "CAD": "C$",  # Canadian Dollar
        "CHF": "CHF",  # Swiss Franc
        "CNY": "¥",  # Chinese Yuan
        "INR": "₹",  # Indian Rupee
        "RUB": "₽",  # Russian Ruble
        "BRL": "R$",  # Brazilian Real
        "ZAR": "R",  # South African Rand
        "SGD": "S$",  # Singapore Dollar
        "HKD": "HK$",  # Hong Kong Dollar
        "NZD": "NZ$",  # New Zealand Dollar
        "KRW": "₩",  # South Korean Won
        "MXN": "Mex$",  # Mexican Peso
        "SEK": "kr",  # Swedish Krona
        "NOK": "kr",  # Norwegian Krone
        "DKK": "kr",  # Danish Krone

    }

    return currency_symbols.get(currency)
