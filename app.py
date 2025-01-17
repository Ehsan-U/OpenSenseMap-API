from fastapi import FastAPI
from datetime import datetime, timedelta
import httpx

app = FastAPI()


@app.get("/version")
async def get_version():
    return {"version": "0.0.1"}


@app.get("/temperature")
async def get_temperature():
    current_datetime = datetime.now()
    hours_ealier = current_datetime - timedelta(hours=12)
    start_time = hours_ealier.isoformat(timespec="seconds") + "Z"
    end_time = current_datetime.isoformat(timespec="seconds") + "Z"
    url = f"https://api.opensensemap.org/boxes?date={start_time},{end_time}&phenomenon=temperature&format=json"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        for box in response.json():
            temps = [float(sensor['lastMeasurement']['value']) for sensor in box['sensors'] if
                     sensor['title'] == "Temperatur"]
            avg_temp = sum(temps) / len(temps)
            return {"temperature": avg_temp}
