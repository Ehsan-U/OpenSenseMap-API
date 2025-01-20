from fastapi import Depends, FastAPI, HTTPException
from datetime import datetime, timedelta
import httpx

from dependencies import get_client

app = FastAPI()


@app.get("/version")
async def get_version():
    return {"version": "0.0.1"}


@app.get("/temperature")
async def get_temperature(client: httpx.AsyncClient = Depends(get_client)):
    try:
        current_datetime = datetime.now()
        hours_earlier = current_datetime - timedelta(hours=12)
        start_time = hours_earlier.isoformat(timespec="seconds") + "Z"
        end_time = current_datetime.isoformat(timespec="seconds") + "Z"
        url = f"https://api.opensensemap.org/boxes?date={start_time},{end_time}&phenomenon=temperature&format=json"

        response = await client.get(url)
        data = response.json()

        for box in data:
            temps = [
                float(sensor["lastMeasurement"]["value"])
                for sensor in box["sensors"]
                if sensor["title"] == "Temperatur"
            ]
            if temps:
                avg_temp = sum(temps) / len(temps)
                return {"temperature": avg_temp}

        raise HTTPException(status_code=404, detail="No temperature sensors found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
