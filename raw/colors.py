def get_color(color):

    # list colours
    color_dict = {
        "black": "#101827",
        "chart_background_dark": "#1C2432",
        "chart_background_light": "#EDF2F8",
        "transparent": "rgba(0,0,0,0)",
        "chart_line_dark": "#3E5275",
        "chart_line_light": "#D2DBE7",
        "green": "#4BDB95",
        "pink": "#FF72D9",
        "purple": "#588AFF",
        "red": "#FF3B4C",
        "orange": "#FF7C58",
        "white": "#FFFFFF",
    }

    return color_dict.get(color)
