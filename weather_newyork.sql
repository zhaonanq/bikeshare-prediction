/* Run this PostgreSQL script to retrieve historical weather data for New York.*/

SET timezone TO "+00:00";     

CREATE TABLE IF NOT EXISTS weather_newyork (
  time timestamp NOT NULL PRIMARY KEY,
  summary text,
  precipIntensity double precision,
  precipProbability double precision,
  precipAccumulation double precision,
  temperature double precision
);
