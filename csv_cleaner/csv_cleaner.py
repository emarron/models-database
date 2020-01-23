import csv
from pprint import pprint

import cursor as cursor


def convert_si_to_number(i):
    result = i
    i = i.lower()
    if 'k' in i:
        result = float(i.strip('k')) * 1000
    if 'm' in i:
        result = float(i.strip('m')) * 1000000
    try:
        return float(result)
    except ValueError:
        return result


def convert_csv_to_dict(csvinput):
    dict_models = []
    with open(csvinput) as f:
        for row in csv.DictReader(f):
            dict_models.append(row)
    return dict_models


csvinput = "input-3.csv"
list_models = convert_csv_to_dict(csvinput)
# list of dictionaries; just cleaning up the values of keys with specific rules. i.e., 'Iterations' must be float.
list_models_cleaned = []
for dict_models in list_models:
    for key, value in dict_models.items():
        if key == 'Iterations' or key == 'Scale' or key == 'Batch Size ' or key == 'HR Size' or key == 'Dataset Size':
            dict_models[key] = convert_si_to_number(value)
    dict_models_cleaned = {key: value for key, value in dict_models.items() if key != '?'}
    list_models_cleaned.append(dict_models_cleaned)

# Dump list of dictionaries into sql, for database insertion.
for dict_models_cleaned in list_models_cleaned:
    # https://blog.softhints.com/python-3-convert-dictionary-to-sql-insert/ code from here
    placeholders = ', '.join(['%s'] * len(dict_models_cleaned))
    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in dict_models_cleaned.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict_models_cleaned.values())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('Models', columns, values)
    f = open("Models.sql", "a")
    f.write(sql + '\n')

# TODO: remove this sql creation crap; replace with csv generated file that I can dump into database. Too much work
#  otherwise, cause the dataset is only 75 entries. I can control debris better, when its in an actual database.
#  Obviously removing "/" in urls is a bad idea. Coding in a language you haven't touched in 9 months while sleep
#  deprived isn't cost effective.
