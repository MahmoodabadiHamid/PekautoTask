import navpy as nv
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

class Gnss_module:
    
    @staticmethod
    def raw_data_parser(text_data):
        '''
            #_________________________________________________ Data Preprocess _______________________________________________________________
            This method will return a list of lists 
            each list contains time_s, x_mm, y_mm, roll_deg, pitch_deg
        '''
        lines = text_data.strip().split('\n')
        # Split each line by commas
        gnss_data = []
        for line in lines:
            values = line.split(',')
            # Convert each value to float and create a sub-list
            float_values = [float(val.strip()) for val in values]
            gnss_data.append(float_values)
        return gnss_data

    
    @staticmethod
    def calculate_projection(gnss_data, altitude):
        '''
            #_________________________________________________ First Task ___________________________________________________________________

            Calculates the projection of GNSS data onto a 3D space.

            Args:
                gnss_data (list): A list of lists containing GNSS data.
                altitude (float): Altitude in millimeters.

            Returns:
                list: A list of lists containing time_s, x_proj_mm, y_proj_mm, z_proj_mm.
        '''
        projections = []
        for time_s, x_mm, y_mm, roll_deg, pitch_deg in gnss_data:
            try:
                vec = [x_mm, y_mm, -altitude]
                roll_rad = np.radians(roll_deg)
                pitch_rad = np.radians(pitch_deg)

                rotation_matrix = np.array([
                [np.cos(pitch_rad), 0, -np.sin(pitch_rad)],
                [np.sin(pitch_rad)*np.sin(roll_rad), np.cos(roll_rad), np.cos(pitch_rad)*np.sin(roll_rad)],
                [np.sin(pitch_rad)*np.cos(roll_rad), -np.sin(roll_rad), np.cos(pitch_rad)*np.cos(roll_rad)]
                ])
                transformed_vector = list(np.dot(rotation_matrix, vec))
                projections.append([time_s] + transformed_vector)

            except Exception as e:
                print(f"Error processing data point: {e}")
                return False

        return projections


    @staticmethod
    def calculate_heading(gnss_data):
        '''
            #_________________________________________________ Second Task _________________________________________________________________
            Calculates vehicle heading based on GNSS data.

            Args:
                gnss_data (list): A list of lists containing GNSS data.

            Returns:
                list: A list of headings in degrees.
        '''
        headings = []
        try:
          # Extract x_mm and y_mm columns from the data
          x_mm = [row[1] for row in gnss_data]
          y_mm = [row[2] for row in gnss_data]

          # Calculate delta_xmm and delta_ymm
          delta_xmm = np.diff(x_mm)
          delta_ymm = np.diff(y_mm)

          # Calculate headings in degrees
          headings = np.arctan(delta_ymm/delta_xmm)*180/np.pi
          
        except Exception as e:
            print(f"Error calculating heading: {e}")
            return False
        return headings
    
    
    @staticmethod
    def visualize_projection(projections):
        '''
            #_________________________________________________ PROJECTION VISUALIZATION PART _________________________________________________________________
            Creates a 3D scatter plot of GNSS data projections.

            Args:
                projections (list): A list of lists containing time_s, x_proj_mm, y_proj_mm, z_proj_mm.
            
        '''
        # Extract the coordinates for plotting
        t = [point[0] for point in projections]
        x = [point[1] for point in projections]
        y = [point[2] for point in projections]
        z = [point[3] for point in projections]

        # Create a 3D scatter plot
        trace = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(size=5, color=z, colorscale='Viridis', opacity=0.8),
            text=t)

        layout = go.Layout(
            scene=dict(
                xaxis_title='X Coordinate',
                yaxis_title='Y Coordinate',
                zaxis_title='Z Coordinate',
                aspectmode="cube"),
            margin=dict(l=0, r=0, b=0, t=30),
            title_text="PekAuto Python Test Task (PROJECTION)"
        )
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(trace)
        fig.update_layout(layout)
        pyo.plot(fig, filename='PROJECTION_VISUALIZATION.html', auto_open=True)


    @staticmethod
    def visualize_headings(gnss_data, headings, projections=None):
        '''
        #_________________________________________________ HEADING VISUALIZATION PART _________________________________________________________________
        Creates a 2D scatter plot of GNSS data points with headings drawn as red lines and optionally adds projected points as a red line.

        Args:
            gnss_data (list): A list of lists containing GNSS data.
            headings (list): A list of headings in degrees.
            projections (list, optional): A list of projected points as [time_s, x_proj_mm, y_proj_mm, z_proj_mm]. Default is None.
        '''
        x_mm = [row[1] for row in gnss_data]
        y_mm = [row[2] for row in gnss_data]
        xy = np.array(list(zip(x_mm, y_mm)))

        # Create subplots with only one column (remove the first subplot)
        fig = make_subplots(rows=1, cols=1, subplot_titles=("Original Data with Heading Drawn On"))

        # Plot the result with little lines pointing in the heading
        trace3 = go.Scatter(x=xy[:, 0], y=xy[:, 1], mode='markers', marker=dict(color='blue', size=12), name='Given Points')
        fig.add_trace(trace3, row=1, col=1)

        vector_length = max(0.8, np.linalg.norm(xy[0] - xy[1])/1.5)
        show_legend = True
        for ind in range(len(xy) - 1):
            start_point = xy[ind]
            end_point = start_point + vector_length * np.array([np.cos(np.radians(headings[ind])), np.sin(np.radians(headings[ind]))])
            trace4 = go.Scatter(x=[start_point[0], end_point[0]], y=[start_point[1], end_point[1]], mode='lines+text',
                                line=dict(color='red', width=2), text=[f'Heading:{headings[ind]:.2f}°,'], textposition='bottom left', name='Heading', showlegend=show_legend)
            fig.add_trace(trace4, row=1, col=1)
            show_legend=False
       
        if projections is not None:
            # Extract projected coordinates
            x_proj = [point[1] for point in projections]
            y_proj = [point[2] for point in projections]
            z_proj = [point[3] for point in projections]
            
            # Add projected points as a red line
            trace5 = go.Scatter(x=x_proj, y=y_proj, mode='lines', line=dict(color='lightgreen', width=2), name='Projected Points')
            fig.add_trace(trace5, row=1, col=1)

        fig.update_xaxes(title_text="X Coordinate", row=1, col=1)
        fig.update_yaxes(title_text="Y Coordinate", row=1, col=1)

        fig.update_layout(title_text="PekAuto Python Test Task (HEADINGS)", showlegend=True, legend=dict(tracegroupgap=1))  # Set showlegend to True
        pyo.plot(fig, filename='HEADING_VISUALIZATION.html', auto_open=True)


    @staticmethod
    def visualize_pitch_and_roll(gnss_data):
        """
        Visualize the roll and pitch values over time from GNSS data.

        Args:
            gnss_data (list): A list of lists containing GNSS data.

        This function creates a plot with two subplots, one displaying the roll values and the other showing the pitch values
        over time. It provides insights into how the roll and pitch change throughout the time.

        Returns:
            None
        """
        time = [row[0] for row in gnss_data]
        roll = [row[3] for row in gnss_data]
        pitch = [row[4] for row in gnss_data]

        trace_roll = go.Scatter(x=time, y=roll, mode='lines', line=dict(color='green', width=2), name='Roll')
        trace_pitch = go.Scatter(x=time, y=pitch, mode='lines', line=dict(color='blue', width=2), name='Pitch')
        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(trace_roll, row=1, col=1)
        fig.add_trace(trace_pitch, row=2, col=1)

        fig.update_yaxes(title_text="Roll Valus", row=1, col=1)
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Pitch Valus", row=2, col=1)

        fig.update_layout(title_text="Pitch and Roll Values", showlegend=True)  # Set showlegend to True
        pyo.plot(fig, filename='pitch_and_roll_VISUALIZATION.html', auto_open=True)



