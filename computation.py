"""
Data Module for the final project (CSC110 at the University of Toronto)

This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.

References
    - L29.py
"""

"""
Data Module for the final project (CSC110 at the University of Toronto)
This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
References
    - L29.py
"""

import python_ta
from sklearn.linear_model import LinearRegression
import numpy as np
import math


##########################################
# Computation: Outputting Coefficients of Line of Best Fit
##########################################

def dict_to_x_y_coords(data: dict[str, list[tuple[tuple[int, int], int]]], industry: str) -> (tuple[int, int]):
    """ Convert data into the x coords and y coords associated with the specified industry.
    The first int in the returned tuple corresponds with the x-coords.

    data in format: dict[str*industry*, list[tuple[tuple[int*year*, int*month*]], int*gdp*]]]

    x-coords: year
    y-coords: gdp
    """


def regress(x_coords: list[int], y_coords: list[int]) -> tuple[float, float]:
    """Take x_coords and y_coords and return coefficients of the line of best fit (y = a * x + b)
    as (a, b).
    >>> coefficients = regress([1, 2, 3], [2, 4, 6])
    >>> math.isclose(round(coefficients[0], 4), 2)
    True
    >>> math.isclose(round(coefficients[1], 4), 0)
    True
    """
    model = LinearRegression()
    x_coords = np.array(x_coords).reshape(-1, 1)
    y_coords = np.array(y_coords)

    # Train model
    model.fit(x_coords, y_coords)

    return model.coef_[0], model.intercept_


def predict_gdp() ->
    """ Predict gdp using regress values


    """

def add_predict_gdp() ->
    """ Add predicted GDP for a specific industry to master dict (derived in data.py) so that it can be displayed


    """

def calculate_dev() ->
    """ Find the deviation between pre-pandemic projections and the actual GDP value
    
    """

