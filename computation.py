"""
Computation Module for the final project (CSC110 at the University of Toronto)
This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
"""

# from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import numpy as np


##########################################
# 1. Main function taking input from Data Module and returning output for Display Module
##########################################


def run_computations(data: dict[str, list[tuple[tuple[int, int], int]]]) \
        -> dict[str, tuple[list[tuple[tuple[int, int], int]], list[tuple[tuple[int, int], int]],
                           list[tuple[tuple[int, int], int]]]]:
    """ Given data, return a dictionary of sector mapped to a list of dates and actual values; a
    list of dates and expected values (rounded to the nearest integer); and a list of dates and
    deviations between the actual and expected values (rounded to the nearest integer).

    Preconditions:
        - len(data) != 0  # input dict is non-empty
        - all(len(sector_name) != 0 for sector_name in data.keys())  # sector names are non-empty
        - all(len(data[sector_name]) != 0 for sector_name in data.keys())  # Each sector's
        list of coordinates is non-empty; Note: non-empty lists of coordinates may not be strict
        enough
        - all(1 <= data[sector_name][i][0][1] <= 12 for i in range(len(data['Primary Sector'])) for
        sector_name in data.keys())  # Months are between 1 and 12
        - all(data[sector_name][i][1] >= 0 for i in range(len(data['Primary Sector'])) for
        sector_name in data.keys())  # GDP values are non-negative
    """
    index_of_covid = determine_index_of_covid(data['Primary Sector'])

    # ACCUMULATOR: dict_so_far: the running dictionary of computed data for each sector
    dict_so_far = {}

    sectors = ['Primary Sector', 'Secondary Sector', 'Tertiary Sector', 'Quaternary Sector']
    for sector in sectors:
        x_y_coords = dict_to_x_y_coords(data, sector)
        # x_y_coords: all coordinates in samp1.csv (i.e. from Jan 2014 to Aug 2021)
        # x_y_coords[0]: dates
        # x_y_coords[1]: actual GDP values

        x_y_coords_for_prediction = (x_y_coords[0][:index_of_covid], x_y_coords[1][:index_of_covid])
        # Note: slicing does not include end index (index_of_covid or (2020, 3))

        slope, intercept = regress(x_y_coords_for_prediction)

        lst_w_actual_values = actual_gdp_values(data[sector])
        lst_w_predicted_values = predict_gdp_values(data[sector], slope, intercept)
        deviations = calculate_dev(data[sector], slope, intercept)

        dict_so_far[sector] = (lst_w_actual_values, lst_w_predicted_values, deviations)

    return dict_so_far


##########################################
# 2. Separating and filtering x and y coordinates (for a sector)
##########################################

def dict_to_x_y_coords(data: dict[str, list[tuple[tuple[int, int], int]]], sector: str) \
        -> tuple[list[tuple[int, int]], list[int]]:
    """ Convert industry's data into a tuple of x-coords and y-coords.
    data in format: dict[str*industry*, list[tuple[tuple[int*year*, int*month*]], int*gdp*]]]
    x-coords: year
    y-coords: gdp

    Preconditions:
        - len(data) != 0  # input dict is non-empty
        - all(len(sector_name) != 0 for sector_name in data.keys())  # sector names are non-empty
        - all(len(data[sector_name]) != 0 for sector_name in data.keys())  # Each sector's
        list of coordinates is non-empty; Note: non-empty lists of coordinates may not be strict
        enough
        - all(1 <= data[sector_name][i][0][1] <= 12 for i in range(len(data[sector_name])) for
        sector_name in data.keys())  # Months are between 1 and 12
        - all(data[sector_name][i][1] >= 0 for i in range(len(data[sector_name])) for
        sector_name in data.keys())  # GDP values are non-negative
        - len(sector) != 0
    """
    x_coords = [data[sector][index][0] for index in range(len(data[sector]))]
    y_coords = [data[sector][index][1] for index in range(len(data[sector]))]

    return x_coords, y_coords


##########################################
# 3. Calculating coefficients of line of best fit
##########################################

def regress(x_y_coords: tuple[list[tuple[int, int]], list[int]]) -> tuple[float, float]:
    """Take x_y_coords and return coefficients of the line of best fit (y = a * x + b)
    as (a, b).

    Preconditions:
        - len(x_y_coords[0]) != 0
        - len(x_y_coords[0]) == len(x_y_coords[1])

    >>> coefficients = regress(([(2019, 12), (2020, 1), (2020, 2)], [0, 2, 4]))
    >>> round(coefficients[0])
    2
    >>> round(coefficients[1])
    0
    """
    model = linear_model.LinearRegression()
    x_coords = np.arange(len(x_y_coords[0])).reshape(-1, 1)
    y_coords = np.array(x_y_coords[1])

    # Train model
    model.fit(x_coords, y_coords)

    return model.coef_[0], model.intercept_


