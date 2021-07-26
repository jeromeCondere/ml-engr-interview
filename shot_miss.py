# Determine shot miss directions and distances using coordinates and indicators.

def get_bearing(start_coordinates, end_coordinates):
   """Function to get bearing between two points"""
   lat1 = np.radians(start_coordinates[0])
   lon1 = np.radians(start_coordinates[1])
   lat2 = np.radians(end_coordinates[0])
   lon2 = np.radians(end_coordinates[1])
   dLon = lon2 - lon1
   y = math.sin(dLon) * math.cos(lat2)
   x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
   brng = np.rad2deg(math.atan2(y, x))
   if brng < 0:
      brng += 360
   return brng

def calculate_start_end_pin_angle(shot_distance, shot_start_distance_yards, shot_end_distance_yards):
   """Function to calculate short/long distances"""
   if(shot_end_distance_yards > 0) & (shot_distance > 0):
      phi = math.acos((shot_distance**2 + shot_end_distance_yards**2 - shot_start_distance_yards**2)
      (2 * shot_distance * shot_end_distance_yards))
   else:
      phi = 0
   return np.rad2deg(phi)

# Function to calculate left/right distances.
def calculate_miss_distance(miss_bearing_left_right, start_end_pin_angle, shot_end_distance_yards):
    if miss_bearing_left_right > 180:
        alpha = 180 - (360 - miss_bearing_left_right) - start_end_pin_angle
    else:
        alpha = 180 - miss_bearing_left_right - start_end_pin_angle
        
    if start_end_pin_angle > 90:
        if miss_bearing_left_right > 180:
            distance_left_right = -shot_end_distance_yards*math.sin(np.radians(alpha))
        else:
            distance_left_right = shot_end_distance_yards*math.sin(np.radians(alpha))
        distance_short_long = -shot_end_distance_yards*math.cos(np.radians(alpha))
    else:
        if miss_bearing_left_right > 180:
            distance_left_right = -shot_end_distance_yards*math.sin(np.radians(180 - alpha))
        else:
            distance_left_right = shot_end_distance_yards*math.sin(np.radians(180 - alpha))
        distance_short_long = shot_end_distance_yards*math.cos(np.radians(180 - alpha))
        
    return distance_left_right, distance_short_long


def get_shot_miss_info(arccos_data):
   """add shot miss info to data"""
   arccos_data['start_to_end_bearing'] = arccos_data.apply(
       lambda row: get_bearing(row['start_coordinates'], row['end_coordinates']), axis=1)
   arccos_data['start_to_pin_bearing'] = arccos_data.apply(
       lambda row: get_bearing(row['start_coordinates'], row['pin_coordinates']), axis=1)
   arccos_data['miss_bearing_left_right'] = arccos_data['start_to_end_bearing'] - arccos_data['start_to_pin_bearing']
   arccos_data['miss_bearing_left_right'] = np.where(arccos_data['miss_bearing_left_right']<0,
                                                     arccos_data['miss_bearing_left_right']+360,
                                                     arccos_data['miss_bearing_left_right'])
   
   # Determine miss distances.
   arccos_data['end_to_pin_bearing'] = arccos_data.apply(
       lambda row: get_bearing(row['end_coordinates'], row['pin_coordinates']), axis=1)
   arccos_data['start_end_pin_angle'] = arccos_data.apply(
       lambda row: calculate_start_end_pin_angle(row['shot_distance_yards_calculated'],
                                                 row['shot_start_distance_yards'],
                                                 row['shot_end_distance_yards']), axis=1
   )
   arccos_data['shot_miss_distance'] = arccos_data.apply(
       lambda row: calculate_miss_distance(row['miss_bearing_left_right'],
                                           row['start_end_pin_angle'],
                                           row['shot_end_distance_yards']), axis=1
   )
   
   arccos_data[['shot_miss_distance_left_right',
                'shot_miss_distance_short_long']] = pd.DataFrame(arccos_data['shot_miss_distance'].tolist(),
                                                                 index=arccos_data.index)
   
   # Impute left/right and short_long miss directions for approach shots.
   conditions = [(arccos_data['shot_type'] == 'ApproachShot') & (arccos_data['hole_isGir'] == False) &
                 (arccos_data['shot_miss_distance_left_right'] < 0),
                 (arccos_data['shot_type'] == 'ApproachShot') & (arccos_data['hole_isGir'] == False) &
                 (arccos_data['shot_miss_distance_left_right'] > 0)]
   values = ['Left', 'Right']
   arccos_data['shot_miss_direction_left_right'] = np.select(conditions, values, default=np.nan)
   conditions = [(arccos_data['shot_type'] == 'ApproachShot') & (arccos_data['hole_isGir'] == False) &
                 (arccos_data['shot_miss_distance_short_long'] < 0),
                 (arccos_data['shot_type'] == 'ApproachShot') & (arccos_data['hole_isGir'] == False) &
                 (arccos_data['shot_miss_distance_short_long'] > 0)]
   values = ['Short', 'Long']
   arccos_data['shot_miss_direction_short_long'] = np.select(conditions, values, default=np.nan)
               
   
   # Use miss distance information to impute miss_direction.
   conditions = [(arccos_data['shot_type'] == 'TeeShot') & (arccos_data['hole_isFairWayRight'] == True),
                 (arccos_data['shot_type'] == 'TeeShot') & (arccos_data['hole_isFairWayLeft'] == True),
                 (arccos_data['shot_type'] == 'ApproachShot') & (arccos_data['hole_isGir'] == False)]
   values = ['Right',
             'Left',
             (arccos_data['shot_miss_direction_short_long']
              + ' '
              + arccos_data['shot_miss_direction_left_right'])]
   arccos_data['shot_miss_direction_all_shots'] = np.select(conditions, values, default=np.nan) 