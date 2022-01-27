import requests,json
import time
import pandas as pd
import matplotlib.pyplot as plt
import concurrent.futures
#Source Api Key and Link
api_Key = 'c371bc94535edb7b97d3e780730385a9'
api_source_link = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'


#Collects Lonitude and Latitude when called and puts them into source api link
random_loc={'south Atl ocean1':'-24.258539760887345,-13.243488310343544',
'south Atl ocean2':'-39.953169013739085,1.346355364604682',
'south Atl ocean3':'-36.502179158686296,-47.257160010373454',
'indian ocean1':'-24.098179018872067,79.48112058767079',
'indian ocean2':'-8.89761511073609,76.93229247578228',
'indian ocean3':'-22.402452000446264,58.56315194527515',
'philippine sea1':'17.75752114788641,131.68815198099261',
'philippine sea2':'27.94437534280473,135.64323008564722',
'north pacific ocean1':'28.56372335160739,-170.65559831559756',
'north pacific ocean2':'13.184803191372147,168.95377678929412',
'north pacific ocean3':'9.393184253264065,-170.12825456831024',
 'mediterranean sea1':'34.62276049908181,18.485027126122898',
'mediterranean sea2':'33.45751601690501,28.76823019822496',
'mediterranean sea3':'35.342860167268576, 12.42057403231911',
'north atl ocean1':'36.340300841205305,-50.069660492332645',
'north atl ocean2':'52.394671901580836,-32.13997308456492',
'north atl ocean3':'55.045929113783345, -48.136066752279255'}
t1 = time.perf_counter()
def checkWeather(longitude,latitude):
    api_link= api_source_link.format(lat = latitude, lon = longitude,API_key = api_Key)
    r = requests.get(api_link)
    if r.status_code == 200:
        # getting data in the json format
        data = r.json()
        #getting city name and timezone
        name = data['name']
        time_zone = data["timezone"]
        main = data['main']
        # getting temperature
        global temperature 
        temperature = main['temp']
        # getting the humidity
        global humidity 
        humidity = main['humidity']
        # getting the pressure
        global pressure 
        pressure = main['pressure']
        # weather report
        report = data['weather']
        current_time = time.ctime()
        #print(current_time)
        #print(f'Name: {name}')
        #print(f"Timezon: {time_zone}")
        #print(f"Long: {longitude},Lat={latitude}")
        #print(f"Temperature: {temperature}")
        #print(f"Humidity: {humidity}")
        #print(f"Pressure: {pressure}")
        #print(f"Weather Report: {report[0]['description']}")
        #print('\n')
        return temperature, humidity, pressure
    elif r.status_code == 400:
        # showing type of error message
        print("Error in the HTTP request/ client errors")
    elif r.status_code == 500:
        # showing type of error message
        print('Error in the HTTP request/server errors')
       
    else:
        print('Some type error')
    
#parses through the dictionary and takes long and lat
data_dict = {}
data_list = []
key_list = []
temperature_list = []
humidity_list =[]
pressure_list = []

#using threadig
def threading(key,values):
    #print(key)
    x,y = value.split(',')
    checkWeather(x,y)
#creates a dictionary which has all the values in a list
    key_list.append(key)
    temperature_list.append(temperature)
    humidity_list.append(humidity)
    pressure_list.append(pressure)
    data_dict.update({'key':key_list ,
                      'temperature':temperature_list ,
                      'humidity':humidity_list ,
                      'pressure':pressure_list})
    data_list.append({key:[temperature, humidity, pressure]})

with concurrent.futures.ThreadPoolExecutor() as executor:
    for key,value in random_loc.items():
        f1 = executor.submit(threading, key,value)
t2 = time.perf_counter()
#print (data_dict)

#print(data_list)
#print(data_dict)
print(f"The time it took is: {t2 - t1}")
df = pd.DataFrame(data_dict)
pd_list_df = pd.DataFrame(data_dict)
print(df.head(10))
df.plot(x= 'key' , y= 'humidity', kind= 'bar')
