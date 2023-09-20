import numpy as np
import matplotlib.pyplot as plt


# Provided text data, Columns:
#time_s, x_mm, y_mm, roll_deg, pitch_deg
text_data = """
1621693264.0155628, 9521, -35074, 3.92, -1.35
1621693264.1979840, 9450, -34970, 3.93, -1.22
1621693264.4237902, 9365, -34853, 3.85, -1.24
1621693264.6384845, 9291, -34759, 3.85, -1.12
1621693264.8448036, 9211, -34649, 3.77, -0.99
1621693265.0378000, 9140, -34547, 3.70, -0.90
1621693265.2572992, 9071, -34444, 3.70, -0.70
1621693265.4631655, 8988, -34334, 3.59, -0.55
1621693265.6851535, 8917, -34231, 3.59, -0.49
1621693265.8768837, 8839, -34126, 3.56, -0.46
1621693266.1154845, 8767, -34021, 3.66, -0.38
1621693266.2963840, 8689, -33914, 3.78, -0.44
1621693266.5014370, 8614, -33808, 3.74, -0.53
1621693266.7386210, 8540, -33704, 3.73, -0.75
1621693266.9416296, 8452, -33590, 3.66, -0.91
1621693267.1762938, 8392, -33494, 3.55, -0.97
1621693267.3843954, 8326, -33399, 3.63, -1.00
1621693267.5642680, 8255, -33292, 3.77, -0.89
1621693267.7781956, 8176, -33189, 3.90, -1.00
1621693268.0044500, 8112, -33099, 3.88, -1.24
1621693268.2188272, 8044, -32986, 3.82, -1.58
1621693268.4177945, 7969, -32892, 3.75, -1.95
1621693268.6272150, 7906, -32804, 3.77, -2.05
1621693268.8552556, 7835, -32705, 3.80, -1.95
1621693269.0375066, 7759, -32616, 3.81, -1.72
1621693269.2567391, 7677, -32504, 3.88, -1.31
1621693269.4572983, 7593, -32391, 3.98, -1.04
1621693269.8621871, 7453, -32193, 4.07, -1.17
1621693270.0862586, 7386, -32103, 4.06, -1.31
1621693270.2752004, 7301, -31996, 4.06, -1.56
"""

#_________________________________________________ Data Preprocess _______________________________________________________________
# Split the text into lines
lines = text_data.strip().split('\n')
    
# Split each line by commas and convert to a list of lists
gnss_data = []
for line in lines:
    values = line.split(',')
    # Convert each value to float and create a sub-list
    float_values = [float(val.strip()) for val in values]
    gnss_data.append(float_values)
#_________________________________________________________________________________________________________________________________


# Constants
installation_height_mm = 1500  # Height of GNSS module above the moving plane in mm


#_________________________________________________ First Task ___________________________________________________________________
# Function to calculate the projection of GNSS module post on the moving plane
def calculate_projection(gnss_data):
    projections = []
    for time_s, x_mm, y_mm, roll_deg, pitch_deg in gnss_data:
        try:
            # Convert degrees to radians
            roll_rad = np.deg2rad(float(roll_deg))
            pitch_rad = np.deg2rad(float(pitch_deg))

            # Calculate projection using trigonometry
            projection_x = x_mm - installation_height_mm * np.tan(roll_rad)
            projection_y = y_mm - installation_height_mm * np.tan(pitch_rad)

            projections.append((time_s, projection_x, projection_y))
        except Exception as e:
            print(f"Error processing data point: {e}")

    return projections
#_________________________________________________________________________________________________________________________________



#_________________________________________________ Second Task _________________________________________________________________
# Function to calculate vehicle heading
def calculate_heading(gnss_data):
    headings = []
    for i in range(len(gnss_data) - 1):
        x1, y1 = gnss_data[i][1], gnss_data[i][2]
        x2, y2 = gnss_data[i + 1][1], gnss_data[i + 1][2]
        
        try:
            # Calculate heading using atan2
            heading_rad = np.arctan2(float(y2) - float(y1), float(x2) - float(x1))
            heading_deg = np.rad2deg(heading_rad)
        
            headings.append((gnss_data[i][0], heading_deg))
        except Exception as e:
            print(f"Error calculating heading: {e}")

    return headings
#_________________________________________________________________________________________________________________________________


# Calculate projections and headings
projections = calculate_projection(gnss_data)
headings = calculate_heading(gnss_data)


