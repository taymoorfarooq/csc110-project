"""
Display Module for the final project (CSC110 at the University of Toronto)
This file is Copyright (c) 2021 Xi Chen, Taymoor Farooq, Se-Eum Kim and Henry Klinck.
"""

# NOTE TO RUN, INSTALL PANDAS TO INTERPRETER
# File > Settings > Python Interpreter > press the + button > search 'pandas' > install

from dataclasses import dataclass
import pandas
import plotly.express as px


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
      - self.name != ''
      - all(1 <= point[0][1] <= 12 for point in self.actual)
      - all(1 <= point[0][1] <= 12 for point in self.expected)
      - all(point[1] >= 0 for point in self.actual)
      - all(point[1] >= 0 for point in self.expected)
      - all(point[0] in [p[0] for p in ac] for point in ex)
    """
    name: str
    actual: list[tuple[tuple[int, int], int]]
    expected: list[tuple[tuple[int, int], int]]


def graph_sectors(sectors: list[Sector]) -> None:
    """Displays a line graph of a list of sectors using Plotly.
    Each sector is shown as a different colour with the actual data being a solid line
    and expected points being shown with a dashed line.
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
    difference = []

    for sector in sectors:
        for i in range(len(sector.actual)):
            sector_name.append(sector.name)
            date.append(str(sector.actual[i][0]))
            gdp.append(sector.actual[i][1])
            style.append('Actual')
            if sector.actual[i][0] in [point[0] for point in sector.expected]:
                difference.append(sector.expected[i][1] - sector.actual[i][1])
            else:
                difference.append('N/A')

        for i in range(len(sector.expected)):
            sector_name.append(sector.name)
            date.append(str(sector.expected[i][0]))
            gdp.append(sector.expected[i][1])
            style.append('Expected')
            difference.append(sector.expected[i][1] - sector.actual[i][1])

    data = {'Date': date, 'Sector': sector_name, 'GDP (in $)(x 1,000,000)': gdp, 'Style': style,
            'Difference in GDP (in $)(x 1,000,000)': difference}
    df = pandas.DataFrame(data)

    graph = px.line(df, title='Monthly Canadian Expected GDP Values vs. Actual GDP Values '
                              '(Categorized by Economic Sector)', x='Date',
                    y='GDP (in $)(x 1,000,000)', color='Sector', line_dash='Style',
                    hover_data=['Difference in GDP (in $)(x 1,000,000)'])
    graph.show()


def graph_changes(sectors: list[Sector]) -> None:
    """Displays a graph showing the differences in expected and actual GDP values for each sector
    in sectors using Plotly
    >>> s1 = Sector('Sector1', [((2020, 2), 4), ((2020, 3), 5), ((2020, 4), 3), ((2020, 5), 4)], \
    [((2020, 2), 4), ((2020, 3), 4), ((2020, 4), 2), ((2020, 5), 3)])
    >>> s2 = Sector('Sector2', [((2020, 2), 8), ((2020, 3), 7), ((2020, 4), 8), ((2020, 5), 10)], \
    [((2020, 2), 8), ((2020, 3), 6), ((2020, 4), 5), ((2020, 5), 4)])
    >>> graph_changes([s1, s2])
    """
    date = []
    sector_name = []
    difference = []

    for sector in sectors:
        for i in range(3):
            date.append(str((2020, 3 + i)))
            sector_name.append(sector.name)
            difference.append(sector.expected[-(3 - i)][1] - sector.actual[-(3 - i)][1])

    data = {'Date': date, 'Sector': sector_name,
            'Difference in GDP (in $)(x 1,000,000)': difference}
    df = pandas.DataFrame(data)

    graph = px.line(df, title='The Difference Between Expected and Actual GDP Values '
                              '(Categorized by Economic Sector)', x='Date',
                    y='Difference in GDP (in $)(x 1,000,000)', color='Sector')
    graph.show()
    
    
def graph_percentage(sectors: list[Sector]) -> None:
    """Displays a graph showing the percentage lost in expected and actual GDP values
    for each sector in sectors using Plotly
    """
    date = []
    sector_name = []
    percents = []

    for sector in sectors:
        for i in range(3):
            date.append(str((2020, 3 + i)))
            sector_name.append(sector.name)
            percents.append(100 - (sector.actual[-(3 - i)][1] / 
                                     sector.expected[-(3 - i)][1] * 100))

    data = {'Date': date, 'Sector': sector_name, 'Percentage lost in GDP': percents}
    df = pandas.DataFrame(data)

    graph = px.line(df, title='The Percentage Lost Between Expected and Actual GDP Values '
                              '(Categorized by Economic Sector)', x='Date',
                    y='Percentage lost in GDP', color='Sector')
    graph.show()


if __name__ == '__main__':
    import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': ['python_ta.contracts', 'math', 'pandas', 'plotly.express', 'dataclass'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })

    import doctest

    doctest.testmod()
    
