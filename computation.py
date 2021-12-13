"""
Computation Module for the final project (CSC110 at the University of Toronto)

This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
"""

from sklearn.linear_model import LinearRegression
import numpy as np
import math
import datetime
from data import open_convert_and_aggregate


##########################################
# 1. Main function taking input from Data Module and returning output for Display Module
##########################################

def run_computations(data: dict[str, list[tuple[tuple[int, int], int]]], n_pred: int) \
        -> dict[str, tuple[list[tuple[tuple[int, int], int]], list[tuple[tuple[int, int], int]],
                           list[tuple[tuple[int, int], int]]]]:
    """Given data and the number of points used in the prediction (n_pred), return a dictionary of
    sector mapped to a list of dates and actual values; a list of dates and expected
    values (rounded to the nearest integer); and a list of dates and deviations between the actual
    and expected values (rounded to the nearest integer).
    """
    sectors = ['Primary Sector', 'Secondary Sector', 'Tertiary Sector', 'Quaternary Sector']
    for sector in sectors:
        x_y_coords = dict_to_x_y_coords(data=data, sector=sector, n_pred=5)
        # x_y_coords[0]: dates
        # x_y_coords[1]: actual GDP values used for prediction
        slope, intercept = regress(x_y_coords)  # for line of best fit
        deviations = calculate_dev(data[sector], slope, intercept)
        # TODO: change dict_to_x_y_coords to only convert dict to x_y_coords and add a filtering
        #  function (calculate_dev will receive x_y_coords as input while regression receive
        #  filtered x_y_coords as input)


##########################################
# 2. Separating and filtering x and y coordinates (for a sector)
##########################################

def dict_to_x_y_coords(data: dict[str, list[tuple[tuple[int, int], int]]], sector: str) \
        -> tuple[list[tuple[int, int]], list[int]]:
    """ Convert industry's data into a tuple of x-coords and y-coords.

    data in format: dict[str*industry*, list[tuple[tuple[int*year*, int*month*]], int*gdp*]]]

    x-coords: year
    y-coords: gdp

    >>> data = open_convert_and_aggregate('samp1.csv')  # From Jan 2012 to Sep 2021
    >>> dict_to_x_y_coords(data, 'Primary Sector')

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

    >>> coefficients = regress(([(2019, 12), (2020, 1), (2020, 2)], [0, 2, 4]))
    >>> math.isclose(round(coefficients[0], 4), 2)
    True
    >>> math.isclose(round(coefficients[1], 4), 0)
    True
    """
    model = LinearRegression()
    x_coords = np.arange(len(x_y_coords[0])).reshape(-1, 1)
    y_coords = np.array(x_y_coords[1])

    # Train model
    model.fit(x_coords, y_coords)

    return model.coef_[0], model.intercept_


##########################################
# 4. Predicting GDP using line of best fit and finding deviation to actual values
##########################################


def add_predict_gdp(data: dict[str, list[tuple[tuple[int, int], int]]]) -> ...:
    """ Add predicted GDP for a specific industry to master dict (derived in data.py) so that it can
    be displayed
    
    INCOMPLETE
    """
    # determine index of Feb 2020 in list
  
    covid_start_index = determine_index_of_covid(data['Primary Sector'])  # index of Feb 2020
    
    
    for sector in data:
        x_y_coords = dict_to_x_y_coords(data, sector)
        model_coefficients = regress(x_y_coords)
        for j in range(covid_start_index, covid_start_index + 3):
            predicted_gdp = x_y_coords[0][j] * model_coefficients[0] + model_coefficients[1]
        


def determine_index_of_covid(data: list[tuple[tuple[int, int], int]]) -> int:
    """Helper Function
    determine index of Feb 2020 in list
    """
    for i in range(0, len(data)):
        if data[i][0] == (2020, 2):
            return i



def calculate_dev(data: list[tuple[tuple[int, int], int]], slope: float, intercept: float) -> list[float]:
    """ Find deviations of actual data points from predicted data points from actual GDP values

    Calculate deviations of data[sector][73] (Feb 2020), data[sector][74] (March 2020) and
    data[sector][75] (April 2020), usuing samp1.csv data
    """
    lst_so_far = []
    covid_start = determine_index_of_covid(data)

    for i in range(covid_start, covid_start + 3):
        projected_value = slope * i + intercept
        actual_value = data[i][1]
        dev = projected_value - actual_value
        lst_so_far.append(dev)
    return lst_so_far


def calculate_rmsd(data: list[tuple[tuple[int, int], int]], slope: float, intercept: float) -> float:
    """ Find deviations of residuals for regression model, aka, root mean square deviation (RMSD)

    RMSD is a statistic that measures accuracy of a regression model
    """
    num_of_datapoints = determine_index_of_covid(data) - 1
    sum_of_residuals_sq_so_far = 0

    for i in range(0, num_of_datapoints + 1):
        residual_sq = (data[i][1] - slope * i + intercept) ** 2
        sum_of_residuals_sq_so_far += residual_sq

    return math.sqrt(sum_of_residuals_sq_so_far / (num_of_datapoints - 2))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'numpy', 'sklearn', 'math', 'datetime'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import doctest

    doctest.testmod()
