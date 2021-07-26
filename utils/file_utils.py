def read_json_file(file):
   """Read Json file """
   try:
      with open(repr(file)) as f:
         file_data = [json.load(f)]
         return file_data
   except FileNotFoundError:
      print("File doesn't exist")
      return None
   except IOError:
      print("File not accessible")
      return None
   except Exception as e:
      print(e)

def read_excel_file(file):
   """ Read excel file """
   try:
      file_data = pd.read_excel(data_mapping_dict_file)
      return file_data
   except FileNotFoundError:
      print("File doesn't exist")
      return None
   except IOError:
      print("File not accessible")
      return None
   except Exception as e:
      print(e)

