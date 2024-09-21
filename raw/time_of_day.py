from datetime import datetime


def time_of_day():
    # get current hour
    current_hour = datetime.now().hour

    # return greeting
    if 5 <= current_hour < 12:
        return "Good morning ☼"
    elif 12 <= current_hour < 17:
        return "Good afternoon •ᴗ•"
    elif 17 <= current_hour < 21:
        return "Good evening ☾"
    else:
        return "Good night ᶻz"
