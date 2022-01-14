"""CSC110 Project 2020: The Plots of the Project

Description
===========
This module displays the plots for this project. It uses the plotly library
and contains the functions necessary to do so.

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Kevin Xia,
and Jennifer Cao. Any forms of distribution of this code, with or without
changes to this code, are prohibited.

This file is Copyright (c) 2020 Katherine Luo, Kevin Xia, and Jennifer Cao.
"""
from typing import List, Dict, Tuple, Any
import plotly.graph_objects as go


def display_plots(results: List[Tuple[List[float], List[float], Dict[str, float]]]) -> None:
    """Display the plots for the results of the data analysis.

    results consists of a list containing five tuples.
    Index 0 of the tuples contains the x-coordinates.
    Index 1 of the tuples contains the y-coordinates.
    Index 2 of the tuples contains a mapping of the results of the data analysis on these
    coordinates: slope, y-intercept, correlation, and coefficient of determination (R^2).

    The first tuple contains the data for a plot of year vs temperature.
    The second tuple contains the data for a plot of temperature vs nitrogen dioxide concentration.
    The third tuple contains the data for a plot of temperature vs ozone concentration.
    The fourth tuple contains the data for a plot of year vs nitrogen dioxide concentration.
    The fifth tuple contains the data for a plot of year vs ozone concentration.

    Preconditions:
        - len(results) == 5
        - all(len(result[0]) == len(result[1]) for result in results)
        - results follows the structure and other requirements mentioned above.
    """
    # Create a blank figure
    fig = go.Figure()

    # Add the plot and regression line of year vs temperature
    add_plot(fig=fig, x_axis=[1920, 2150], titles=('Year vs Temperature', 'Regression Line'),
             initial_visibility=True, results=results[0])

    # Add the plot and regression line of temperature vs nitrogen dioxide concentration
    add_plot(fig=fig, x_axis=[-50, 50],
             titles=('Temperature vs Nitrogen Dioxide', 'Nitrogen Dioxide Regression Line'),
             initial_visibility=False, results=results[1])

    # Add the plot and regression line of temperature vs ozone concentration
    add_plot(fig=fig, x_axis=[-50, 50],
             titles=('Temperature vs Ozone', 'Ozone Regression Line'),
             initial_visibility=False, results=results[2])

    # Add the plot and regression line of year vs nitrogen dioxide concentration
    add_plot(fig=fig, x_axis=[1920, 2150],
             titles=('Year vs Nitrogen Dioxide', 'Nitrogen Dioxide Regression Line'),
             initial_visibility=False, results=results[3])

    # Add the plot and regression line of year vs ozone concentration
    add_plot(fig=fig, x_axis=[1920, 2150], titles=('Year vs Ozone', 'Ozone Regression Line'),
             initial_visibility=False, results=results[4])

    # Add the drop-down menu to the figure by calling create_buttons()
    fig.update_layout(
        title='Year vs Average Temperature in Toronto',
        xaxis_title='Year',
        yaxis_title='Average Temperature (Celsius)',
        updatemenus=[dict(buttons=create_buttons())]
    )

    # Display the figure with the plots
    fig.show()


def add_plot(fig: go.Figure, x_axis: List[float], titles: Tuple[str, str], initial_visibility: bool,
             results: Tuple[List[float], List[float], Dict[str, float]]) -> None:
    """Add the plot and regression line for the given results to the given figure.

    x_axis is a list containing the smallest x-value at index 0 and the
    largest x-value at index 1.
    titles[0] is the name of the plot.
    titles[1] is the title of the regression line.
    initial_visibility is whether the plot is initially visible to the user.
    results[0] contains the x-coordinates for the plot.
    results[1] contains the y-coordinates for the plot.
    results[2] contains a mapping of the regression line results (slope, y-intercept,
    correlation, and coefficient of determination (R^2) to their corresponding values).

    Preconditions:
        - len(x_axis) == 2
        - x_axis[0] < x_axis[1]
        - len(results[0]) > 0
        - len(results[1]) > 0
        - len(results[0]) == len(results[1])
    """
    # Add scatter plot
    fig.add_trace(
        go.Scatter(name=f'<br>{titles[0]}',
                   x=results[0],  # x-coordinates
                   y=results[1],  # y-coordinates
                   mode='markers',
                   visible=initial_visibility)
    )

    # Add regression line
    fig.add_trace(
        go.Scatter(name=f'<br>{titles[1]}'
                        f'<br>Slope: {round(results[2]["slope"], 3)}'
                        f'<br>Y-intercept: {round(results[2]["y-intercept"], 3)}'
                        f'<br>Correlation: {round(results[2]["correlation"], 3)}'
                        f'<br>R^2: {round(results[2]["R^2"], 3)}',
                   x=x_axis,
                   y=[evaluate_line(results[2]['slope'],
                                    results[2]['y-intercept'],
                                    x_axis[0]),
                      evaluate_line(results[2]['slope'],
                                    results[2]['y-intercept'],
                                    x_axis[1])],
                   mode='lines',
                   visible=initial_visibility)
    )


