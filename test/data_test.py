from io import StringIO

import pandas as pd
from clippd_info import get_clipped_info
from preprocessing import mapping
from raw_data_import import convert_raw_data
from shot_distance import get_shot_distance_coord_info
from shot_miss import get_shot_miss_info
from shot_type import get_shot_type_info
from strokes_gained import get_strokes_gained_info
from test_data import course_test_data
from test_data import data_mapping_dict_str
from test_data import pga_putting_str
from test_data import pga_str
from test_data import round_test_data
from test_data import terrain_test_data


def test_convert_raw_data():
    """ Test convert raw data """

    raw_data_converted = convert_raw_data(round_test_data, course_test_data, terrain_test_data)
    raw_data_converted_columns = set(raw_data_converted.columns)
    expected_columns = {
        "shot_shotId", "shot_clubType", "shot_clubId", "shot_startLat",
        "shot_startLong", "shot_endLat", "shot_endLong", "shot_distance",
        "shot_isHalfSwing", "shot_startAltitude", "shot_endAltitude",
        "shot_shotTime", "shot_shouldIgnore", "shot_noOfPenalties",
        "shot_isSandUser", "shot_isNonSandUser",
        "shot_shouldConsiderPuttAsChip", "shot_userStartTerrainOverride",
        "hole_putts", "hole_noOfShots", "hole_isSandSave", "hole_isFairWayUser",
        "hole_startTime", "hole_endTime", "hole_isGir", "hole_holeId",
        "hole_approachShotId", "hole_isSandSaveChance", "hole_scoreOverride",
        "hole_isUpDown", "hole_isFairWayLeft", "hole_pinLong",
        "hole_shouldIgnore", "hole_isFairWayRightUser", "hole_pinLat",
        "hole_isFairWay", "hole_isFairWayRight", "hole_isFairWayLeftUser",
        "hole_isUpDownChance", "roundId", "round_roundId", "round_roundVersion",
        "round_courseId", "round_userId", "round_startTime", "round_endTime",
        "round_noOfHoles", "round_noOfShots", "round_shouldIgnore",
        "round_teeId", "round_isPrivate", "round_isVerified", "round_isEnded",
        "round_isDriverRound", "round_courseVersion", "round_lastModifiedTime",
        "round_noOfHolesOverride", "round_scoreOverride", "name", "courseId",
        "hole_par", "shot_startDistanceToCG", "shot_startTerrain",
        "shot_endTerrain"
    }
    assert(raw_data_converted.shape[0] > 0)
    assert(expected_columns == raw_data_converted_columns)


def test_shot_distance():
    """ Test adding shot distance info"""

    raw_data_converted = convert_raw_data(round_test_data, course_test_data, terrain_test_data)
    raw_data_converted_columns = set(raw_data_converted.columns)

    arccos_data = get_shot_distance_coord_info(raw_data_converted)
    arccos_data_columns = set(arccos_data.columns)

    expected_columns_added = {
        "start_coordinates", "pin_coordinates", "shot_start_distance_yards",
        "end_coordinates", "shot_distance_yards_calculated", "shot_end_distance_yards", "hole_yards"
    }
    assert(arccos_data_columns - raw_data_converted_columns == expected_columns_added)


def test_shot_type():
    """ Test adding shot type info"""

    raw_data_converted = convert_raw_data(round_test_data, course_test_data, terrain_test_data)

    arccos_data = get_shot_distance_coord_info(raw_data_converted)
    arccos_data_old_columns = set(arccos_data.columns)
    arccos_data = get_shot_type_info(arccos_data)
    arccos_data_new_columns = set(arccos_data.columns)

    expected_columns_added = {
        "shot_type", "shot_distance_yards_zscore", "shot_start_distance_yards_zscore", "shot_subtype"
    }
    assert(arccos_data_new_columns - arccos_data_old_columns == expected_columns_added)


def test_shot_miss():
    """ Test adding shot miss info """

    raw_data_converted = convert_raw_data(round_test_data, course_test_data, terrain_test_data)

    arccos_data = get_shot_distance_coord_info(raw_data_converted)
    arccos_data = get_shot_type_info(arccos_data)
    arccos_data_old_columns = set(arccos_data.columns)
    arccos_data = get_shot_miss_info(arccos_data)
    arccos_data_new_columns = set(arccos_data.columns)

    expected_columns_added = {
        "start_to_end_bearing", "start_to_pin_bearing", "miss_bearing_left_right",
        "miss_bearing_left_right", "end_to_pin_bearing", "start_end_pin_angle", "shot_miss_distance",
        "shot_miss_direction_left_right", "shot_miss_direction_short_long", "shot_miss_direction_all_shots",
        "shot_miss_distance_left_right", "shot_miss_distance_short_long"
    }

    assert(arccos_data_new_columns - arccos_data_old_columns == expected_columns_added)


