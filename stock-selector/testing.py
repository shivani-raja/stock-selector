from raw.get_cashflow_data import get_cashflow_data
import plotly.graph_objects as go

ticker = "AAPL"


cashflow_data = get_cashflow_data(ticker)

year = 2023

cashflow_data = cashflow_data.loc[cashflow_data.calendarYear == str(year)]
cashflow_data = cashflow_data.squeeze()


cashflow_chart = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Cash at Start", "Operations", "Investing", "Financing", "Cash at End"],
            textposition="outside",
            y=[
                cashflow_data.cashAtBeginningOfPeriod,
                cashflow_data.netCashProvidedByOperatingActivities,
                cashflow_data.netCashUsedForInvestingActivites,
                cashflow_data.netCashUsedProvidedByFinancingActivities,
                cashflow_data.cashAtEndOfPeriod,
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            base=0
        )
    )

cashflow_chart.show()