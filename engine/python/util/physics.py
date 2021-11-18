def get_percent(number, percent=1):
    return number / 100 * percent


def get_new_speed(v0, a, t):
    return v0 + a * t / 1000


def get_distance(v, t):
    return v * t / 1000
