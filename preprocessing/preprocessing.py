from clippd_info import get_clipped_info
from shot_distance import get_shot_distance_coord_info
from shot_miss import get_shot_miss_info
from shot_type import get_shot_type_info
from strokes_gained import get_strokes_gained_info

from utils.file_utils import read_csv_file
from utils.file_utils import read_excel_file


def sort(arccos_data):
    arccos_data.sort_values(
        by=["player_id", "round_time", "round_id", "hole_id", "shot_id"], inplace=True
    )
    return arccos_data


def fill_na(arccos_data):
    arccos_data["shot_startTerrain"] = arccos_data["shot_startTerrain"].fillna("Green")
    arccos_data["shot_endTerrain"] = arccos_data["shot_endTerrain"].fillna("Green")
    return arccos_data


def mapping(arccos_data, data_mapping_dict):
    arccos_data_dictionary = data_mapping_dict
    arccos_data_dictionary = (
        arccos_data_dictionary.dropna().set_index("Arccos").to_dict()["Clippd"]
    )
    filtered_columns = list(arccos_data_dictionary.keys())
    filtered_columns.remove("'arccos'")
    arccos_data = arccos_data[filtered_columns].copy()
    arccos_data.columns = arccos_data.columns.to_series().map(
        arccos_data_dictionary
    )
    arccos_data["data_source"] = "arccos"
    return arccos_data


def process_fields(arccos_data, pga_file, pga_putting_file, data_mapping_dict_file):
    """process field by fixing the values"""

    # Process the dataframe  generated by convert raw
    arccos_data = fill_na(arccos_data)

    # Capitalize first letter of string
    arccos_data[["shot_startTerrain", "shot_endTerrain"]] = arccos_data[
        ["shot_startTerrain", "shot_endTerrain"]
    ].applymap(lambda s: s.capitalize())

    arccos_data = get_shot_distance_coord_info(arccos_data)
    print("shot distance info added")

    arccos_data = get_shot_type_info(arccos_data)
    print("shot type info added")

    arccos_data = get_shot_miss_info(arccos_data)
    print("shot miss info added")

    pga = read_csv_file(pga_file)
    pga_putting = read_csv_file(pga_putting_file)

    arccos_data = get_strokes_gained_info(
        arccos_data, pga, pga_putting
    )
    print("strokes gained info added")

    data_mapping_dict = read_excel_file(data_mapping_dict_file)
    arccos_data = mapping(arccos_data, data_mapping_dict)

    arccos_data = get_clipped_info(arccos_data, data_mapping_dict)
    arccos_data = sort(arccos_data)

    return arccos_data
