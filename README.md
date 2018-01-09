## Motivation
![alt text][logo]

[logo]: https://github.com/lifeisapomdp/bikeshare-prediction/images/Citi_Bike_logo.jpg "Citi Bike"

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Bike Share systems are becoming increasingly popular in urban areas. With growing membership and expansion of service comes many operational challenges. A major challenge in their operations is the unbalanced demand and supply at bike stations as a function of time and location. The most obvious example is that working districts have high supply during morning peak hours and high demand during evening peak hours. 

Most bike share systems employ active rebalancing to ease the pressure at peak times. This means transporting a certain number of bikes from inactive stations to more active stations, or between stations and storage, in order to maximize the usage of each bike and ease supply and demand inbalance problems across bike stations at different times.

A quantitative, predictive model for the demand and supply at bike stations would help operators plan bike transports more efficiently. This project aims to build such a model for bike arrivals at each station within one-hour time intervals, as a function of the following parameters:

• time of day, divided into 24 one-hour intervals

• whether a day is a work day or weekend/federal holiday

• hourly temperature

• hourly precipitation intensity

The output of our model will be the number of bikes departing from a station within the one-hour time interval.

## Initial data processing

Requires: clean_citi_monthly_data.ipynb, monthly data. 

Monthly data can be downloaded directly from Citi Bike's [website](https://www.citibikenyc.com/system-data), which is then passed through the  clean_citi_monthly_data.ipynb file for initial processing. 

## Binning and merging processed data

Requires: demand_merge.ipynb, processed monthly data.

In order to perform regression on the demand and supply bikes, we discrete each day into 24 one-hour intervals, count the number of bikes departing from each station in each time interval, fill in observations where the count is zero (since they are not reflected in the original data). Then we determine whether each date is a work day, i.e. not weekend or federal holiday. These are done by passing processed data through the demand_merge.ipynb file. 

## Scraping hourly weather data

See Figure [fig:weather] for a snippet of scraped weather data, which is stored in a PostgreSQL database. 

## Adding hourly weather data 

Requires: demand_add_weather.ipynb, binned and merged data. 

Finally, we associate weather data to each date and time bucket. Hourly weather data is obtained from [Dark Sky](https://darksky.net), using a python scraper modified from code provided on the Github page of the bikeshare prediction project by [Data Science for Social Good](https://github.com/dssg/bikeshare). 

## Final data used for prediction training and testing

The final dataset consists of ~1.3 million observations, which we split into 70% training set, 20% validation set, and 10% test set. We also performed data normalization and found that this procedure improved predictions slightly.

A snippet of the processed data for demand prediction is shown in Figure [fig:Processed-data-for], where the column “Count” is the number of bikes departing from a station in a specific time bucket. This data is then fed into various regression and classification models for training, evaluation, and prediction. We also normalized each feature, as well as divided the “Count” column by 10. For classification, we grouped the counts to intervals of length 4, for a total of 9 categories, where the last category is any number that is larger than 30. 
