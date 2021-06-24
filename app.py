# for reading json format
import json
# for randomize the clothing suggestion
import random
# for quiting the program
import sys
# for grabbing data from the URL
import urllib.request
# for read the config file
import configparser
# for checking the file existence
from os import path
# for plotting the graph
import matplotlib.pyplot as plt


# function: allow user select a place
def input_place():
    # print all the places with index
    for i in range(len(places)):
        print(i+1, ":", places[i])
    input_valid = False
    while not input_valid:
        try:
            place_index = input("What is your location? (Enter the index of the place that shown above):")
            if 0 < int( place_index) <= len(places):
                input_valid = True
            else:
                print("Error input! Answer should between 0 to ", len(places), " Please input again.\n")
        except ValueError:
            print("Error input! Answer should be a integer. Please input again.\n")
    return places[int(place_index)-1]


# function: transfer weather icon code to weather status
def num_to_status(num):
    numbers = {
        50: "Sunny", 51: "Sunny Periods", 52: "Sunny Intervals",
        53: "Sunny Periods with A Few Showers", 54: "Sunny Intervals with Showers",
        60: "Cloudy", 61: "Overcast", 62: "Light Rain", 63: "Rain",
        64: "Heavy Rain", 65: "Thunderstorms",
        70: "Fine", 71: "Fine", 72: "Fine", 73: "Fine", 74: "Fine", 75: "Fine",
        76: "Mainly Cloudy", 77: "Mainly Fine",
        80: "Windy", 81: "Dry", 82: "Humid", 83: "Fog", 84: "Mist", 85: "Haze",
        90: "Hot", 91: "Warm", 92: "Cool",  93: "Cold"
    }
    return numbers.get(num, None)


# function: get the temperature according to user location
def get_temp(location):
    for w_obj in weatherObj['temperature']['data']:
        if w_obj['place'] == location:
            temp = w_obj['value']
    print("The current temperature in", location, "is", temp, "°C.")
    return temp


# function: analysis the temperature for user location and give suggestion
def temp_analysis(location):
    for w_obj in weatherObj['temperature']['data']:
        if w_obj['place'] == location:
            current_temp = w_obj['value']
    print("The current temperature in", location, "is", current_temp, "°C.")
    global suggestion
    if current_temp > 33:
        suggestion += "It is very hot right now, remember to drink plenty of water and avoid over exertion during " \
                      "outdoor work or activities.\n"
        suggestion += "Also you should keep windows open when you are staying indoors without air-conditioning to " \
                      "ensure that there is adequate ventilation.\n] "
    elif current_temp > 23:
        suggestion += "It is a bit warm right now, remember to drink more water.\n"
    elif current_temp > 13:
        suggestion += "It is a bit cold right now, remember to wear more cloth to keep yourself warm.\n"
    else:
        suggestion += "It is very cold right now, remember to put on warm clothes and to avoid adverse health effects " \
                      "due to the cold weather.\n "
        suggestion += "You must also ensure adequate indoor ventilation.\n"


# function: analysis the current weather and give suggestion
def weather_analysis():
    sunny = [50, 51, 52]
    rain = [53, 54, 62, 63, 64, 65]
    cloudy = [60, 61, 76, 77]
    fine = [70, 71, 72, 73, 74, 75]
    for obj_weather in weatherObj['icon']:
        weather_index = obj_weather
        weather_status = num_to_status(obj_weather)
    print("The weather now is", weather_status + ".")

    global suggestion
    if weather_index in rain:
        suggestion += "It is rain now, remember to bring an umbrella if you decide to go outside or avoid " \
                      "outdoor activities.\n"
    if weather_index in sunny:
        suggestion += "It is sunny now, be careful not to have sunburn. Doing outdoor activities should use a " \
                      "sunscreen lotion to avoid sunburn.\n "
    if weather_index in cloudy:
        suggestion += "It is cloudy now. Pay attention to the weather. It may rain later.\n"
    if weather_index in fine:
        suggestion += "The weather is fine now. Very suitable for stargazing.\n"
    if weather_index == 80:
        suggestion += "The weather is windy now. It may have rain later.\n"
    if weather_index == 81:
        suggestion += "The weather is dry now. Remember to use moisturizer to protect your skin.\n"
    if weather_index == 82:
        suggestion += "The weather is humid now. Your cloth may difficult to dry.\n"
    if weather_index == 83:
        suggestion += "The weather is fog now. Careful when you are driving.\n"
    if weather_index == 84:
        suggestion += "The weather is mist now. Careful when you are driving.\n"
    if weather_index == 85:
        suggestion += "The weather is haze now. Careful when you are driving.\n"


# function: analysis the current air quality and give suggestion
def air_quality_analysis():
    for air_obj in airQualityObj:
        if air_obj['type'] == "general":
            general_risk_min = air_obj['health_risk_min']
            general_risk_max = air_obj['health_risk_max']
    print("Today's general Air Quality Health Index (AQHI):", general_risk_min, "to", general_risk_max + "\n")
    global suggestion
    if general_risk_max == "Low" or general_risk_max == "Moderate":
        suggestion += "Today's air quality is very good, very suitable for outdoor activities.\n"
    elif general_risk_max == "high" or general_risk_max == "Very High":
        suggestion += "[Today's air quality is bad, it is recommended to put on a mask.\n"
    else:
        suggestion += "Today's air quality is very bad, it is recommended to put on a mask or avoid outdoor " \
                      "activities.\n "