def create_buttons() -> List[Dict[str, Any]]:
    """Return a list of the seven buttons for a drop-down menu."""
    # Button for year vs temperature plot
    button1 = dict(
        label='Year vs Temperature',
        method='update',
        args=[{'visible': [True, True, False, False, False, False,
                           False, False, False, False]},
              {'title': 'Year vs Average Temperature in Toronto',
               'xaxis': {'title': 'Year'},
               'yaxis': {'title': 'Average Temperature (Celsius)'}}]
    )

    # Button for temperature vs nitrogen dioxide concentration plot
    button2 = dict(
        label='Temperature vs Nitrogen Dioxide',
        method='update',
        args=[{'visible': [False, False, True, True, False, False,
                           False, False, False, False]},
              {'title': 'Average Temperature vs Nitrogen Dioxide '
                        'Concentration in Toronto',
               'xaxis': {'title': 'Temperature (Celsius)'},
               'yaxis': {'title': 'Nitrogen Dioxide Concentration (ppb)'}}]
    )

    # Button for temperature vs ozone concentration plot
    button3 = dict(
        label='Temperature vs Ozone',
        method='update',
        args=[{'visible': [False, False, False, False, True, True,
                           False, False, False, False]},
              {'title': 'Average Temperature vs Ozone Concentration in Toronto',
               'xaxis': {'title': 'Temperature (Celsius)'},
               'yaxis': {'title': 'Ozone Concentration (ppb)'}}]
    )

    # Button for temperature vs concentrations plots
    button4 = dict(
        label='Temperature vs Concentrations',
        method='update',
        args=[{'visible': [False, False, True, True, True, True,
                           False, False, False, False]},
              {'title': 'Average Temperature vs Concentrations in Toronto',
               'xaxis': {'title': 'Temperature (Celsius)'},
               'yaxis': {'title': 'Concentration (ppb)'}}]
    )

    # Button for year vs nitrogen dioxide concentration plot
    button5 = dict(
        label='Year vs Nitrogen Dioxide',
        method='update',
        args=[{'visible': [False, False, False, False, False, False,
                           True, True, False, False]},
              {'title': 'Year vs Predicted Nitrogen Dioxide Concentration in Toronto',
               'xaxis': {'title': 'Year'},
               'yaxis': {'title': 'Predicted Nitrogen Dioxide Concentration (ppb)'}}]
    )

    # Button for year vs ozone concentration plot
    button6 = dict(
        label='Year vs Ozone',
        method='update',
        args=[{'visible': [False, False, False, False, False, False,
                           False, False, True, True]},
              {'title': 'Year vs Predicted Ozone Concentration in Toronto',
               'xaxis': {'title': 'Year'},
               'yaxis': {'title': 'Predicted Ozone Concentration (ppb)'}}]
    )

    # Button for year vs concentrations plot
    button7 = dict(
        label='Year vs Concentrations',
        method='update',
        args=[{'visible': [False, False, False, False, False, False,
                           True, True, True, True]},
              {'title': 'Year vs Predicted Concentrations in Toronto',
               'xaxis': {'title': 'Year'},
               'yaxis': {'title': 'Predicted Concentration (ppb)'}}]
    )

    return [button1, button2, button3, button4, button5, button6, button7]


def evaluate_line(slope: float, y_intercept: float, x: float) -> float:
    """Return the y-value given the slope and the y-intercept of the regression line
    and corresponding x-value.
    """
    return slope * x + y_intercept


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            # The names (strs) of imported modules
            'extra-imports': ['plotly.graph_objects', 'python_ta.contracts'],
            # The names (strs) of functions that call print/open/input
            'allowed-io': [],
            'max-line-length': 100,
            'disable': ['R1705', 'C0200']
        }
    )
