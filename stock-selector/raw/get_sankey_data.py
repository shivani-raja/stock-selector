import pandas as pd
from raw.format_number import format_number
from raw.currency_symbols import get_currency_symbol

color_dict = {"green": "#4BDB95", "red": "#FF3B4C"}


def get_sankey_data(df):
    """prepares data for sankey diagram

    :return: sankey_data, which feeds into the sankey diagram
    """

    # get currency symbol
    currency = df["reportedCurrency"].values[0]
    currency_symbol = get_currency_symbol(currency)

    sankey_nodes = pd.DataFrame()
    sankey_links = pd.DataFrame()

    for year in df["calendarYear"]:
        mask = df[df["calendarYear"] == year].squeeze()

        # data for nodes
        node_data = pd.DataFrame()
        node_data["x"] = [0, 0.3, 0.3, 0.5, 0.5, 0.7, 1, 1]
        node_data["y"] = [0.6, 0.4, 0.9, 0.3, 0.6, 0.2, 0.1, 0.35]
        node_data["label"] = [
            f"Total<br>Revenue<br>{currency_symbol}{format_number(mask.revenue)}",
            f"Gross Profit<br>{currency_symbol}{format_number(mask.grossProfit)}",
            f"Cost of<br>Sales<br>{currency_symbol}{format_number(mask.costOfRevenue)}",
            f"Operating<br>Income<br>{currency_symbol}{format_number(mask.operatingIncome)}",
            f"Operating<br>Expenses<br>{currency_symbol}{format_number(mask.operatingExpenses)}",
            f"Pre-tax<br>Income<br>{currency_symbol}{format_number(mask.incomeBeforeTax)}",
            f"Net<br>Income<br>{currency_symbol}{format_number(mask.netIncome)}",
            f"Tax<br>{currency_symbol}{format_number(mask.incomeTaxExpense)}"
        ]
        node_data["color"] = [
            "#FF72D9",
            "#4BDB95",
            "#FF3B4C",
            "#4BDB95",
            "#FF3B4C",
            "#4BDB95",
            "#4BDB95",
            "#FF3B4C",
        ]
        node_data["year"] = year

        # data for linkers
        link_data = pd.DataFrame()
        link_data["source"] = [0, 0, 1, 1, 3, 5, 5]
        link_data["target"] = [1, 2, 3, 4, 5, 6, 7]
        link_data["value"] = [
            mask["grossProfit"],
            mask["costOfRevenue"],
            mask["operatingIncome"],
            mask["operatingExpenses"],
            mask["incomeBeforeTax"],
            mask["netIncome"],
            mask["incomeTaxExpense"],
        ]
        link_data["year"] = year
        link_data["color"] = [
            "rgba(75, 219, 149, 0.5)",
            "rgba(255, 59, 76, 0.5)",
            "rgba(75, 219, 149, 0.5)",
            "rgba(255, 59, 76, 0.5)",
            "rgba(75, 219, 149, 0.5)",
            "rgba(75, 219, 149, 0.5)",
            "rgba(255, 59, 76, 0.5)",
        ]

        sankey_nodes = pd.concat([sankey_nodes, node_data], axis=0)
        sankey_links = pd.concat([sankey_links, link_data], axis=0)

    return sankey_nodes, sankey_links
