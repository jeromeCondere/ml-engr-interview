
def sort_data(arccos_data):
   """Sort data using  by specific fields"""
   arccos_data.sort_values(by=['round_userId', 'round_startTime', 'roundId', 'hole_holeId', 'shot_shotId'], inplace=True)
   return arccos_data



def fill_na(arcos_data):
   arccos_data['shot_startTerrain'] = arccos_data['shot_startTerrain'].fillna('Green')
   arccos_data['shot_endTerrain'] = arccos_data['shot_endTerrain'].fillna('Green')
   return arccos_data

def get_shot_distance_coord_info(arcos_data):
   """add coordinate and shot distance to the dataframe"""
   # Calculate starting distance for each shot.
   arccos_data['start_coordinates'] = list(zip(arccos_data['shot_startLat'],
                                               arccos_data['shot_startLong']))
   arccos_data['pin_coordinates'] = list(zip(arccos_data['hole_pinLat'],
                                             arccos_data['hole_pinLong']))
   arccos_data['shot_start_distance_yards'] = arccos_data.apply(
       lambda row: distance.distance(row['start_coordinates'], row['pin_coordinates']).ft / 3, axis=1
   )
   arccos_data['shot_endLat'].fillna(arccos_data['hole_pinLat'], inplace=True)
   arccos_data['shot_endLong'].fillna(arccos_data['hole_pinLong'], inplace=True)
   arccos_data['end_coordinates'] = list(zip(arccos_data['shot_endLat'], arccos_data['shot_endLong']))

   # Calculate shot distance in yards using start and end coordinates.
   arccos_data['shot_distance_yards_calculated'] = arccos_data.apply(
    lambda row: distance.distance(row['start_coordinates'], row['end_coordinates']).ft / 3, axis=1
   )

   # Calculate end distance for each shot.
   arccos_data['shot_end_distance_yards'] = arccos_data.apply(
    lambda row: distance.distance(row['end_coordinates'], row['pin_coordinates']).ft / 3, axis=1
   )
   arccos_data['shot_end_distance_yards'].fillna(0, inplace=True)

   # Take hole length as the distance to CG for first shot.
   arccos_data['hole_yards'] = np.where(arccos_data['shot_shotId'] == 1,
                                     arccos_data['shot_startDistanceToCG'],
                                     np.nan)
   arccos_data['hole_yards'].ffill(inplace=True)
   arccos_data['hole_yards'] = pd.to_numeric(arccos_data['hole_yards'])

   return arccos_data


def get_shot_type_info(arccos_data):
   """add shot info to the dataframe"""
   # Impute shot type.
   conditions_shot_type = [(arccos_data['shot_startTerrain'] == 'Tee') & (arccos_data['hole_par'] != 3),
   (arccos_data['shot_start_distance_yards'] <= 30) & (arccos_data['shot_startTerrain'] != 'Green'),
   (arccos_data['shot_startTerrain'] == 'Green')]
   values = ['TeeShot', 'GreensideShot', 'Putt']
   arccos_data['shot_type'] = np.select(conditions_shot_type, values, default='ApproachShot')

   # Calculate z-scores for shot distance and start distance and by club and shot type.
   arccos_data['shot_distance_yards_zscore'] = (arccos_data.groupby(['round_userId', 'shot_type', 'shot_clubType'])
   ['shot_distance_yards_calculated']
   .transform(lambda x: zscore(x, ddof=1)))
   .fillna(0)

   arccos_data['shot_start_distance_yards_zscore'] = (arccos_data.groupby(['round_userId', 'shot_type', 'shot_clubType'])
   ['shot_start_distance_yards']
   .transform(lambda x: zscore(x, ddof=1)))
   .fillna(0)

   # Impute shot subtype.
   conditions = [arccos_data['shot_type'] == 'TeeShot',
   (arccos_data['shot_type'] == 'ApproachShot') &
   (arccos_data['shot_distance_yards_zscore'] <= -1) &
   (arccos_data['shot_end_distance_yards'] > 30) &
   (arccos_data['shot_endTerrain'] != 'Fairway'),
   (arccos_data['shot_type'] == 'ApproachShot') &
   (arccos_data['shot_distance_yards_zscore'] > -1) &
   (arccos_data['shot_start_distance_yards_zscore'] > 1) &
   (arccos_data['shot_end_distance_yards'] > 30),
   arccos_data['shot_type'] == 'GreensideShot',
   arccos_data['shot_type'] == 'Putt']

   values = ['TeeShot', 'Recovery', 'LayUp', 'GreensideShot', 'Putt']
   arccos_data['shot_subtype'] = np.select(conditions, values, default='GoingForGreen')



def process_fields(arccos_data):
   """process field by fixing the values"""
   arccos_data = arccos_data.fill_na(arcos_data)

   # Capitalize first letter of string
   arccos_data[['shot_startTerrain', 'shot_endTerrain']] = arccos_data[['shot_startTerrain', 'shot_endTerrain']].apply(
      lambda s: s.capitalize()
   )

   arccos_data = get_distance_coord(arcos_data)