def test_strokes_gained():
    """ Test adding strokes gained info"""

    raw_data_converted = convert_raw_data(round_test_data, course_test_data, terrain_test_data)

    arccos_data = get_shot_distance_coord_info(raw_data_converted)
    arccos_data = get_shot_type_info(arccos_data)
    arccos_data = get_shot_miss_info(arccos_data)
    arccos_data_old_columns = set(arccos_data.columns)

    pga = pd.read_csv(StringIO(pga_str))
    pga_putting = pd.read_csv(StringIO(pga_putting_str))
    arccos_data = get_strokes_gained_info(
        arccos_data, pga, pga_putting
    )
    arccos_data_new_columns = set(arccos_data.columns)

    expected_columns_added = {"next_shot_shotId", "strokes_gained_calculated"}

    assert(arccos_data_new_columns - arccos_data_old_columns == expected_columns_added)


def test_mapping():
    """ test that the mapped dataframe contains columns from data dict """

    raw_data_converted = convert_raw_data(round_test_data, course_test_data, terrain_test_data)

    arccos_data = get_shot_distance_coord_info(raw_data_converted)
    arccos_data = get_shot_type_info(arccos_data)
    arccos_data = get_shot_miss_info(arccos_data)

    pga = pd.read_csv(StringIO(pga_str))
    pga_putting = pd.read_csv(StringIO(pga_putting_str))
    arccos_data = get_strokes_gained_info(
        arccos_data, pga, pga_putting
    )

    data_mapping_dict = pd.read_csv(StringIO(data_mapping_dict_str))
    arccos_data = mapping(arccos_data, data_mapping_dict)
    arccos_data_columns = set(arccos_data.columns)

    expected_columns_kept = {
        "shot_strokes_gained", "club_id", "shot_miss_distance_short_long", "course_id", "player_id",
        "shot_end_lat", "shot_miss_distance_left_right", "shot_distance_yards", "shot_category",
        "shot_end_long", "hole_score", "round_id", "shot_end_lie", "shot_end_distance_yards",
        "shot_start_lie", "round_score", "shot_miss_direction", "shot_start_distance_yards",
        "pin_lat", "pin_long", "hole_id", "shot_time", "hole_yards", "shot_type", "shot_start_long",
        "round_time", "shot_start_lat", "hole_par", "shot_id", "holes_played", "data_source"
    }

    assert(arccos_data.shape[1] == 31)
    assert(arccos_data_columns == expected_columns_kept)


def test_clipped_info():
    """ test that the final dataframe has the right ammount of columns"""

    raw_data_converted = convert_raw_data(round_test_data, course_test_data, terrain_test_data)

    arccos_data = get_shot_distance_coord_info(raw_data_converted)
    arccos_data = get_shot_type_info(arccos_data)
    arccos_data = get_shot_miss_info(arccos_data)

    pga = pd.read_csv(StringIO(pga_str))
    pga_putting = pd.read_csv(StringIO(pga_putting_str))
    arccos_data = get_strokes_gained_info(
        arccos_data, pga, pga_putting
    )

    data_mapping_dict = pd.read_csv(StringIO(data_mapping_dict_str))
    arccos_data = mapping(arccos_data, data_mapping_dict)
    arccos_data = get_clipped_info(arccos_data, data_mapping_dict)
    arccos_data_columns = set(arccos_data.columns)

    expected_columns_kept = {
        "shot_start_distance_yards", "hole_yards", "shot_end_lat", "shot_category",
        "round_id", "shot_type", "shot_time", "hole_par", "pin_long",
        "shot_strokes_gained", "data_source", "shot_end_lie", "shot_distance_yards",
        "course_id", "round_time", "shot_end_distance_yards", "hole_score", "round_score",
        "shot_end_long", "shot_start_long", "shot_miss_direction", "shot_start_lie",
        "shot_miss_distance_left_right", "round_date", "shot_id", "player_id",
        "pin_lat", "holes_played", "hole_id", "club_id", "shot_start_lat", "shot_miss_distance_short_long"
    }

    assert(arccos_data.shape[1] == 32)
    assert(arccos_data_columns == expected_columns_kept)
