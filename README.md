Pekauto Test Task Documentation
Hamid Mahoodabadi
Mahmoodabadihamid@gmail.com

## Introduction

The GNSS (Global Navigation Satellite System) module is a collection of functions designed to process and analyze raw GNSS data. It includes tasks such as parsing raw GNSS data, calculating the projection of GNSS points onto a moving plane, determining vehicle heading, and visualizing the GNSS data and its projection.

## Functions definition:

1. **Raw Data Parsing**: The code includes a `raw_data_parser` method that parses raw GNSS data from a text format and converts it into a list of lists. Each sub-list contains `time_s`, `x_mm`, `y_mm`, `roll_deg`, and `pitch_deg` values.

2. **Projection Calculation**: The `calculate_projection` method calculates the projection of GNSS data onto a 3D space. It takes the parsed GNSS data and an altitude value as input and returns a list of lists containing `time_s`, `x_proj_mm`, `y_proj_mm`, and `z_proj_mm`.

3. **Heading Calculation**: The `calculate_heading` method calculates vehicle headings based on GNSS data. It takes the parsed GNSS data and computes the headings in degrees.

4. **Visualization**:
   - `visualize_projection`: Creates a 3D scatter plot of GNSS data projections.
   - `visualize_headings`: Creates a 2D scatter plot of GNSS data points with headings drawn as red lines and optionally adds projected points as a red line.

## Usage

1. Define your raw GNSS data in the `raw_data` variable using the specified format.

2. Initialize an instance of the `Gnss_module` class.

3. Use the class methods to process and visualize your GNSS data as needed. The provided example code demonstrates how to parse the data, calculate projections, calculate headings, and visualize the results.
