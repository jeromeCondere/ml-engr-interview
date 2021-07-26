
#TODO: evaluate
def sort_data(arccos_data):
   """Sort data using  by specific fields"""
   arccos_data.sort_values(by=['round_userId', 'round_startTime', 'roundId', 'hole_holeId', 'shot_shotId'], inplace=True)
   return arccos_data

def last_sort(arcos_data):
   # Add Clippd dataframe to data
   ## Sort.
   arccos_data.sort_values(by=['player_id', 'round_time', 'round_id', 'hole_id', 'shot_id'], inplace=True)
 



def fill_na(arcos_data):
   arccos_data['shot_startTerrain'] = arccos_data['shot_startTerrain'].fillna('Green')
   arccos_data['shot_endTerrain'] = arccos_data['shot_endTerrain'].fillna('Green')
   return arccos_data

def mapping(arccos_data, data_mapping_dict_file):
   data_dictionary = pd.read_excel(data_mapping_dict_file)
   arccos_data_dictionary = data_dictionary[['Clippd', 'Arccos']]
   arccos_data_dictionary = arccos_data_dictionary.dropna().set_index('Arccos').to_dict()['Clippd']
   filtered_columns = list(arccos_data_dictionary.keys())
   filtered_columns.remove("'arccos'")
   arccos_data = arccos_data[filtered_columns].copy()
   arccos_data.columns = arccos_data.columns.to_series().map(arccos_data_dictionary)  # TODO: fix
   arccos_data['data_source'] = 'arccos'
   return arccos_data



def process_fields(arccos_data):
   """process field by fixing the values"""
   arccos_data = arccos_data.fill_na(arcos_data)

   # Capitalize first letter of string
   arccos_data[['shot_startTerrain', 'shot_endTerrain']] = arccos_data[['shot_startTerrain', 'shot_endTerrain']].apply(
      lambda s: s.capitalize()
   )

   arccos_data = get_distance_coord(arcos_data)




def get_clipped_info(arcos_data, data_mapping_dict_file):
   """add clippd info to the dataframe"""
   data_dictionary = pd.read_excel(data_mapping_dict_file)
   clippd_data = pd.DataFrame(columns=data_dictionary['Clippd'].values)
   
     
   # Concatenate data sources.
   arccos_data = pd.concat([clippd_data, arccos_data])  # TODO: fix, empty df, add column if exists
   # Tidy datetime features and add round_date.
   datetime_features = ['round_time', 'shot_time']
   arccos_data[datetime_features] = arccos_data[datetime_features].apply(lambda x: x.replace(tzinfo=pytz.UTC))
       
   arccos_data['round_date'] = pd.to_datetime(arccos_data['round_time']).dt.date
   # Convert data_source to categorical variable and order dataframe.
   arccos_data['data_source'] = pd.Categorical(arccos_data['data_source'], categories=['arccos', 'gsl', 'whs'], ordered=True)
   arccos_data.sort_values(by=['data_source', 'player_id', 'round_time', 'round_id', 'hole_id'], inplace=True)
   
   return arcos_data

