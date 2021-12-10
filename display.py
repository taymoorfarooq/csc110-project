"""
Display Module for the final project (CSC110 at the University of Toronto)
This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
"""

# NOTE TO RUN, INSTALL PANDAS TO INTERPRETER
# File > Settings > Python Interpreter > press the + button > search 'pandas' > install

import pandas
import plotly.express as px
import python_ta
from dataclasses import dataclass


@dataclass
class Sector:
    """Dataclass containing data about an economic sector. Contains 2 lists of tuples,
    one for each actual and expected GDP values in a certain year and month
    as well as the name of the sector.
    Instance Attributes:
      - name: name of sector
      - actual: the GDP values from the dataset and date
      - expected: GDP values calculated from line of best fit based off pre-pandemic values and date

    Representation Invariants:
      - name != ''
      - all dates are valid
      - TODO?

    """
    name: str
    actual: list[tuple[tuple[int, int], int]]
    expected: list[tuple[tuple[int, int], int]]


def graph_sectors(sectors: list[Sector]) -> None:
    """TODO: docstring

    >>> s1 = Sector('Sector1', [((2020, 1), 4), ((2020, 2), 5), ((2020, 3), 3), ((2020, 4), 4), \
    ((2020, 5), 6)], [((2020, 1), 4), ((2020, 2), 5), ((2020, 3), 2), ((2020, 4), 3)])
    >>> s2 = Sector('Sector2', [((2020, 1), 8), ((2020, 2), 7), ((2020, 3), 8), ((2020, 4), 10), \
    ((2020, 5), 9)], [((2020, 1), 8), ((2020, 2), 7), ((2020, 3), 6), ((2020, 4), 5)])
    >>> graph_sectors([s1, s2])

    """
    date = []
    sector_name = []
    gdp = []
    style = []

    for sector in sectors:
        for i in range(len(sector.actual)):
            sector_name.append(sector.name)
            date.append(str(sector.actual[i][0]))
            gdp.append(sector.actual[i][1])
            style.append('Actual')
        for i in range(len(sector.expected)):
            sector_name.append(sector.name)
            date.append(str(sector.expected[i][0]))
            gdp.append(sector.expected[i][1])
            style.append('Expected')

    data = {'Date': date, 'Sector': sector_name, 'GDP': gdp, 'Style': style}
    df = pandas.DataFrame(data)

    graph = px.line(df, x='Date', y='GDP', color='Sector', line_dash='Style')
    graph.show()


# TODO: pythonTA stuff
