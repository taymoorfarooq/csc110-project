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

    >>> open_and_convert('samp1.csv')
    """

    return list_to_dict(file_to_list(filename))


def month_to_num(monthyear: str) -> tuple[int, int]:
    """
    Helper Function 1:

    Return a tuple with the tuple[int, int] equivalent of the input date string
    written in format: 'Year, Month'

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
    """
    output_dict = {}
    dates = list_so_far[11]

    month_tuples = [month_to_num(x) for x in dates[1:len(dates)]]
    industry_list = [x[0] for x in list_so_far[13:len(list_so_far) - 11]]

    date_gdp = [[(month_tuples[i - 1], list_so_far[x][i])
                 for i in range(1, len(list_so_far[x]) - 11)]
                for x in range(13, len(list_so_far) - 11)]

    for j in range(0, len(industry_list)):
        output_dict[industry_list[j]] = date_gdp[j]

    return output_dict


python_ta.check_all(config={
    'extra-imports': ['csv'],  # the names (strs) of imported modules
    'allowed-io': ['file_to_list'],  # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['R1705', 'C0200']
})
