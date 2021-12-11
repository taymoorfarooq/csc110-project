"""
Data Module for the final project (CSC110 at the University of Toronto)

This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
"""

import csv
import python_ta

##########################################
# Data Wrangling: Converting to Dictionary
##########################################


def open_and_convert(filename: str) -> dict[str, list[tuple[tuple[int, int], int]]]:
    """
    Opens and converts the dataset into a dictionary

    Preconditions:
        - filename != ''

    >>> open_and_convert('samp1.csv')
    """

    return list_to_dict(file_to_list(filename))


def month_to_num(monthyear: str) -> tuple[int, int]:
    """
    Helper Function 1:

    Return a tuple with the tuple[int, int] equivalent of the input date string
    written in format: 'Year, Month'

    Preconditions:
        - monthyear != ''

    >>> month_to_num('January 2014')
    (2014, 1)
    """
    months = {'January': 1,
              'February': 2,
              'March': 3,
              'April': 4,
              'May': 5,
              'June': 6,
              'July': 7,
              'August': 8,
              'September': 9,
              'October': 10,
              'November': 11,
              'December': 12
              }

    return (int(monthyear[-4:len(monthyear)]), (months[monthyear[0:-5]]))


def file_to_list(filename: str) -> list[list[str]]:
    """
    Helper Function 2:

    Return a list of lists converting the raw sample data in CSV format

    Preconditions:
        - filename != ''

    >>> file_to_list('samp1.csv')
    """
    list_so_far = []

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            list_so_far = list_so_far + [row]

    return list_so_far


def list_to_dict(list_so_far: list) -> dict[str, list[tuple[tuple[int, int], int]]]:
    """
    Helper Function 3:

    Convert the input list into a dictionary

    Preconditions:
        - len(list_so_far) > 0

    """
    output_dict = {}
    dates = list_so_far[11]

    month_tuples = [month_to_num(x) for x in dates[1:len(dates)]]
    industry_list = [x[0] for x in list_so_far[13:len(list_so_far) - 11]]

    date_gdp = [[(month_tuples[i - 1], int(list_so_far[x][i].replace(',', '')))
                 for i in range(1, len(list_so_far[x]) - 11)]
                for x in range(13, len(list_so_far) - 11)]

    for j in range(0, len(industry_list)):
        output_dict[industry_list[j]] = date_gdp[j]

    return output_dict


##########################################
# Data Wrangling: Categorizing Data
##########################################


def aggregate_4sectors(combined_dict: dict) -> dict[str, list[tuple[tuple[int, int], int]]]:
    """
    Return a dictionary mapping the name of the economic sector
    (Primary/Secondary/Tertiary/Quaternary) to the aggregated
    sum of GDP values per industry in the respective sector.
    Input the dictionary from helper function: categorize_4_sectors

    Preconditions:
        - len(combined_dict) != 0

    >>> aggregate_4sectors(categorize_4_sectors(open_and_convert('samp1.csv')))
    """
    primary_keys = list(combined_dict['Primary'].keys())
    secondary_keys = list(combined_dict['Secondary'].keys())
    tertiary_keys = list(combined_dict['Tertiary'].keys())
    quaternary_keys = list(combined_dict['Quaternary'].keys())

    year_month_tuples = [combined_dict['Primary'][primary_keys[0]][j][0] for j in range(0, len(
        combined_dict['Primary'][primary_keys[0]]))]

    primary_sums = []
    secondary_sums = []
    tertiary_sums = []
    quaternary_sums = []

    ag_primary_data = []
    ag_secondary_data = []
    ag_tertiary_data = []
    ag_quaternary_data = []

    for i in range(0, len(combined_dict['Primary'][primary_keys[0]])):
        primary_sums = primary_sums + \
            [sum((combined_dict['Primary'][y][i][1]) for y in primary_keys)]
        secondary_sums = secondary_sums + \
            [sum((combined_dict['Secondary'][y][i][1]) for y in secondary_keys)]
        tertiary_sums = tertiary_sums + \
            [sum((combined_dict['Tertiary'][y][i][1]) for y in tertiary_keys)]
        quaternary_sums = quaternary_sums + \
            [sum((combined_dict['Quaternary'][y][i][1]) for y in quaternary_keys)]

        ag_primary_data = ag_primary_data + [(year_month_tuples[i], primary_sums[i])]
        ag_secondary_data = ag_secondary_data + [(year_month_tuples[i], secondary_sums[i])]
        ag_tertiary_data = ag_tertiary_data + [(year_month_tuples[i], tertiary_sums[i])]
        ag_quaternary_data = ag_quaternary_data + [(year_month_tuples[i], quaternary_sums[i])]

    return {'Primary': ag_primary_data, 'Secondary': ag_secondary_data,
            'Tertiary': ag_tertiary_data, 'Quaternary': ag_quaternary_data}


def categorize_4_sectors(dct: dict) -> dict[str, dict]:
    """
    Helper Function 4:

    Return a dictionary mapping the economic sector name
    (Primary/Secondary/Tertiary/Secondary) to the industries in them
    without aggregation


    Preconditions:
        len(dct) != 0

    >>> categorize_4_sectors(open_and_convert('samp1.csv'))
    """
    industry_list = list(dct.keys())
    primary_codes = ['[11]', '[21]']
    secondary_codes = ['[22]', '[23]', '[31-33]']
    tertiary_codes = ['[41]', '[44-45]', '[48-49]', '[52]', '[53]', '[54]', '[55]', '[56]',
                      '[61]', '[62]', '[71]', '[72]', '[81]', '[91]']
    quaternary_codes = ['51']
    primary_dict = {}
    secondary_dict = {}
    tertiary_dict = {}
    quaternary_dict = {}

    for y in industry_list:
        for p in primary_codes:
            if p in y:
                primary_dict[y] = dct[y]
        for s in secondary_codes:
            if s in y:
                secondary_dict[y] = dct[y]
        for t in tertiary_codes:
            if t in y:
                tertiary_dict[y] = dct[y]
        for q in quaternary_codes:
            if q in y:
                quaternary_dict[y] = dct[y]

    return {'Primary': primary_dict, 'Secondary': secondary_dict,
            'Tertiary': tertiary_dict, 'Quaternary': quaternary_dict}


python_ta.check_all(config={
    'extra-imports': ['csv'],  # the names (strs) of imported modules
    'allowed-io': ['file_to_list'],  # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['R1705', 'C0200']
})
