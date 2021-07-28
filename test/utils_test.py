from raw_data_import import get_key_list
from test_data import round_test_data
# pytest for utils function


def test_get_key_list_remove_fields():
    # test that gey_key_list return the keys without the fields to remove
    list_items_to_remove = ["shots"]
    keylist = get_key_list(round_test_data, list_items_to_remove)
    assert "shots" not in keylist


def test_get_key_list_fields():
    # test that the right fields are returned
    expected_fields = [
        "holeId", "noOfShots", "isGir", "putts", "isSandSaveChance", "isSandSave",
        "startTime", "endTime", "shouldIgnore", "isFairWay", "isFairWayRight", "isFairWayLeft",
        "approachShotId", "isUpDownChance", "isUpDown", "isFairWayUser",
        "isFairWayRightUser", "isFairWayLeftUser", "pinLat", "pinLong", "scoreOverride"
    ]

    list_items_to_remove = ["shots"]
    keylist = get_key_list(round_test_data, list_items_to_remove)
    assert set(keylist) == set(expected_fields)
