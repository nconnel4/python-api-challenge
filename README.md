# python-api-challenge
 
## Purpose
The purpose of this project was to use Python API's for Open Weather and Google to pull location data for 500+ random locations. Weather data was pulled from Open Weather API and imported into pandas to analyze the relationship of latitude versus temperature, humidity, cloudiness, and wind speed. Results were recorded in the WeatherPy jupyter notebook. The second part of the project used Google's Map API to create a heatmap of the humidity collected from Open Weather API. Google's Places API was used to find a hotel closest to the cities that would be ideal for vacation based on the following criteria:
1) Temperature between 70 and 80 degrees Fahrenheit
2) Humidity < 50%
3) Wind Speed < 10 mph
4) Cloud Cover < 25%

These locations were plotted using markers on the map shown in VacationPy jupyter notebook.
