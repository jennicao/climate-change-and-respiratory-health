"""CSC110 Project 2020: The Main File of the Project

Description
===========
This is the main file of the CSC110 project. This project focuses on the
effects of climate change and ozone concentration on Torontonian residents'
respiratory health. This main file runs the code necessary to wrangle the
datasets, perform simple linear regression on the data, and display the
results of this project.

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Kevin Xia,
and Jennifer Cao. Any forms of distribution of this code, with or without
changes to this code, are prohibited.

This file is Copyright (c) 2020 Katherine Luo, Kevin Xia, and Jennifer Cao.
"""
import data_wrangling
import data_analysis
import plots


if __name__ == '__main__':
    # Data wrangling: csv to dataclass
    toronto_atmospheres = data_wrangling.read_csv_data1('toronto_atmospheres.csv')
    toronto_daily_temps = data_wrangling.read_csv_data2('weatherstats_toronto_daily.csv')

    # Convert daily temperatures to yearly temperatures
    toronto_yearly_temps = data_wrangling.daily_to_yearly(toronto_daily_temps)

    # Set up the x-coordinates and y-coordinates for simple linear regression
    # ACCUMULATOR: Keep track of the x-coordinates (year) so far
    x_coords1 = []
    # ACCUMULATOR: Keep track of the y-coordinates (temperature) so far
    y_coords1 = []
    for yearly_temp in toronto_yearly_temps:
        x_coords1.append(yearly_temp.date.year)
        y_coords1.append(yearly_temp.avg_temp)

    # ACCUMULATOR: Keep track of the x-coordinates (temperature) so far
    x_coords2 = []
    # ACCUMULATOR: Keep track of the y-coordinates (nitrogen dioxide) so far
    y_coords2 = []
    # ACCUMULATOR: Keep track of the y-coordinates (ozone) so far
    y_coords3 = []
    for atmosphere in toronto_atmospheres:
        x_coords2.append(atmosphere.temperature)
        y_coords2.append(atmosphere.nitrogen_dioxide)
        y_coords3.append(atmosphere.ozone)

    # Data analysis: simple linear regression
    # year vs temperature
    results1 = data_analysis.simple_linear_regression(x_coords1, y_coords1)
    # temperature vs nitrogen dioxide concentration
    results2 = data_analysis.simple_linear_regression(x_coords2, y_coords2)
    # temperature vs ozone concentration
    results3 = data_analysis.simple_linear_regression(x_coords2, y_coords3)

    # SPECIAL ANALYSIS: year -> temperature -> nitrogen dioxide/ozone
    # ACCUMULATOR: Keep track of the predicted y-coordinates (nitrogen dioxide) so far
    y_coords4 = []
    # ACCUMULATOR: Keep track of the predicted y-coordinates (ozone) so far
    y_coords5 = []

    # Determine the predicted concentrations from year
    for year in x_coords1:
        temperature = results1['slope'] * year + results1['y-intercept']
        nitrogen_dioxide = results2['slope'] * temperature + results2['y-intercept']
        ozone = results3['slope'] * temperature + results3['y-intercept']

        y_coords4.append(nitrogen_dioxide)
        y_coords5.append(ozone)

    # year vs predicted nitrogen dioxide concentration
    results4 = data_analysis.simple_linear_regression(x_coords1, y_coords4)
    # year vs predicted ozone concentration
    results5 = data_analysis.simple_linear_regression(x_coords1, y_coords5)

    # Display plots
    plots.display_plots([(x_coords1, y_coords1, results1),
                         (x_coords2, y_coords2, results2),
                         (x_coords2, y_coords3, results3),
                         (x_coords1, y_coords4, results4),
                         (x_coords1, y_coords5, results5)])
