# ClimateAndTemperatureAnalysis
Python and SQLAlchemy to analyse tempeture and climate
The data and csv files are in Resources folder
The output and any images from plotting will be in Output folder

## Climate Analysis file
This file will do the following:
  - query and analyse the last 12 months of precipitation data
  - query and analyse the last 12 months of temperature observation data (TOBS)
    
## API.py file
This file will do the following:
  - flask API for the queries developed
  - There are 5 routes total that shows the following:
    1. Precipitation data
    2. Stations data
    3. TOBS data
    4. Calculate min, max, ave for date provided
    5. Calculate min, max, ave for the period provided (start date to end date)

## Temperature Analysis 1 file
This file will do the following:
  - Analyse temperature for June and December 

## Temperature Analysis 2 file
This file will do the following:
  - Analyse prior years trends for the period desired (i.e. trip dates)
  - Calculate daily rainfall average
  - Calculate daily temperature normals  
