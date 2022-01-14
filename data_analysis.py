"""CSC110 Project 2020: The Data Analysis of the Project

Description
===========
This module does the data analysis for this project. It contains functions
that perform simple linear regression and related calculations on the datasets.

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Kevin Xia,
and Jennifer Cao. Any form of distribution of this code, with or without
changes to this code, is prohibited.

This file is Copyright (c) 2020 Katherine Luo, Kevin Xia, and Jennifer Cao.
"""
from typing import List, Dict, Tuple
import math


def simple_linear_regression(x_coords: List[float], y_coords: List[float]) \
        -> Dict[str, float]:
    """Return a mapping of the slope, the y-intercept, the correlation, and
    the coefficient of determination (R^2) of the regression line to their
    corresponding values after performing simple linear regression on the
    given x- and y-coordinates.

    Preconditions:
        - len(x_coords) > 0
        - len(y_coords) > 0
        - len(x_coords) == len(y_coords)
    """
    # n = the number of x- and y-coodinates
    n = len(x_coords)

    # Calculate the average of x-coordinates and the average of y-coordinates
    x_avg = sum(x_coords) / len(x_coords)
    y_avg = sum(y_coords) / len(y_coords)

    # Calculate the numerators and denominators of the formulas for the
    # slope, correlation, and R^2 of the regression line
    numerator, x_denominator, y_denominator = \
        calculate_formulas(x_coords, y_coords, n, x_avg, y_avg)

    # Calculate the slope, y-intercept, and correlation
    slope = numerator / x_denominator
    y_intercept = y_avg - slope * x_avg
    correlation = numerator / math.sqrt(x_denominator * y_denominator)

    # Calculate R^2
    r_squared_numerator = sum([(y_coords[i] - (slope * x_coords[i] + y_intercept)) ** 2
                               for i in range(0, n)])
    r_squared = 1 - r_squared_numerator / y_denominator

    return {'slope': slope, 'y-intercept': y_intercept,
            'correlation': correlation, 'R^2': r_squared}


def calculate_formulas(x_coords: List[float], y_coords: List[float], n: int,
                       x_avg: float, y_avg: float) -> Tuple[float, float, float]:
    """Return a tuple of the numerators and denominators of the formulas for the slope,
    correlation, and coefficient of determination (R^2) for the regression
    line based on the given x- and y-coordinates.

    n is the number of x- and y-coordinates.
    x_avg is the average of the x-coordinates.
    y_avg is the average of the y-coordinates.

    The return at index 0 is the numerators of the formulas.
    The return at index 1 is the denominators involving x-coordinates of the formulas.
    The return at index 2 is the denominators involving y-coordinates of the formulas.

    Preconditions:
        - len(x_coords) > 0
        - len(y_coords) > 0
        - n > 0
        - len(x_coords) == len(y_coords) == n
    """
    # ACCUMULATOR: Keep track of the sum of the numerator seen
    # so far for the formulas
    numerator_so_far = 0

    # ACCUMULATOR: Keep track of the sum of the denominator
    # involving x-coordinates seen so far for the formulas
    x_denominator_so_far = 0

    # ACCUMULATOR: Keep track of the sum of the denominator
    # involving y-coordinates seen so far for the formulas
    y_denominator_so_far = 0

    # Calculate the numerators and denominators of the formulas for
    # slope, y-intercept, correlation, and R^2
    for i in range(0, n):
        numerator_so_far += (x_coords[i] - x_avg) * (y_coords[i] - y_avg)
        x_denominator_so_far += (x_coords[i] - x_avg) ** 2
        y_denominator_so_far += (y_coords[i] - y_avg) ** 2

    return (numerator_so_far, x_denominator_so_far, y_denominator_so_far)


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
            'extra-imports': ['math', 'python_ta.contracts'],
            # The names (strs) of functions that call print/open/input
            'allowed-io': [],
            'max-line-length': 100,
            'disable': ['R1705', 'C0200']
        }
    )
