import tkinter as tk
import requests
import time
import sqlite3
from datetime import datetime

def getWeather(event=None):
    city = textfield.get()
    api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=644b916cd16e80575b3c2b3c3bff751e"
    json_data = requests.get(api).json()
    
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunset'] - 21600))
    
    final_info = condition + "\n" + str(temp) + "°C"
    final_data = "\n" + "Min Temp: " + str(min_temp) + "°C" + "\n" + "Max Temp: " + str(max_temp) + "°C" + "\n" + "Pressure: " + str(pressure) + "\n" + "Humidity: " + str(humidity) + "\n" + "Wind Speed: " + str(wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset
    
    label1.config(text=final_info)
    label2.config(text=final_data)
    
    # Store data in SQLite database
    store_weather_data(city, condition, temp, min_temp, max_temp, pressure, humidity, wind, sunrise, sunset)

def store_weather_data(city, condition, temp, min_temp, max_temp, pressure, humidity, wind, sunrise, sunset):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS weather (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 city TEXT,
                 condition TEXT,
                 temp REAL,
                 min_temp REAL,
                 max_temp REAL,
                 pressure INTEGER,
                 humidity INTEGER,
                 wind REAL,
                 sunrise TEXT,
                 sunset TEXT,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Insert weather data
    c.execute('''INSERT INTO weather (city, condition, temp, min_temp, max_temp, pressure, humidity, wind, sunrise, sunset)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (city, condition, temp, min_temp, max_temp, pressure, humidity, wind, sunrise, sunset))
    
    conn.commit()
    conn.close()

# GUI setup
canvas = tk.Tk()
canvas.geometry("600x500")
canvas.title("Weather App")
f = ("poppins", 15, "bold")
t = ("poppins", 35, "bold")

textfield = tk.Entry(canvas, font=t)
textfield.pack(pady=20)
textfield.focus()
textfield.bind("<Return>", getWeather)

label1 = tk.Label(canvas, font=t)
label1.pack()
label2 = tk.Label(canvas, font=f)
label2.pack()

canvas.mainloop()
