"""
Main Module for the final project (CSC110 at the University of Toronto)

This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
"""

from data import open_convert_and_aggregate
from computation import run_computations
from display import Sector, graph_sectors


def run_program(file: str = 'samp1.csv') -> None:
    """Runs the entire program by processing file (samp1.csv by default), predicting GDP values,
    and displaying graphs.

    samp1.csv has dates from Jan 2014 to Sep 2021.

    Preconditions:
        - file != ''
    """
    data = open_convert_and_aggregate(file)

    data_points = run_computations(data)

    # ACCUMULATOR sectors: the running list of Sector objects
    sectors = []
    sector_names = ['Primary Sector', 'Secondary Sector', 'Tertiary Sector', 'Quaternary Sector']
    for sector_name in sector_names:
        sectors.append(Sector(name=sector_name, actual=data_points[sector_name][0],
                              expected=data_points[sector_name][1]))

    graph_sectors(sectors)


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['python_ta.contracts'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
