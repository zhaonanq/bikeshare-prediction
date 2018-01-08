## Motivation

Bike Share systems are becoming increasingly popular in urban areas. With growing membership and expansion of service comes many operational challenges. A major challenge in their operations is the unbalanced demand and supply at bike stations as a function of time and location. The most obvious example is that working districts have high supply during morning peak hours and high demand during evening peak hours. 

Most bike share systems employ active rebalancing to ease the pressure at peak times. This means transporting a certain number of bikes from inactive stations to more active stations, or between stations and storage, in order to maximize the usage of each bike and ease supply and demand inbalance problems across bike stations at different times.

A quantitative, predictive model for the demand and supply at bike stations would help operators plan bike transports more efficiently. This project aims to build such a model for bike arrivals at each station within one-hour time intervals, as a function of the following parameters:

• time of day, divided into 24 one-hour intervals

• whether a day is a work day or weekend/federal holiday

• hourly temperature

• hourly precipitation intensity

The output of our model will be the number of bikes departing from a station within the one-hour time interval.

## Data Processing

Data can be downloaded directly from Citi Bike's website: https://www.citibikenyc.com/system-data, which is then passed through the  clean_citi_monthly_data.ipynb file for initial processing. 
