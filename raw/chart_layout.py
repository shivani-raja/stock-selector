from raw.colors import get_color


def get_layout(palette):

    # get colors
    transparent = get_color("transparent")
    chart_line_light = get_color("chart_line_light")
    chart_line_dark = get_color("chart_line_dark")
    white = get_color("white")
    black = get_color("black")

    if palette == "light":
        chart_line = chart_line_light
        font_color = black
    else:
        chart_line = chart_line_dark
        font_color = white

    chart_layout = {
        "paper_bgcolor": transparent,
        "plot_bgcolor": transparent,
        "font_family": "Inter",
        "font_color": font_color,
        "xaxis": {
            "linecolor": chart_line,
            "gridcolor": chart_line,
            "zerolinecolor": chart_line,
        },
        "yaxis": {
            "linecolor": chart_line,
            "gridcolor": chart_line,
            "zerolinecolor": chart_line,
        },
        "legend": {
            "orientation": "h",
            "yanchor": "top",
            "x": 0.25,
        },
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
    }

    return chart_layout
