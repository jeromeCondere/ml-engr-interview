#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import pandas as pd


def read_json_file(file):
    """Read Json file """

    try:
        with open(file) as f:
            file_data = [json.load(f)]
            return file_data
    except FileNotFoundError:
        print("File {} doesn't exist".format(file))
        return None
    except IOError:
        print("File {} not accessible".format(file))
        return None
    except Exception as e:
        print(e)


def read_excel_file(file):
    """ Read excel file """

    try:
        file_data = pd.read_excel(file)
        return file_data
    except FileNotFoundError:
        print("File {} doesn't exist".format(file))
        return None
    except IOError:
        print("File {} not accessible".format(file))
        return None
    except Exception as e:
        print(e)


def read_csv_file(file):
    """ Read csv file """

    try:
        file_data = pd.read_csv(file)
        return file_data
    except FileNotFoundError:
        print("File {} doesn't exist".format(file))
        return None
    except IOError:
        print("File {} not accessible".format(file))
        return None
    except Exception as e:
        print(e)
