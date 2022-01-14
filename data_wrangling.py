"""CSC110 Project 2020: The Data Wrangling of the Project

Description
===========
This module does the data wrangling for this project. It contains the
functions and dataclasses necessary to do so. The functions are responsible
for reading the CSV files. The dataclasses represent the variables in the
datasets.

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Kevin Xia,
and Jennifer Cao. Any form of distribution of this code, with or without
changes to this code, is prohibited.

This file is Copyright (c) 2020 Katherine Luo, Kevin Xia, and Jennifer Cao.
"""
from typing import List
from dataclasses import dataclass
import csv
import datetime


@dataclass
class TorontoAtmosphere:
    """A dataclass representing Toronto's atmosphere.

    Instance Attributes:
        - temperature: the temperature in Toronto (in Celsius)
        - nitrogen_dioxide: the nitrogen dioxide concentration in Toronto (in ppb)
        - ozone: the ozone concentration in Toronto (in ppb)

    Representation Invariants:
        - self.temperature > -273.15
        - self.ozone > 0
        - self.nitrogen_dioxide > 0
    """
    temperature: float
    nitrogen_dioxide: float
    ozone: float


@dataclass
class TorontoTemperatureYearly:
    """A dataclass representing Toronto's average yearly temperature.

    Instance Attributes:
        - date: the date in Toronto
        - avg_temp: the average yearly temperature in Toronto (in Celsius)

    Preconditions:
        - date.year > 0
        - 1 <= date.month <= 12
        - 1 <= date.day <= 31
        - date.day is a valid day for date.month
    """
    date: datetime.date
    avg_temp: float


@dataclass
class TorontoTemperatureDaily:
    """A dataclass representing Toronto's average daily temperature.

    Instance Attributes:
        - date: the date in Toronto
        - avg_temp: the average daily temperature in Toronto (in Celsius)

    Preconditions:
        - date.year > 0
        - 1 <= date.month <= 12
        - 1 <= date.day <= 31
        - date.day is a valid day for date.month
    """
    date: datetime.date
    avg_temp: float


def read_csv_data1(filepath: str) -> List[TorontoAtmosphere]:
    """Return a list of TorontoAtmosphere dataclasses that represent
     rows from the CSV file: toronto_atmospheres.csv.

    Preconditions:
        - filepath == 'toronto_atmospheres.csv'
        - toronto_atmospheres.csv is not empty
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        # ACCUMULATOR: Keep track of the rows in the data
        # converted to TorontoAtmosphere dataclasses so far
        data_so_far = []

        for row in reader:
            data_so_far.append(csv_to_dataclass1(row))

    return data_so_far


def csv_to_dataclass1(csv_row: List[str]) -> TorontoAtmosphere:
    """Return a TorontoAtmosphere dataclass that represents a
    row in the CSV file dataset: toronto_atmospheres.csv.

    Preconditions:
        - csv_row refers to a row from the following CSV file:
        toronto_atmospheres.csv
        - toronto_atmospheres.csv is not empty
    """
    return TorontoAtmosphere(temperature=float(csv_row[1]),
                             nitrogen_dioxide=float(csv_row[2]),
                             ozone=float(csv_row[3]))


def read_csv_data2(filepath: str) -> List[TorontoTemperatureDaily]:
    """Return a list of TorontoTemperatureDaily dataclasses that represent
     rows from the CSV file: weatherstats_toronto_daily.csv.

    Preconditions:
        - filepath == 'weatherstats_toronto_daily.csv'
        - weatherstats_toronto_daily.csv is not empty
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        # ACCUMULATOR: Keep track of the rows in the data
        # converted to TorontoTemperatureDaily dataclasses so far
        data_so_far = []

        for row in reader:
            # Check that the temperature exists
            # Else, skip and don't append to list
            if row[1] != '':
                data_so_far.append(csv_to_dataclass2(row))

    return data_so_far


def csv_to_dataclass2(csv_row: List[str]) -> TorontoTemperatureDaily:
    """Return a TorontoTemperatureDaily dataclass that represents a
    row in the CSV file dataset: weatherstats_toronto_daily.csv.

    Preconditions:
        - csv_row refers to a row from the following CSV file:
        weatherstats_toronto_daily.csv
        - weatherstats_toronto_daily.csv is not empty
    """
    return TorontoTemperatureDaily(date=datetime.date.fromisoformat(csv_row[0]),
                                   avg_temp=float(csv_row[1]))


def daily_to_yearly(daily_temps: List[TorontoTemperatureDaily]) \
        -> List[TorontoTemperatureYearly]:
    """Return a list of TorontoTemperatureYearly dataclasses that contain the average temperature
    of each year from 1940-2020.

    daily_temps is a list of average daily temperatures in Toronto from 1940-2020.

    Preconditions:
        - len(daily_temps) > 0
    """
    # Add another daily temperature so that the average yearly temperature of 1940 is
    # calculated in the for loop instead of getting "skipped over"
    daily_temps_modified = daily_temps + [TorontoTemperatureDaily(date=datetime.date(9999, 1, 1),
                                                                  avg_temp=0)]

    # ACCUMULATOR: Keep track of the current year so far
    # (Starts from 2020 and goes to 1940)
    current_year = daily_temps[0].date.year
    # ACCUMULATOR: Keep track of the average yearly temperatures so far
    yearly_temps_so_far = []
    # ACCUMULATOR: Keep track of the average daily temperatures so far
    temps_so_far = []

    # Loop through each daily average temperature
    for daily_temp in daily_temps_modified:
        temps_so_far.append(daily_temp.avg_temp)

        # Check if the year ends
        if daily_temp.date.year != current_year:
            # Calculate the average temperature for that year
            average_temp = sum(temps_so_far) / len(temps_so_far)

            # Create a TorontoTemperatureYearly dataclass
            yearly_temp = TorontoTemperatureYearly(date=datetime.date(current_year, 1, 1),
                                                   avg_temp=average_temp)

            # Append yearly_temp to yearly_temps_so_far
            yearly_temps_so_far.append(yearly_temp)

            # Start a new year
            current_year = daily_temp.date.year
            temps_so_far = []

    return yearly_temps_so_far


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
            'extra-imports': ['dataclasses', 'csv', 'datetime', 'python_ta.contracts'],
            # The names (strs) of functions that call print/open/input
            'allowed-io': ['read_csv_data1', 'read_csv_data2'],
            'max-line-length': 100,
            'disable': ['R1705', 'C0200']
        }
    )
