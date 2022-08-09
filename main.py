import requests
from datetime import datetime
import smtplib
import time

# ISS Overhead Detector Runs Every 60 Seconds

MY_LAT = 40.7127281  # Your latitude
MY_LONG = -74.0060152  # Your longitude

MY_EMAIL = ""  # Your GMAIL
MY_PASSWORD = ""  # Your Password


def is_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 or MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters, verify=False)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now.hour <= sunrise or time_now.hour >= sunset:
        return True
    return False


while True:
    if is_above() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:ISS Overhead Notification\n\nQuick! Lookup, you can spot the ISS right now!"
            )
    time.sleep(60)
