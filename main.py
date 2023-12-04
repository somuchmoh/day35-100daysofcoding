import os
import requests
from twilio.rest import Client

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
API_key = os.getenv("OWM_API_KEY")
URL_endpoint = "https://api.openweathermap.org/data/2.5/forecast"

parameters = {
    "lat": 25.032969,
    "lon": 121.565414,
    "cnt": 4,
    "appid": API_key

}


response = requests.get(url=URL_endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()

weather_list = [weather_data['list'][code]['weather'][0]['id'] for code in range(0, len(weather_data['list']))
                 if weather_data['list'][code]['weather'][0]['id'] < 701]

will_rain = False
for code in weather_list:
    if code < 700:
        will_rain = True


if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
            .create(
        body="It is going to rain today. Remember to bring an ☔️",
        from_= os.getenv("TWILIO_FROM"),
        to= os.getenv("TWILIO_TO"),
    )
    print(message.status)
