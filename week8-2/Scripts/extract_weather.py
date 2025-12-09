import json
from pathlib import Path
from datetime import datetime
import requests

data_dir=Path(__file__).resolve().parents[1]/"data"/"raw"
data_dir.mkdir(parents=True,exist_ok=True)

def  extract_weather_data(lat=17.17,lon=78.4867,days=1):
        url="https://api.open-meteo.com/v1/forecast"
        prams={
                "latitude":lat,
                "longitude":lon,
                "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "forecast_days":days,
                "timezone":"auto"

        }
        resp=requests.get(url,params=prams)
        resp.raise_for_status()
        data=resp.json()

        filename=data_dir/f"weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filename.write_text(json.dumps(data, indent=2))
        print(f"Extracted weather data save to :{filename}")
        return data

if __name__=="__main__":
        extract_weather_data()
        