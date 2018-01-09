import os
import json
import urllib.request, urllib.error, urllib.parse
import time
import datetime
from forecastio import forecastio 
import psycopg2
import sys

city_lat  = 40.7830
city_long = -73.9712

try:
  #conn = psycopg2.connect("dbname="+os.environ.get('dbname')+" user="+os.environ.get('dbuser')+ " host="+os.environ.get('dburl'))
  conn = psycopg2.connect(dbname=DBNAME,user=USER,password=PASSWORD)
except:
  print("I am unable to connect to the database")
  exit()
cur = conn.cursor()

#Casts float from string when there is the posbility of the empty string

forecast = forecastio.Forecastio(API_KEY)
result = forecast.load_forecast(city_lat,city_long)

start_date = datetime.datetime(2017,6,1)
end_date = datetime.datetime(2017,9,1)
d = start_date
delta = datetime.timedelta(hours=1)

while d < end_date:
    result = forecast.load_forecast(city_lat,city_long,d,lazy=True)
    current = forecast.get_currently()
    days_list = []
    item = current
    time = item.time
    summary = item.summary
    precip_intensity = item.precipIntensity
    precip_probility = item.precipProbability
    precip_accumulation = item.precipAccumulation
    temperature = item.temperature
    if (time is not None):
      try:
        cur.execute("""INSERT INTO weather_newyork (time,summary,precipIntensity,precipProbability,precipAccumulation,temperature) VALUES
            (%s,%s,%s,%s,%s,%s);""",
            (time,summary,precip_intensity,precip_probility,precip_accumulation,temperature))
        conn.commit()
      except:
        print(d)
        print("Unexpected error:", sys.exc_info()[0])
        pass
    d += delta

conn.commit()

