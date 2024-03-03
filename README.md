# sqlalchemy-challenge
Climate Data Analysis and Climate App Design
This repository contains code and documentation for analyzing climate data from Hawaii and designing a Flask-based API for accessing the analysis results.

Part 1: Analyze and Explore the Climate Data
Precipitation Analysis
The precipitation_analysis.ipynb notebook contains Python code for analyzing precipitation data from Hawaii. The analysis includes calculating the total precipitation over a specific period and visualizing the precipitation trends over time.

Station Analysis
The station_analysis.ipynb notebook explores the weather stations available in the dataset. It identifies the most active weather station and provides insights into its temperature observations.

Part 2: Design Your Climate App
Flask API
The app.py file contains the Flask application code that serves as the backend for the Climate Analysis API. The API provides endpoints for accessing precipitation data, station information, temperature observations, and temperature statistics for specified date ranges.

Available Endpoints:
/api/v1.0/precipitation: Returns precipitation data for the last 12 months.
/api/v1.0/stations: Returns a list of weather stations.
/api/v1.0/tobs: Returns temperature observations for the last 12 months.
/api/v1.0/<start_date>: Returns temperature statistics (TMIN, TAVG, TMAX) for dates greater than or equal to the start date.
/api/v1.0/<start_date>/<end_date>: Returns temperature statistics for dates between the start and end dates inclusive.