def plot_graph(fweek, fmax, fmin):
    # Remove item after 7 day, because default is 9 day
    del fweek[7:]
    del fmax[7:]
    del fmin[7:]
    plt.figure(figsize=[8.5, 5])
    plt.plot(fweek, fmax, label="max temperature")
    plt.plot(fweek, fmin, 'g--', label="min temperature")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.xlabel('Week')
    plt.ylabel('Celsius')
    plt.ylim((10, 35))
    plt.title('7-day weather forecast')
    plt.subplots_adjust(right=0.75)
    plt.savefig('forecast.png')
    plt.show()


# suggest clothing combination that suit the temperature
def cloth_suggest(temp):
    if temp > 25:
        outwear = []
        top = random.choice(["T-shirt Crew Neck", "T-shirt V-Neck", "Tank Tops", "Polo Shirt"])
        bottom = random.choice(["Shorts"])
        shoes = random.choice(["Running Shoes", "Sneakers", "Slippers"])
    elif temp > 18:
        outwear = random.choice(["Hooded Jacket", "Windcheater", "Bomber Jacket"])
        top = random.choice(["T-shirt Crew Neck", "T-shirt V-Neck", "Tank Tops", "Polo", "Shirt"])
        bottom = random.choice(["Jeans", "Jogger Pants", "Chino Pants", "Casual Pants", "Shorts"])
        shoes = random.choice(["Running Shoes", "Sneakers", "Boots", "Boat Shoe", "Slippers"])
    elif temp > 13:
        outwear = random.choice(["Hooded Jacket", "Windcheater", "Parka", "Leather Jacket"])
        top = random.choice(["Long Sleeve Jersey", "Sweatshirt", "LONG SLEEVE T-SHIRT"])
        bottom = random.choice(["Jeans", "Jogger Pants", "Chino Pants", "Casual Pants"])
        shoes = random.choice(["Running Shoes", "Sneakers", "Boots", "Boat Shoe"])
    else:
        outwear = random.choice(["Parka", "Padded Coat"])
        top = random.choice(["Long Sleeve Jersey", "Sweatshirt", "LONG SLEEVE T-SHIRT"])
        bottom = random.choice(["Jeans", "Jogger Pants", "Chino Pants", "Casual Pants"])
        shoes = random.choice(["Running Shoes", "Sneakers", "Boots", "Boat Shoe"])
    print("\nOutwear:", outwear), print("Top:", top), print("Bottom:", bottom), print("Shoes:", shoes, "\n")
#===========================================================================================================


# get current weather data from online in json format
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
weatherData = urllib.request.urlopen(url).read().decode()
weatherObj = json.loads(weatherData)

# get air quality data from online in json format
url = "https://ogciopsi.blob.core.windows.net/dataset/aqhi/aqhi.json"
airQualityData = urllib.request.urlopen(url).read().decode()
airQualityObj = json.loads(airQualityData)

# get weather forecast data from online in json format
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en"
weatherForecastData = urllib.request.urlopen(url).read().decode()
weatherForecastObj = json.loads(weatherForecastData)

# create a list and store all the places name and their temperature
places = []
temps = []
for x in weatherObj['temperature']['data']:
    places.append(x['place'])
    temps.append(x['value'])

# create three lists for storing forecast data
forecastWeek = []
forecastMax = []
forecastMin = []
for x in weatherForecastObj['weatherForecast']:
    forecastWeek.append(x['week'])
    forecastMax.append(x['forecastMaxtemp']['value'])
    forecastMin.append(x['forecastMintemp']['value'])

# read config file to get user name and place
if path.exists("config.txt"):
    try:
        config = configparser.ConfigParser()
        config.read_file(open(r'config.txt'))
        username = config.get('My Config', 'Name')
        place = config.get('My Config', 'Place')
    except configparser.NoOptionError:
        print("Missing option in config.txt.")
        username = ""
        place = input_place()
else:
    # let user input their location and store in to place
    username = ""
    place = input_place()

for obj in weatherObj['temperature']['data']:
    if obj['place'] == place:
        temperature = obj['value']

# create a string for storing the suggestion
suggestion = "Hi " + username + ". Here are your daily suggestions.\n"

print("[Weather Report]")
# analysis the user location temperature
temp_analysis(place)
# analysis the current weather
weather_analysis()
# analysis the current air quality
air_quality_analysis()

suggestion += "Have a nice day.\n"
print("[Today's Suggestions]")
print(suggestion)

while True:
    print("---------------------------------------")
    print("  1. View the weather forecast graph")
    print("  2. View the current temperature in all places")
    print("  3. Choose cloth combination for you")
    print("  4. View the suggestions again")
    print("  5. Quit the program")
    print("---------------------------------------")
    index = input("Select a option by typing(1-5): ")
    if index == "1":
        # plot the 7-day weather forecast graph
        plot_graph(forecastWeek, forecastMax, forecastMin)
    elif index == "2":
        for i in range(len(places)):
            print(places[i] + ": " + str(temps[i]) + "°C.")
    elif index == "3":
        # suggest clothing combination that suit the temperature
        cloth_suggest(temperature)
    elif index == "4":
        # display the suggestions again
        print(suggestion)
    elif index == "5":
        print("Bye~")
        # quit the program
        sys.exit(0)
    else:
        print("Error input. Please enter again.")
