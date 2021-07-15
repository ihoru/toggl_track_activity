def _get_duration_components(duration):
    days = duration.days
    seconds = duration.seconds

    minutes = seconds // 60
    seconds %= 60

    hours = minutes // 60
    minutes %= 60

    return days, hours, minutes, seconds


def duration_string(duration):
    days, hours, minutes, seconds = _get_duration_components(duration)

    string = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    if days:
        string = '{} day(s) '.format(days) + string

    return string
