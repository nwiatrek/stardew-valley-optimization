import sys
import re
import numpy as np
import pandas as pd
import xlsxwriter
from datetime import datetime


def day_split(variables, number_of_days):
    """take in all the variables and put them into an array of arrays
    that is set for each day"""
    days = []
    iterator = 0
    number_of_days = int(number_of_days)
    while(iterator < number_of_days):
        temp = []
        days.append([])
        for variable in variables:
            if(f"on {iterator} " in variable):
                # push to the corresponding option
                days[iterator].append(variable)
                temp.append(variable)
        iterator += 1
    return days


def read_file(file):
    variables = []
    txt_file = open(file, 'r')
    lines = txt_file.readlines()
    for line in lines:
        variables.append(line)
    return variables


def make_map(day_vars):
    current_day = np.empty([29, 29], dtype=object)
    actions_filtered = []
    for i in day_vars:
        if('did plant' in i or 'occupied on' in i or 'prepped on' in i or ('sprinkler on' in i and 'bought sprinkler on' not in i)):
            actions_filtered.append(i)

    for i in actions_filtered:
        # print(i)
        value = re.search(r'(\d+,\d+)', i)
        if(value is None):
            print(i)
        coordinate = value.group(1)
        coordinate = coordinate.split(',')
        if(current_day[int(coordinate[0])][int(coordinate[1])] is None):
            current_day[int(coordinate[0])][int(coordinate[1])] = get_action(i)
    return current_day


def determine_if_action_taken(variable):
    if(variable[-5] is '1'):
        return True
    return False


def get_action(variable):
    if('did plant on' in variable and determine_if_action_taken(variable)):
        return re.search(r'\[.+\]', variable).group(0)
    elif('occupied on' in variable and determine_if_action_taken(variable)):
        return 'o'
    elif('sprinkler on' in variable and determine_if_action_taken(variable)):
        return 'SPRINKLER'
    elif('soil prepped' in variable and determine_if_action_taken(variable)):
        return 'prepped'


def main(file, number_of_days):
    variables = read_file(file)
    variable_by_day = day_split(variables, number_of_days)
    # print(variable_by_day[2])
    writer = pd.ExcelWriter('map_generated.xlsx')

    for i in range(len(variable_by_day)):
        map_day = make_map(variable_by_day[i])
        df = pd.DataFrame(map_day)
        df.to_excel(writer, f'day {i}')

    writer.save()
    print('done!')


if __name__ == '__main__':
    file = sys.argv[1]
    number_of_days = sys.argv[2]
    print(number_of_days)
    main(file, number_of_days)
