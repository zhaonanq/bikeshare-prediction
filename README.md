## Motivation

<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/Citi_Bike_logo.jpg" width="150">

Bike share systems are becoming increasingly popular in urban areas. With growing membership and expansion of service comes many operational challenges. A major challenge in their operations is the unbalanced demand and supply at bike stations as a function of time and location. The most obvious example is that working districts have high supply during morning peak hours and high demand during evening peak hours. 

Most bike share systems employ active rebalancing to ease the pressure at peak times. This means transporting a certain number of bikes from inactive stations to more active stations, or between stations and storage, in order to maximize the usage of each bike and ease supply and demand inbalance problems across bike stations at different times.

A quantitative, predictive model for the demand and supply at bike stations would help operators plan bike transports more efficiently. This project aims to build such a model for bike arrivals at each station within one-hour time intervals, as a function of the following parameters:

• time of day, divided into 24 one-hour intervals

• whether a day is a work day or weekend/federal holiday

• hourly temperature

• hourly precipitation intensity

The output of our model will be the number of bikes departing from a station within the one-hour time interval. 

## Initial data processing

Requires: [clean_citi_monthly_data.ipynb](https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/clean_citi_monthly_data.ipynb), monthly data from Citi Bike.

Monthly data can be downloaded directly from Citi Bike's [website](https://www.citibikenyc.com/system-data), which is then passed through the  clean_citi_monthly_data.ipynb file for initial processing. This includes...

## Binning and merging processed data

Requires: [demand_merge.ipynb](https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/demand%20prediction/demand_merge.ipynb), processed monthly data.

In order to perform regression on the demand and supply of bikes, we discretize each day into 24 one-hour intervals and count the number of bikes departing from a station in each time interval. We also fill in observations where the count is zero, since they are not reflected explicitly in the original data. Then we determine whether each date is a work day, i.e. not weekend or federal holiday. These are done by passing the initially processed data through the demand_merge.ipynb file. 

## Scraping hourly weather data

See below for a snippet of the scraped weather data, which is stored in a PostgreSQL database. 

<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/weather_snippet.PNG" class="centerImage" width="300">

## Adding hourly weather data 

Requires: demand_add_weather.ipynb, binned and merged data. 

Finally, we associate weather data to each date and time bucket. Hourly weather data is obtained from [Dark Sky](https://darksky.net), using a python scraper modified from code provided on the Github page of the bikeshare prediction project by [Data Science for Social Good](https://github.com/dssg/bikeshare). 

## Final data used for prediction training and testing

The final dataset consists of ~1.3 million observations, which we split into 70% training set, 20% validation set, and 10% test set. We also performed data normalization and found that this procedure improved predictions slightly.

A snippet of the processed data for demand prediction is shown in Figure [fig:Processed-data-for], where the column “Count” is the number of bikes departing from a station in a specific time bucket. This data is then fed into various regression and classification models for training, evaluation, and prediction. We also normalized each feature, as well as divided the “Count” column by 10. For classification, we grouped the counts to intervals of length 4, for a total of 9 categories, where the last category is any number that is larger than 30. 
