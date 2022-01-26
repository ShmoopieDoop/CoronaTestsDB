import requests
import json
import math
import pymongo
import os

KEY = "AIzaSyDa9utUpcaPfpA9M3VP7zOTZe9ytm03Hws"

mongo_client = pymongo.MongoClient(
    f"mongodb+srv://ShmoopieDoop:{os.environ.get('MONGO_USER_PASSWORD')}@cluster0.ylm9c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = mongo_client["testLocations"]
colec = db["testLocations"]


def geo_dist(l1, l2):  #! Deprecated
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


def find_closest_loc(user_loc, loc_count):  #! Deprecated
    with open("./testData/madaQuickTests.json", "r") as f:
        data: dict = json.load(f)
    locs = list(data.values())
    locs.sort(
        key=lambda x: geo_dist(x["geolocation"], user_loc)
        if x["geolocation"]
        else 9999999999
    )
    return locs[:loc_count]


def find_near(geoJSON, limit=1):
    col = db["testLocations"]
    if "location_2dsphere" not in col.index_information():
        col.create_index([("location", pymongo.GEOSPHERE)])
    locations = []
    for doc in col.find(
        {"location": {"$nearSphere": geoJSON["coordinates"]}}, projection={"_id": False}
    ).limit(limit):
        locations.append(doc)
    return locations
