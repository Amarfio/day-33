import requests
from datetime import datetime
import smtplib
import time

# response = requests.get(url="http://api.open-notify.org/iss-now.json#")
# print(response.status_code)

# if response.status_code == 400:
#     raise  Exception("That resource does not exist.")
# elif response.status_code == 401:
#     raise Exception("You are not authorised to access this data")

#OR
# response.raise_for_status()
# data = response.json()
# # print(data["iss_position"])
# longitude = data["iss_position"]["longitude"]
# latitude = data["iss_position"]["latitude"]
# iss_position = (longitude, latitude)
# print(iss_position)

# parameters = {
#     "lat": 5.603717,
#     "lng": -0.186964,
#     "formatted": 0
# }
#
# response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
# response.raise_for_status()
# data = response.json()
# sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
# sunset = data["results"]["sunset"].split("T")[1].split(":")[0]
# print(f"sunrise time {sunrise}")
# print(f"sunset time {sunset}")
# print(data)

MY_LAT = 5.603717
MY_LONG = -0.186964

#email credentials
MY_EMAIL = "joshuaamarfio1@gmail.com"
MY_PASSWORD = "eitckhtbudwcqmwj"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #your position is within +5 degrees of the iss position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        pass

def is_night():
    parameters = {
        "lat" : MY_LAT,
        "lng" : MY_LONG,
        "formatted" : 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
    sunset = data["results"]["sunset"].split("T")[1].split(":")[0]
    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("stmp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject:Happy Birthday:\n\nThe ISS is above you in the way"
            )
        # print(f"sunrise time {sunrise}")
        # print(f"sunset time {sunset}")