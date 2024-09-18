import plotly.graph_objects as go
from dash import dcc, html
from raw.format_number import format_number

config = {"displayModeBar": False}

chart_layout = {
    "paper_bgcolor": "#1C2432",
    "plot_bgcolor": "#1C2432",
    "font_family": "Inter",
    "font_color": "#FFFFFF",
    "xaxis": {
        "linecolor": "#3E5275",
        "gridcolor": "#3E5275",
        "zerolinecolor": "#3E5275",
    },
    "yaxis": {
        "linecolor": "#3E5275",
        "gridcolor": "#3E5275",
        "zerolinecolor": "#3E5275",
    },
    "legend": {
        "orientation": "h",
        "yanchor": "top",
        "x": 0.25,
    },
}


def update_cashflow_charts(cashflow_data, currency, year):

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
            text=[
                f"{currency}{format_number(cashflow_data.cashAtBeginningOfPeriod)}",
                f"{currency}{format_number(cashflow_data.netCashProvidedByOperatingActivities)}",
                f"{currency}{format_number(cashflow_data.netCashUsedForInvestingActivites)}",
                f"{currency}{format_number(cashflow_data.netCashUsedProvidedByFinancingActivities)}",
                f"{currency}{format_number(cashflow_data.cashAtEndOfPeriod)}",
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            base=0,
        )
    )

    cashflow_chart.update_layout(
        title=f"Cashflow Analysis {year}", **chart_layout, yaxis_tickprefix=currency
    )

    return html.Div(
        dcc.Graph(figure=cashflow_chart, config=config), className="cashflow-chart"
    )
