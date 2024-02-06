# Working with APIs

  This guide is a walk-through on using the requests library to get data from a API. The guide will handle the basics of setting up a script to fetch data and some data manipulation.

For this example we're going to use yr.no as an example since it is a public API providing weather forecasts globally. API documentation: https://api.met.no/weatherapi/locationforecast/2.0/documentation

Requests is an excellent library that is part of the standard distribution of Python. See https://requests.readthedocs.io/en/latest/ for more documentation of requests.

The input we need is the latitude and longitude (you can find the latitude/longitude from google maps, just right click on a place and copy the coordinates) for me that is -37.81002731164721, 144.96436660091567 (right in front of the Redmond Barry statue in the State Library Forecourt in Melbourne, Australia)

## The basics

Lets make a short script that sets out the basics:

```  
#!/usr/bin/env python3
import  requests

url  =  'https://api.met.no/weatherapi/locationforecast/2.0/compact'

headers  = {}
headers['User-Agent'] =  'Testing out forecasting API'

params  = {}
params['lat'] =  -37.81002731164721
params['lon'] =  144.96436660091567

response  =  requests.get(url, headers=headers, params=params)
print(response.json())
print(f"\nUrl is {response.url}")
```

This little snippet of code sets out some of the basics for communicating with APIs. We've set up two dictionaries (denoted by {}), these are simple key-value store, you save a value for a specific key, in this case 144.96436660091567 for the key 'lon'.

These dictionaries are then used as input, together with the base url, to the requests library and we save the resulting object we got from that query into a variable called 'response'.  
 
 If you run this as a one time script in regular python you will run the same query every time you run the script. If you have set up an ipython interpreter you can save the output and start exploring the contents of the response variable by writing 'response.' and hitting the tab-key. 

## Manipulating json output 

The output is a json-data structure consisting of dictionaries and lists. It can be a bit hard to read but what we want is the keys "properties"/"timeseries" and the first dictionary in that list.

```
print(response.json()['properties']['timeseries'][0])
```
 
To make it a bit simpler to work with we can assign that dictionary to a local variable.

```
forecast  =  response.json()['properties']['timeseries'][0]
```

### Time
Now we have a variable called forecast with the most up to date forecast data. One of the things we notice pretty quickly is that the time in the API is based on UTC, and we would like to convert it to our local timezone.

There are multiple ways of doing this for example you can use the built-in datetime library, but the problem with that library is that it is a bit convoluted to work with, so we are going to use pip to install a new library to our python environment. Pendulum is a nice addition to any python environment to make it easier to work with dates. See https://pendulum.eustace.io/docs/ for more information and documentation.

```
import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pendulum'])
```
You only need to run this line once to install the library. If for some reason the library fails to install you can safely skip the next steps.

```
import pendulum

time  = pendulum.parse(forecast['time'])

localtime  =  time.in_timezone('Australia/Melbourne') # You can change this to your local timezone see 'TZ identifier' here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

print(localtime)
```
This bit of code takes the value from 'time' in the forecast variable we saved earlier and converts it from UTC-time to my local time.

### Temperature

 The temperature we get from yr is given in Celsius, but for our American friends we might want to convert it to Fahrenheit. According to google, the formula for converting Celsius to Fahrenheit is (20°C × 9/5) + 32 = 68°F, we can recreate that function in python.
```
celsius  =  forecast['data']['instant']['details']['air_temperature']

farenheit  = (celsius  *  9/5) +  32

print(farenheit)
```
  

A problem we might run into here is that there is simply too many decimals and we would like to round then off to two decimals:

```
print(round(farenheit, 2))
```
  
### Finished product
we can put all of this together in one print statement

 ```
print(f"At {localtime.format('dddd Do [of] MMMM YYYY h:mm A')} it was {celsius} degrees celsius (that's {round(farenheit, 2)} degrees farenheit)")
```
  
This has been a small example of what you can do with APIs in Python. It gets really interesting once you start using a identifier from one API to look up information in a different API to get information.

There are also different methods we haven't touched on, for example using 'put', 'post' and 'delete' which can set off different actions.
