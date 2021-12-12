"""
Main Module for the final project (CSC110 at the University of Toronto)

This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
"""

from data import open_convert_and_aggregate
from computation import run_computations


def run_program(file: str = 'samp1.csv') -> None:
    """Runs the entire program by processing file (samp1.csv by default), predicting GDP values,
    and displaying graphs.

    samp1.csv has dates from Jan 2012 to Sep 2021.
    """
    data = open_convert_and_aggregate(file)

    data_points = run_computations(data, 5)
