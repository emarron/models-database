import csv
import pandas as pd


def convert_si_to_number(i):

    i = i.lower().strip(',')
    result = i
    if 'k' in i:
        result = int(float(i.strip('k')) * 1000)
    if 'm' in i:
        result = int(float(i.strip('m')) * 1000000)
    try:
        return int(result)
    except ValueError:
        return i


def convert_csv_to_dict(csvinput):
    dict_models = []
    with open(csvinput) as f:
        for row in csv.DictReader(f):
            dict_models.append(row)
    return dict_models


csvinput = "input.csv"
list_models = convert_csv_to_dict(csvinput)
columns = []
# list of dictionaries; just cleaning up the values of keys with specific rules. i.e., 'Iterations' must be float.
# Replacing '?' with nulls.
for dict_models in list_models:
    for key, value in dict_models.items():
        if key == 'Iterations' or key == 'Scale' or key == 'Batch Size ' or key == 'HR Size' or key == 'Dataset Size':
            dict_models[key] = convert_si_to_number(value)
        if dict_models[key] == '?':
            dict_models[key] = ''

df = pd.DataFrame(list_models)
# Giving an index for unique key. No change of duplicates.
export_csv = df.to_csv(r'export_models.csv')
