"""
Computation Module for the final project (CSC110 at the University of Toronto)

This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
"""

# import python_ta
from sklearn.linear_model import LinearRegression
import numpy as np
import math
import datetime
from data import open_convert_and_aggregate


##########################################
# Computation: Outputting Coefficients of Line of Best Fit
##########################################

def dict_to_x_y_coords(data: dict[str, list[tuple[tuple[int, int], int]]], industry: str,
                       n_pred: int) -> tuple[list[int], list[int]]:
    """ Convert industry's data into a tuple of x-coords and y-coords, filtered to include n_pred
    data points.

    data in format: dict[str*industry*, list[tuple[tuple[int*year*, int*month*]], int*gdp*]]]

    x-coords: year
    y-coords: gdp

    >>> data = open_convert_and_aggregate('samp1.csv')  # From Jan 2012 to Sep 2021
    >>> dict_to_x_y_coords(data, 'Primary Sector', 5)

    """
    n_pred = min(128, len(data[industry]))  # compatible also with a small sample of the data
    # COVID_START_MONTH_COUNT = data[industry].index(((2020, 3), ...))  # archived implementation

    # index 0:
    data_first_month = datetime.date(data[industry][0][0][0], data[industry][0][0][1], 1)
    pred_last_month = datetime.date(2020, 2, 1)
    # index 0 + (data_first_month - pred_last_month)
    pred_last_month_index = diff_month(data_first_month, pred_last_month)
    # Multiple list element indexing: lst[<start>:<end + 1>]
    x_y_coords = data[industry][pred_last_month_index - n_pred:pred_last_month_index + 1]


def diff_month(d1: datetime.date, d2: datetime.date) -> int:
    """
    Return the number of months between d1 and d2.

    >>> diff_month(datetime.date(2020, 2, 1), datetime.date(2019, 2, 1))
    12
    >>> diff_month(datetime.date(2020, 2, 1), datetime.date(2020, 3, 1))
    -1
    """
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def regress(x_y_coords: tuple[list[int], list[int]]) -> tuple[float, float]:
    """Take x_y_coords and return coefficients of the line of best fit (y = a * x + b)
    as (a, b).

    >>> coefficients = regress([1, 2, 3], [2, 4, 6])
    >>> math.isclose(round(coefficients[0], 4), 2)
    True
    >>> math.isclose(round(coefficients[1], 4), 0)
    True
    """
    model = LinearRegression()
    x_coords = np.array(x_y_coords[0]).reshape(-1, 1)
    y_coords = np.array(x_y_coords[1])

    # Train model
    model.fit(x_coords, y_coords)

    return model.coef_[0], model.intercept_


def predict_gdp() -> ...:
    """ Predict gdp using regress values


    """


def add_predict_gdp() -> ...:
    """ Add predicted GDP for a specific industry to master dict (derived in data.py) so that it can
    be displayed


    """


def calculate_dev() -> ...:
    """ Find the deviation between pre-pandemic projections and the actual GDP value
    
    """
