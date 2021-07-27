from raw_data_import import get_key_list
# pytest for utils function

round_info_test_data = [{
    "roundId": 6175751,
    "roundVersion": 226,
    "courseId": 947,
    "userId": "simple user id",
    "startTime": "2020-12-17T12:04:09.000000Z",
    "endTime": "2020-12-17T15:46:13.485000Z",
    "noOfHoles": 18,
    "noOfShots": 76,
    "shouldIgnore": "F",
    "teeId": 2,
    "isPrivate": "F",
    "isVerified": "F",
    "isEnded": "T",
    "isDriverRound": "F",
    "courseVersion": 3,
    "lastModifiedTime": "2020-12-17T15:46:30.227000Z",
    "noOfHolesOverride": None,
    "scoreOverride": None,
    "holes":
    [
        {
            "holeId": 1,
            "noOfShots": 6,
            "isGir": "F",
            "putts": 2,
            "isSandSaveChance": "F",
            "isSandSave": "F",
            "startTime": "2020-12-17T12:09:12.338000Z",
            "endTime": "2020-12-17T12:24:05.173000Z",
            "shouldIgnore": "F",
            "isFairWay": "F",
            "isFairWayRight": "F",
            "isFairWayLeft": "T",
            "approachShotId": 4,
            "isUpDownChance": "F",
            "isUpDown": "F",
            "isFairWayUser": None,
            "isFairWayRightUser": None,
            "isFairWayLeftUser": None,
            "pinLat": 52.165891736696,
            "pinLong": 0.172658975318,
            "scoreOverride": None,
            "shots":
            [
                {
                    "shotId": 1,
                    "clubType": 2,
                    "clubId": 2,
                    "startLat": 52.166022757016,
                    "startLong": 0.166272406133,
                    "endLat": 52.166277519753,
                    "endLong": 0.168771843281,
                    "distance": 173.363,
                    "isHalfSwing": "F",
                    "startAltitude": 30.303,
                    "endAltitude": 41.2584,
                    "shotTime": "2020-12-17T12:09:12.338000Z",
                    "shouldIgnore": "F",
                    "noOfPenalties": 0,
                    "isSandUser": None,
                    "isNonSandUser": None,
                    "shouldConsiderPuttAsChip": "F",
                    "userStartTerrainOverride": 0
                }
            ]
        }
    ]
}]


def test_get_key_list_remove_fields():
    # test that gey_key_list return the keys without the fields to remove
    list_items_to_remove = ["shots"]
    keylist = get_key_list(round_info_test_data, list_items_to_remove)
    assert "shots" not in keylist


def test_get_key_list_fields():
    # test that the right fields are returned
    expected_fields = [
        "holeId", "noOfShots", "isGir", "putts", "isSandSaveChance", "isSandSave",
        "startTime", "endTime", "shouldIgnore", "isFairWay", "isFairWayRight", "isFairWayLeft",
        "approachShotId", "isUpDownChance", "isUpDown", "isFairWayUser",
        "isFairWayRightUser", "isFairWayLeftUser", "pinLat", "pinLong", "scoreOverride"]

    list_items_to_remove = ["shots"]
    keylist = get_key_list(round_info_test_data, list_items_to_remove)
    assert set(keylist) == set(expected_fields)
