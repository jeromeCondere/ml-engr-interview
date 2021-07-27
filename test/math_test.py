from utils import calculate_miss_distance
from utils import calculate_start_end_pin_angle
from utils import get_bearing


def test_bearing():
    # Test that the bearing function works properly
    start_coord = (40, -60)
    end_coord = (38.89, -80)
    bearing1 = get_bearing(start_coord, end_coord)

    start_coord = (45, 2)
    end_coord = (39, -40)
    bearing2 = get_bearing(start_coord, end_coord)

    assert round(bearing1, 4) == 272.3233
    assert round(bearing2, 4) == 274.0282


def test_distance():
    start_end_pin_angle = calculate_start_end_pin_angle(
        shot_distance=5, shot_start_distance_yards=7, shot_end_distance_yards=2
    )
    assert round(start_end_pin_angle, 4) == 180.0


def test_calculate_start_end_pin_angle():
    start_end_pin_angle = calculate_start_end_pin_angle(
        shot_distance=5, shot_start_distance_yards=7, shot_end_distance_yards=2
    )
    assert round(start_end_pin_angle, 4) == 180.0


def test_miss_distance():
    miss_distance1 = calculate_miss_distance(
        miss_bearing_left_right=22, start_end_pin_angle=160, shot_end_distance_yards=7
    )
    assert (round(miss_distance1[0], 4), round(miss_distance1[1], 4)) == (
        -0.2443,
        -6.9957,
    )

    miss_distance2 = calculate_miss_distance(
        miss_bearing_left_right=2, start_end_pin_angle=10, shot_end_distance_yards=7
    )
    assert (round(miss_distance2[0], 4), round(miss_distance2[1], 4)) == (1.4554, 6.847)
