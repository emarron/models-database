import csv
from pprint import pprint


def convert_si_to_number(i):
    result = i
    i = i.lower()
    if 'k' in i:
        result = float(i.strip('k')) * 1000
    if 'm' in i:
        result = float(i.strip('m')) * 1000000
    if '?' in i:
        result = ""
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


csvinput = "input.csv"
dict_models = convert_csv_to_dict(csvinput)
pprint(dict_models)
for entry in dict_models:
    for key, value in entry.items():
        if key == 'Iterations' or key == 'Scale' or key == 'Batch Size ' or key == 'HR Size' or key == 'Dataset Size':
            entry[key] = convert_si_to_number(value)
            print(entry[key])
