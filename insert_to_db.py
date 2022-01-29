from bs4 import BeautifulSoup
import requests
from datetime import datetime
from db import colec
import log


def write_ichilov(data, test_type):
    locations = []
    for cell in data:
        location = {}
        location["SettlementName"] = cell.find("td", class_="column-1").text
        location["Address"] = cell.find("td", class_="column-2").text
        location["StartTime"] = cell.find("td", class_="column-3").text
        location["EndTime"] = cell.find("td", class_="column-4").text
        geolocation = cell.find("a")
        if geolocation:
            link: str = geolocation["href"]
            point = link[link.find("=") + 1 : link.find("&")]
            latlng = point.split("%2C")
            location["location"] = {
                "type": "Point",
                "coordinates": [float(latlng[1]), float(latlng[0])],
            }
        location["organization"] = "Ichilov Well"
        location["testType"] = test_type
        locations.append(location)
    colec.insert_many(locations)


def get_ichilov():
    URL = "https://ichilov-well.co.il/fast_test/"
    result = requests.get(URL)
    doc = BeautifulSoup(result.text, "html.parser")
    tables = doc.find_all("tbody", class_="row-hover")
    test_types = ["antigen", "PCR"]
    for i, table in enumerate(tables):
        rows: list[BeautifulSoup] = table.find_all("tr")
        write_ichilov(rows, test_types[i])


def get_mada():
    URL = "https://f.mda.org.il:8867/Scheduling/api/Quick/GetCentersForMDAIS"
    headers = {
        "x-abyss-token": "f86b3a1d-e3c0-431a-bde8-c88535cc023a",
    }
    result = requests.post(
        URL,
        json={"Date": str(datetime.today().isoformat()), "Language": "he"},
        headers=headers,
    )
    data = result.json()
    format_mada(data)
    colec.insert_many(data)


def format_mada(data):
    for loc in data:
        lat = loc["Lat"]
        lng = loc["Lon"]
        loc["location"] = {"type": "Point", "coordinates": [lng, lat]}
        loc["organization"] = "MDA"
        loc["testType"] = "antigen"


def refreshDB():
    print("works")
    try:
        log.logger.info("Starting refresh...")
        colec.drop()
        get_ichilov()
        get_mada()
        log.logger.info("Refreshed!")
    except Exception as e:
        log.logger.error(f"refresh failed :( \nException: {e}")


if __name__ == "__main__":
    refreshDB()
