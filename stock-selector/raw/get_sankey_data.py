import pandas as pd


def get_sankey_data(df):
    """prepares data for sankey diagram

    :return: sankey_data, which feeds into the sankey diagram
    """

    sankey_data = pd.DataFrame()

    for year in df["calendarYear"]:
        mask = df[df["calendarYear"] == year].squeeze()
        yearly_data = pd.DataFrame()
        yearly_data["source"] = [0, 0, 1, 1, 3, 5, 5]
        yearly_data["target"] = [1, 2, 3, 4, 5, 6, 7]
        yearly_data["value"] = [
            mask["grossProfit"],
            mask["costOfRevenue"],
            mask["operatingIncome"],
            mask["operatingExpenses"],
            mask["incomeBeforeTax"],
            mask["netIncome"],
            mask["incomeTaxExpense"],
        ]
        yearly_data["label"] = [
            "Total Revenue",
            "Gross Profit",
            "Cost of Sales",
            "Operating Income",
            "Operating Expenses",
            "Pre-tax Income",
            "Net Income",
        ]
        yearly_data["x"] = [0.1, 0.1, 0.4, 0.4, 0.7, 0.7, 0.9]
        yearly_data["y"] = [0.2, 0.5, 0.2, 0.5, 0.2, 0.5, 0.2]
        yearly_data["year"] = year

        sankey_data = pd.concat([sankey_data, yearly_data], axis=0)

    return sankey_data