##########################################
# 4. Predicting GDP using line of best fit and finding deviation to actual values and list
# with actual values
##########################################


def actual_gdp_values(data: list[tuple[tuple[int, int], int]]) -> list[tuple[tuple[int, int], int]]:
    """Returns list containing actual GDP values with dates going up to May 2020

    Preconditions:
        - all(len(data) != 0
        - all(1 <= data[i][0][1] <= 12 for i in range(len(data))
        # Months are between 1 and 12
        - all(data[i][1] >= 0 for i in range(len(data)) # GDP values are non-negative
        - any((data[i][0] == (2020, 3)) for i in range(0, len(data)))
        - any((data[i][0] == (2020, 4)) for i in range(0, len(data)))
        - any((data[i][0] == (2020, 5)) for i in range(0, len(data)))
    """
    covid_start_index = determine_index_of_covid(data)

    lst_so_far = []
    for i in range(0, covid_start_index + 3):
        lst_so_far.append(data[i])
    return lst_so_far


def predict_gdp_values(data: list[tuple[tuple[int, int], int]], slope: float,
                       intercept: float) -> list[tuple[tuple[int, int], int]]:
    """Similar use pf predict_gpd_values, expect this function takes a list as input and returns a
    list

    Preconditions:
        - all(len(data) != 0
        - all(1 <= data[i][0][1] <= 12 for i in range(len(data))
        # Months are between 1 and 12
        - all(data[i][1] >= 0 for i in range(len(data)) # GDP values are non-negative
        - any((data[i][0] == (2020, 3)) for i in range(0, len(data)))
        - any((data[i][0] == (2020, 4)) for i in range(0, len(data)))
        - any((data[i][0] == (2020, 5)) for i in range(0, len(data)))
    """
    pred_data = filter_data(data)

    # determine index of March 2020 in list
    covid_start_index = determine_index_of_covid(data)  # index of March 2020

    for i in range(covid_start_index, covid_start_index + 3):
        predicted_gdp = int((i * round(slope, 3)) + round(intercept, 3))
        pred_data.append(((2020, 3 + (i - covid_start_index)), predicted_gdp))

    return pred_data


def filter_data(data: list[tuple[tuple[int, int], int]]) -> list[tuple[tuple[int, int], int]]:
    """ Helper Function for predict_gdp_values_to_list
    Return dict containing values and dates associated to dates prior to start of covid (March 2020)

    Preconditions:
        - all(len(data) != 0
        - any((data[i][0] == (2020, 3)) for i in range(0, len(data)))
    """
    # determine index of March 2020 in list
    covid_start_index = determine_index_of_covid(data)  # index of March 2020

    lst_so_far = []
    for i in range(0, covid_start_index):
        lst_so_far.append(data[i])

    return lst_so_far


def determine_index_of_covid(data: list[tuple[tuple[int, int], int]]) -> int:
    """Helper Function
    Determine index of March 2020 in list
    Preconditions:
        - all(len(data) != 0
        - all(1 <= data[i][0][1] <= 12 for i in range(len(data))
        # Months are between 1 and 12
        - all(data[i][1] >= 0 for i in range(len(data)) # GDP values are non-negative
        - any((data[i][0] == (2020, 3)) for i in range(0, len(data)))
    """
    for i in range(0, len(data)):
        if data[i][0] == (2020, 3):
            return i
    return 0


def calculate_dev(data: list[tuple[tuple[int, int], int]], slope: float,
                  intercept: float) -> list[tuple[tuple[int, int], int]]:
    """ Return a dictionary of
    sector mapped to a list of dates and deviations between the actual
    and expected values (rounded to the nearest integer)

    Preconditions:
        - all(len(data) != 0
        - all(1 <= data[i][0][1] <= 12 for i in range(len(data))
        # Months are between 1 and 12
        - all(data[i][1] >= 0 for i in range(len(data)) # GDP values are non-negative
        - any((data[i][0] == (2020, 3)) for i in range(0, len(data)))
        - any((data[i][0] == (2020, 4)) for i in range(0, len(data)))
        - any((data[i][0] == (2020, 5)) for i in range(0, len(data)))
    """
    lst_so_far = []
    covid_start_index = determine_index_of_covid(data)

    for i in range(covid_start_index, covid_start_index + 3):
        projected_value = slope * i + intercept
        actual_value = data[i][1]
        dev = actual_value - round(projected_value)
        date = data[i][0]
        lst_so_far.append((date, dev))
    return lst_so_far


if __name__ == '__main__':
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['python_ta.contracts', 'numpy', 'sklearn', 'math', 'datetime'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']}
    # )

    import doctest

    doctest.testmod(verbose=True)

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
