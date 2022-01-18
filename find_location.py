import requests
import json
import math
import geocoder

KEY = "AIzaSyDa9utUpcaPfpA9M3VP7zOTZe9ytm03Hws"


def geo_dist(l1, l2):
    R = 6371000
    ANG1 = l1["lat"] * math.pi / 180
    ANG2 = l2["lat"] * math.pi / 180
    DELTA1 = (l1["lat"] - l2["lat"]) * math.pi / 180
    DELTA2 = (l1["lng"] - l2["lng"]) * math.pi / 180

    a = (math.sin(DELTA1 / 2) ** 2) + (math.cos(ANG1) * math.cos(ANG2)) * (
        math.sin(DELTA2 / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def get_geolocation(location):
    address: str = location["address"]
    URL = f"""
    https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={address.replace(' ', '%20')}&inputtype=textquery&fields=formatted_address%2Cname%2Cgeometry&key={KEY}
    """.encode(
        "utf-8"
    )
    response = requests.get(URL)
    data = eval(response.text)["candidates"]
    if data:
        geo = data[0]["geometry"]
        return geo["location"]
    else:
        print(f"Couldnt find {address} on the map")
        return {}


def add_geolocation(filename):
    with open(f"./testData/{filename}.json", "r") as f:
        data: dict = json.load(f)
    for v in data.values():
        v["geolocation"] = get_geolocation(v)
    with open(f"./testData/{filename}.json", "w") as f:
        json.dump(data, f, ensure_ascii=False)


def find_closest_loc():
    with open("./testData/madaQuickTests.json", "r") as f:
        data: dict = json.load(f)
    me = geocoder.ip("me").latlng
    me = {"lat": me[0], "lng": me[1]}
    closest = data["location0"]
    min_d = geo_dist(me, closest["geolocation"])
    for i, loc in enumerate(data.values(), start=1):
        loc_geo = loc["geolocation"]
        if loc_geo:
            smaller = min(min_d, geo_dist(me, loc_geo))
            if smaller != min_d:
                min_d = smaller
                closest = loc
    print(me)
    print(closest)
    print(min_d)


find_closest_loc()
