# @API Authentication
"""
* Authentication ourselves --> access more secure and more valuable data
* from the API providers.

# other valuable data for example is weather data - paid = selling data (good maintenance)
# why do people charge for APIs - how you get the data? - wetter stations, employees, data science (resource intensive)

@ How do you prevent people from abusing this free tier?
--> Different ways that you can authenticate yourself with them
* API Key --> like your personal account number and password
    Way how the API provider can track how much you're using their API and to authorize your access and deny you
    access once you've gone over the limit
"""

import os

# ----------------- USING API KEYS TO AUTHENTICATE AND GET THE WEATHER FROM @OPENWEATHERAPP ----------------- #
# * really import to read the instructions menu
import requests
from twilio.http.http_client import TwilioHttpClient
from twilio.rest import Client

# @os module in python provides functions for interacting with the operating system

# HOW TO GET TWILIO TO WORK ON FREE ACCOUNTS WITH THE PROXY (fixing requests ConnectionError in HTTPSConnectionPool)
# About what is a proxy
"""
The twilio api basically needs to be told how to connect to the proxy servers that free accounts use. 
When paid  account on python anywhere, you have an actual address to your dedicated server 

# what is a proxy server? 
The main tasks of a proxy server are veiling (verschleiern), securing and accelerating of data transmissions between 
local client and webserver 
Request to server (server gets ip address of proxy --> often they have a cache where they store last loaded data)

# basically proxy (vertretung) is a intermediary (vermittler) in a network, who can receive requests and forward 
"""

# Environment Variables - env
"""
Environment variables have values which are strings (paths) which can be used in our applications 
or our code 

TWO MAJOR USE CASES 
1. convenience --> when you deploy large application the process is quite complicated.
    --> update code without messing around with the code base  
    !-- you want to access particular folder often --> simplifying the access 
* If you had an application that was sending you emails out to your clients, then your client ase emails 
    --> might change day to day. So certain variables that are being used in you code base could be set as 
    environment variables (they are depended of current circumstances) and you can modify those variables 
    without having to touch the code. 

2. Security --> developing software: uploading code base  (not good to have auth key or api keys stored in the same 
    --> place of your code 
    !-- That's where environment variables come in (allow us to separate out where we store our keys, our secret stuf, 
        and various other variables away form were our code base is located 
        
# how to create a environment variable 
'export nameVariable=value'

if hit "env" again we can see the updated environment
**** to get this env variable with python import os 
os.environ.get("envVarName")

TO EVENTUALLY RUN THE CODE  
# we need to provide the program the envionvariables 
so export EnvVariable=Value; another EnvVariable;
"""

# instruction how to connect to proxy
proxy_client = TwilioHttpClient()
# environ in python is a mapping object that represents the users environmental variables
# it returns a dictionary having users env variable as key and their values as value.
proxy_client.session.proxies = {'https': os.environ["https_proxy"]}

# ---------------- PROVIDE DATA ------------------
# it is up to everything but not including question mark
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
MY_API_KEY = "API KEY"
CITY = "Berlin"
MY_LATITUDE = 0.5
MY_LONGITUDE = 0.5


weather_params = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "appid": MY_API_KEY,
    # this should speed up the api fetching process and it also means --> transferring less data acorss the internet
    "exclude": "current,minutely,daily"
    # exclude parameters in comma separated --> exclude some parts of the weather data from the api response
}
# params everything after question mark of the api endpoint example
response = requests.get(url=OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
if response.status_code == 200:
    weather_data = response.json()
    # it iterates through the next 12 hours
    # we could also use the slice function which would be :
    """
    slice_object = slice(slice_count)
    weather_data["hourly"][slice_object]
    """
    will_rain = False
    # the last num (13) will not be included,
    # so we have 0 the current weather id to +12 hours weather id
    for hour in weather_data["hourly"][:13]:
        # we go into hourly weather and check if first state id is smaller 700
        if hour["weather"][0]["id"] < 700:
            will_rain = True
            # leave the for loop
            break
    if will_rain:
        # ----------------------------- SENDING SMS VIA THE TWILIO API  ----------------------------- #
        """
        @ Twilio - trial money 
        Twilio is an API service that allows us to send text messages or phone calls or have a virtual 
        phone number in any country 
        """
        # twilio SMS python quickstart - @https://www.twilio.com/docs/sms/quickstart/python
        # we need to copy our account_sid and auth token from twilio.com/console
        # sid = security identifier --> session identifier   - identification for my Twilio account
        ACCOUNT_SID = "SID"
        AUTH_TOKEN = "TOKEN"

        # set up Twilio client using our account sid and auth token
        client = Client(ACCOUNT_SID, AUTH_TOKEN, http_client=proxy_client)
        message = client.messages \
            .create(
                body="It is going to rain today. Remember to bring an ☂️!",
                # it is my free twilio trial phone number
                from_="+NUMBER",
                # any number that you see hre under verified caller IDs can be used in your code
                to="+NUMBER"
            )
        # just to make sure that it was actually sent successfully
        # queued = Warteschlange
        print(message.status)
    # we could obtain a weather id --> it is an identifier for the current weather state like html web codes
    # as a rule everything below  id 700 --> we need umbrella else not

    # the script runs at 7am and 7pm, so we only need the first (0th) dict and the 12th

# time stamp format MM/dd/yyyy HH:mm:ss ZZZZ - digital record of the time of occurrence of a particular event
