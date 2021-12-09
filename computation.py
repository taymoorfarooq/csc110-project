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

def regress(x_coords: list[float],  y_coords: list[float]) -> tuple[float, float]:
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
