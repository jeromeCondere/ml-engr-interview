#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

import numpy as np


def get_bearing(start_coordinates, end_coordinates):
    """Get bearing between two points"""

    lat1 = np.radians(start_coordinates[0])
    lon1 = np.radians(start_coordinates[1])
    lat2 = np.radians(end_coordinates[0])
    lon2 = np.radians(end_coordinates[1])
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) \
        * math.cos(lat2) * math.cos(dLon)
    brng = np.rad2deg(math.atan2(y, x))
    if brng < 0:
        brng += 360
    return brng


def calculate_start_end_pin_angle(shot_distance,
                                  shot_start_distance_yards,
                                  shot_end_distance_yards):
    """Calculate short/long distances"""

    if shot_end_distance_yards > 0 and shot_distance > 0:
        phi = math.acos((shot_distance ** 2 + shot_end_distance_yards
                        ** 2 - shot_start_distance_yards ** 2) / (2
                        * shot_distance * shot_end_distance_yards))
    else:
        phi = 0
    return np.rad2deg(phi)


def calculate_miss_distance(miss_bearing_left_right,
                            start_end_pin_angle,
                            shot_end_distance_yards):
    """Calculate left/right distances."""

    if miss_bearing_left_right > 180:
        alpha = 180 - (360 - miss_bearing_left_right) \
            - start_end_pin_angle
    else:
        alpha = 180 - miss_bearing_left_right - start_end_pin_angle

    if start_end_pin_angle > 90:
        if miss_bearing_left_right > 180:
            distance_left_right = -shot_end_distance_yards \
                * math.sin(np.radians(alpha))
        else:
            distance_left_right = shot_end_distance_yards \
                * math.sin(np.radians(alpha))
        distance_short_long = -shot_end_distance_yards \
            * math.cos(np.radians(alpha))
    else:
        if miss_bearing_left_right > 180:
            distance_left_right = -shot_end_distance_yards \
                * math.sin(np.radians(180 - alpha))
        else:
            distance_left_right = shot_end_distance_yards \
                * math.sin(np.radians(180 - alpha))
        distance_short_long = shot_end_distance_yards \
            * math.cos(np.radians(180 - alpha))

    return (distance_left_right, distance_short_long)
