## Motivation

<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/Citi_Bike_logo.jpg" width="150">

Bike share systems are becoming increasingly popular in urban areas. With growing membership and expansion of service comes many operational challenges. A major challenge in their operations is the unbalanced demand and supply at bike stations as a function of time and location. The most obvious example is that working districts have high supply during morning peak hours and high demand during evening peak hours. 

Most bike share systems employ active rebalancing to ease the pressure at peak times. This means transporting a certain number of bikes from inactive stations to more active stations, or between stations and storage, in order to maximize the usage of each bike and ease supply and demand inbalance problems across bike stations at different times.

A quantitative, predictive model for the demand and supply at bike stations would help operators plan bike transports more efficiently. This project aims to build such a model for bike arrivals at each station within one-hour time intervals, as a function of the following parameters:

• latitude and longitude of the bike station

• time of day, divided into 24 one-hour intervals

• whether a day is a work day or weekend/federal holiday

• hourly temperature

• hourly precipitation intensity

The output of our model will be the number of bikes departing from a station within the one-hour time interval. 

## Initial data processing

Requires: [clean_citi_monthly_data.ipynb](https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/clean_citi_monthly_data.ipynb), monthly data from Citi Bike.

Monthly data can be downloaded directly from Citi Bike's [website](https://www.citibikenyc.com/system-data), a snippet of which is shown below.
<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/snippet%20of%20original%20data.JPG" class="centerImage">

It is then passed through the clean_citi_monthly_data.ipynb file for initial processing. This includes:

• discard trips shorter than 60 seconds and longer than an hour, which likely result from riders' failing to dock properly

• discard trips taken by day-pass holders(labeled "customers" in the dataset) rather than subscribers, since day-pass holder rides are much less predictable

• discard those trip that are taken by Citi Bike crew on rebalancing trips, as they do not reflect actual usage

• separate date and time, and convert time into 24 one-hour time buckets

• determine if a date is work day, i.e. not weekend or a federal holiday;assign binary variable 0 if it is a work day and 1 otherwise

## Binning and merging processed data

Requires: [demand_merge.ipynb](https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/demand%20prediction/demand_merge.ipynb), processed monthly data.

In order to perform regression on the demand (or supply) of bikes, we discretize each day into 24 one-hour intervals and count the number of bikes departing from (or arriving at) a station in each time interval. We also fill in observations where the count is zero, since they are not reflected explicitly in the original data. Note that before binning, we also need to discard irrelevant features such as trip duration and gender and age of riders. Finally we merge all observations into a single file. These are done by passing the initially processed data through the demand_merge.ipynb file. 

## Scraping hourly weather data
<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/dark_sky_logo.png" class="centerImage" width="200">

Hourly weather data is obtained from [Dark Sky](https://darksky.net), using a Python [scraper](https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/weather/historical_newyork.py) modified from code provided on the Github page of the bikeshare prediction project by [Data Science for Social Good](https://github.com/dssg/bikeshare), which in turn relies on this Python [wrapper](https://github.com/ZeevG/python-forecast.io) of the Dark Sky API. In order to scrape and store the hourly data, follow the instructions given below for storing data on local Windows machine. Caution: the procedure is slightly different for virtual machine or Unix-like machines.

In order to scrape and store the hourly data, first install PostgreSQL and in Windows command line type,
```
psql -U postgres
```
and enter the password you were asked to create during installation. You are now in the PostgreSQL environment. Now create a PostgreSQL database by typing 
```
CREATE DATABASE database_name;
```
Next, create a table where the weather data will be stored by exiting from PostgreSQL first with `\q`, navigating to the directory where the [weather_newyork.sql](https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/weather/weather_newyork.sql) file is, and typing
```
psql -U postgres -d database_name -f weather_newyork.sql
```
If prompted, enter your password again. 

Now we can run the scraper historical_newyork.py to load historical hourly weather into the database. Note that in that file, which contains the line
```
conn = psycopg2.connect("dbname="+os.environ.get('dbname')+" user="+os.environ.get('dbuser')+ " host="+os.environ.get('dburl'))
```
you will need to specify the value of the environmental variable 'dbname', which should be the same as database_name, and value of 'dbuser', which is 'postgres' in our case. You don't need to specify host if the database is on your local machine;otherwise, the value of 'dburl' should be the address of the virtual machine. 
Finally, you will need to supply a Dark Sky API key in the line 
`forecast = forecastio.Forecastio(API_KEY)` 
which can be obtained by setting up an account at Dark Sky. 

Also discuss difference between virtual and local machine. 


See below for a snippet of the scraped weather data, which is stored in a PostgreSQL database. 

<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/weather_snippet.PNG" class="centerImage">

## Adding hourly weather data 

Requires: demand_add_weather.ipynb, binned and merged data. 

Finally, we associate weather data to each date and time bucket.  

## Final data used for prediction training and testing

The final dataset consists of ~1.3 million observations, which we split into 70% training set, 20% validation set, and 10% test set. We also performed data normalization and found that this procedure slightly improved predictions.

A snippet of the processed data for demand prediction is shown below. 

<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/snippet%20of%20processed%20data.PNG" class="centerImage">

Here the column “Count” is the number of bikes departing from a station in a specific time bucket. This data is then fed into various regression and classification models for training, evaluation, and prediction. For classification, we grouped the counts to intervals of length 4, for a total of 9 categories, where the last category is any number that is larger than 31. 

We see from the snippet above that there is intrinsic noise in the dataset: even given similar weather conditions, the count for the above station (with latitude 40.73221853 and longitude -73.98165557) in time bucket 0 could have a demand ranging between 0 and 4. As we will later see, 4 is also where the RMSE of the validation set for our regression algorithm lies, and our classification algorithm with categories of length 4 can achieve near perfect accuracy on the validation set.   

## Regression with neural network

<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/Tensorflow_logo.png" class="centerImage" width="100">

Details to come... For now, please refer to the final project report file in this repo.

## Classification with neural network

<img src="https://github.com/lifeisapomdp/bikeshare-prediction/blob/master/images/Tensorflow_logo.png" class="centerImage" width="100">

Details to come... For now, please refer to the final project report file in this repo.
