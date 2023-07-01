from flask import Flask, request, jsonify, send_file
from main import gen_plot
import base64
from io import BytesIO
from typing import List, Dict, Optional
import requests


def get_name(lat, lon):
    params = {
        "language": "en",
        "worldview": "cn",
        "access_token": "pk.eyJ1Ijoic29uZ2hvbmd5aSIsImEiOiJja25jdDdjZG4xM25iMnVvb2NjbDl3YjMwIn0.PJZgJQmBgR_g-vsSD7uKFA"
    }
    url = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + str(lon) + "," + str(lat) + ".json"
    r = requests.get(url, params=params)
    r = r.json()
    if len(r['features']) == 0:
        return None
    for feature in r['features']:
        if feature['id'].startswith("place"):
            return feature['text']
    for feature in r['features']:
        if feature['id'].startswith("country"):
            return feature['text']
    return None


class Query():
    name: Optional[str]
    data: Dict[str, List[float]]
    lat: Optional[float]
    lon: Optional[float]

    def __init__(self, json):
        self.name = json.get("name", None)
        self.data = json.get("data", None)
        self.lat = json.get("lat", None)
        self.lon = json.get("lon", None)

        # validate
        if self.data is None:
            raise ValueError("data is required")
        if not isinstance(self.data, dict):
            raise TypeError("data must be a dict")
        if "prep" not in self.data or "temp" not in self.data:
            raise ValueError("data must contain 'prep' and 'temp'")
        if not isinstance(self.data["prep"], list) or not isinstance(self.data["temp"], list):
            raise TypeError("data['prep'] and data['temp'] must be lists")
        if len(self.data["prep"]) != 12 or len(self.data["temp"]) != 12:
            raise ValueError("data['prep'] and data['temp'] must have length 12")
        # prep and temp must be floats. Validate and Raise valueError if not
        for i in range(12):
            if not (isinstance(self.data["prep"][i], float) or isinstance(self.data["prep"][i], int)) or not (
                    isinstance(self.data["temp"][i], float) or isinstance(self.data["temp"][i], int)):
                raise TypeError("data['prep'] and data['temp'] must be lists of floats")
        if self.name is None and (self.lat is None or self.lon is None):
            raise ValueError("name or latlon is required")
        if self.lat is not None and self.lon is not None:
            if not (-90 <= self.lat <= 90):
                raise ValueError("lat must be between -90 and 90")
            if not (-180 <= self.lon <= 180):
                raise ValueError("lon must be between -180 and 180")
            self.name = get_name(self.lat, self.lon)


app = Flask(__name__)


@app.route("/", methods=["POST"])
def main():
    data = request.json
    data = Query(data)
    name = data.name
    data = data.data
    fig = gen_plot(data, name)
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=300)
    buffer.seek(0)
    data = base64.b64encode(buffer.read()).decode("utf-8")
    return send_file(BytesIO(base64.b64decode(data)), mimetype="image/png"), 200, {
        "Access-Control-Allow-Origin": "*",
    }
