from preprocessing import process_fields
from raw_data_import import convert_raw_data

from utils.file_utils import read_json_file


def generate_arccos_data(
        round_data_file, course_data_file, terrain_data_file,
        pga_file, pga_putting_file, data_mapping_dict_file
):
    round_data = read_json_file(round_data_file)
    course_data = read_json_file(course_data_file)
    terrain_data = read_json_file(terrain_data_file)
    list_data = [round_data, course_data, terrain_data]

    # If something went wrong while loading the file a None is returned
    if(None in list_data):
        return None
    else:
        raw_data_file = convert_raw_data(round_data, course_data, terrain_data)
        arccos_data = process_fields(raw_data_file, pga_file, pga_putting_file, data_mapping_dict_file)
        return arccos_data


def main():
    """Produces the arccos data"""

    round_data_file = "round.json"
    course_data_file = "2020-12-03T12_20_14.080Z.json"
    terrain_data_file = "terrain.json"
    pga_file = "PGA Benchmark.csv"
    pga_putting_file = "PGA Putting Benchmark.csv"
    data_mapping_dict_file = "data_dictionary.xlsx"
    arccos_data = generate_arccos_data(
        round_data_file, course_data_file, terrain_data_file,
        pga_file, pga_putting_file, data_mapping_dict_file
    )
    if(arccos_data is not None):
        arccos_data.to_csv("arccos_data.csv", encoding="utf-8", index=False)
    else:
        print("An error occured. Exiting")


if __name__ == "__main__":
    main()
