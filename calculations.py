import math


def in_zone(event, point_1: tuple, point_2: tuple, correction_function) -> bool:
    point_1 = correction_function(point_1, rounding=False, native_failure_multiplier=1)
    point_2 = correction_function(point_2, rounding=False, native_failure_multiplier=1)
    return point_1[0] <= event.x <= point_2[0] and point_1[1] <= event.y <= point_2[1]


def in_circle(event, center: tuple, radius: int, correction_function) -> bool:
    center = correction_function(center, rounding=False, native_failure_multiplier=1)
    radius = correction_function(radius, rounding=False, native_failure_multiplier=1)
    hypotenuse = math.sqrt((event.x - center[0]) ** 2 + (event.y - center[1]) ** 2)
    return hypotenuse <= radius

