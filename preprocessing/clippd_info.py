import pandas as pd
import pytz


def get_clipped_info(arccos_data, data_mapping_dict_file):
    """add clippd info to the dataframe"""

    data_dictionary = pd.read_excel(data_mapping_dict_file)
    clippd_data = pd.DataFrame(columns=data_dictionary["Clippd"].values)

    # Concatenate data sources.
    arccos_data = pd.concat([clippd_data, arccos_data])  # TODO: fix, empty df, add column if exists
    # Tidy datetime features and add round_date.
    datetime_features = ["round_time", "shot_time"]
    arccos_data[datetime_features] = arccos_data[datetime_features].applymap(
        lambda x: x.replace(tzinfo=pytz.UTC)
    )

    arccos_data["round_date"] = pd.to_datetime(arccos_data["round_time"]).dt.date
    # Convert data_source to categorical variable and order dataframe.
    arccos_data["data_source"] = pd.Categorical(
        arccos_data["data_source"], categories=["arccos", "gsl", "whs"], ordered=True
    )

    return arccos_data
