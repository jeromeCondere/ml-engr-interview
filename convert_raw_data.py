import json

# TODO: check if file exists
def read_json_file(file):
   """Read Json file"""
   with open(repr(file)) as f:
      file_data = [json.load(f)]
      return file_data


# TODO get unit tests for that
def get_key_list(data, list_items_to_remove):
   """Get key list from round data without the 'shot' key"""
   item = data[0]
   key_list = list(item['holes'][0].keys())
   key_list = [e for e in t if e not in list_items_to_remove]
   return key_list

# TODO uses generator
def get_hole_info_df(round_data):
   """Make a dataframe from hole info in the rounds data"""
   appended_data = []
   for item in rounds_data:
      key_list = get_key_list(round_data, ['shots'])  # ????? TODO: print
      shot_data = pd.json_normalize(item['holes'], 'shots', key_list, record_prefix='shot_', meta_prefix='hole_')
      shot_data['roundId'] = item['roundId']
      appended_data.append(shot_data)
   return pd.concat(appended_data)


def get_hole_round_merged_info(round_data, course_data):
   """merge hole and round info into a single dataframe"""
   # Convert round info to dataframe.
   arccos_hole_info = get_hole_info_df(round_data)
   arccos_round_info = pd.DataFrame(rounds_data)
   arccos_round_info.columns = ['round_' + column for column in arccos_round_info.columns]
   
   # join hole and round info tables and drop round_holes column.
   merged_info = arccos_hole_info.merge(arccos_round_info, left_on=['roundId'], right_on=['round_roundId'])
   merged_info.drop(columns=['round_holes'], inplace=True)

   # convert numeric feature columns to numeric
   numeric_features = ['shot_shotId', 'shot_clubType', 'shot_clubId', 'shot_startLat', 'shot_startLong',
                    'shot_endLat', 'shot_endLong', 'shot_distance', 'shot_startAltitude',
                    'shot_endAltitude', 'shot_noOfPenalties', 'hole_noOfShots', 'hole_pinLat',
                    'hole_pinLong', 'hole_putts', 'hole_holeId', 'hole_approachShotId', 'roundId',
                    'hole_noOfShots']
   merged_info[numeric_features] = merged_info[numeric_features].apply(pd.to_numeric, errors='coerce')

   # Convert time features to datetime.
   time_features = ['shot_shotTime', 'hole_startTime', 'hole_endTime', 'round_startTime', 'round_endTime']
   merged_info[time_features] = merged_info[numeric_features].apply(pd.to_datetime, errors='coerce')

   # Convert to boolean
   boolean_map = {'T': True, 'F': False, 1: True, 0: False, 'None': None}
   boolean_features = ['shot_isHalfSwing', 'shot_shouldIgnore', 'shot_isSandUser',
                    'shot_isNonSandUser', 'shot_shouldConsiderPuttAsChip', 'hole_isFairWayRight', 
                    'hole_isFairWayLeft', 'hole_scoreOverride', 'hole_isSandSave',
                    'hole_isUpDown', 'hole_isFairWayRightUser', 'hole_isFairWayUser',
                    'hole_isFairWayLeftUser', 'hole_isGir', 'hole_isFairWay',
                    'hole_isSandSaveChance']
   merged_info[boolean_features] = arccos_hole_info[boolean_features].replace(boolean_map)

   # Add course name.
   arccos_course_name = course_data[['name', 'courseId']].drop_duplicates()
   merged_info = merged_info.merge(arccos_course_name, how='left', left_on=['round_courseId'], right_on=['courseId'])

   return merged_info


def get_shot_info_df(shot_data):
   appended_data = []
   for item in terrain_data:
      key_list = get_key_list(shot_data, ['drive', 'approach', 'chip', 'sand'])
      drive_data = pd.json_normalize(item['holes'], 'drive', key_list, record_prefix='shot_', meta_prefix='hole_')
      approach_data = pd.json_normalize(item['holes'], 'approach', key_list, record_prefix='shot_', meta_prefix='hole_')
      chip_data = pd.json_normalize(item['holes'], 'chip', key_list, record_prefix='shot_', meta_prefix='hole_')
      sand_data = pd.json_normalize(item['holes'], 'sand', key_list, record_prefix='shot_', meta_prefix='hole_')
      shot_data = pd.concat([drive_data, approach_data, chip_data, sand_data], axis=0)
      shot_data['roundId'] = item['roundId']
      appended_data.append(shot_data)
    
   return pd.concat(appended_data)

def get_merged_info(round_data, course_data, shot_data, terrain_data):
   """get dataframe with all info merged"""
   arccos_hole_info = get_hole_round_merged_info(round_data, course_data)
   merged_info = arccos_hole_info.merge(
    arccos_hole_info_terrain[['roundId', 'hole_holeId', 'shot_shotId',
                              'hole_par', 'shot_startDistanceToCG',
                              'shot_startTerrain', 'shot_endTerrain']],
    how='left',
    left_on=['roundId', 'hole_holeId', 'shot_shotId'],
    right_on=['roundId', 'hole_holeId', 'shot_shotId'])
   return merged_info
