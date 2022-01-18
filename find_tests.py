from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
import time


def get_pikud():
    URL = "https://experience.arcgis.com/experience/e2dfe3e44f4046ba93f37637e10bc6b6?data_id=dataSource_2-%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%93%D7%99%D7%92%D7%95%D7%9D_946%3A520474&locale=he"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "esri-popup__main-container esri-widget")
            )
        )
    except selenium.common.exceptions.TimeoutException:
        print("error")
        driver.quit()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    print(soup.text)


def city_list():
    cities = set()
    with open("madaQuickTests.json", "r") as f:
        locations: dict = json.load(f)
    for item in locations.values():
        cities.add(item["city-name"])
    with open("./testData/cityNames.json", "w") as f:
        json.dump(list(cities), f, ensure_ascii=False)


def get_goodpharm():
    URL = "https://goodpharm.co.il/covtests/"
    result = requests.get(URL)
    doc = BeautifulSoup(result.text, "html.parser")
    locs = doc.find_all("h2", class_="elementor-heading-title elementor-size-default")
    for i in locs:
        print(i.text)


def write_mada(data, filename):
    locations = {}
    for i, row in enumerate(data):
        location = {}
        cells: list[BeautifulSoup] = row.find_all("td")
        loc_info = cells[1].text.replace("–", "-").split("-")
        location["status"] = 1 if cells[0].text == "פתוח" else 0
        try:
            location["city-name"] = loc_info[0].strip()
            location["address"] = loc_info[1].strip()
        except IndexError:
            location["address"] = loc_info[0].strip()
        location["start-time"] = cells[2].text
        location["end-time"] = cells[3].text
        locations[f"location{i}"] = location
    with open(f"./testData/{filename}", "w") as j:
        json.dump(locations, j, ensure_ascii=False)


def get_mada():
    URL = "https://f.mda.org.il:8867/CentersInfo/centers-list"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/app-root/app-centers/table/tr[2]")
            )
        )
    except selenium.common.exceptions.TimeoutException:
        print("error")
        driver.quit()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    table = soup.find_all("tr")[1:]
    write_mada(table, "madaQuickTests.json")


def write_ichilov(data, filename):
    locations = {}
    for i, cell in enumerate(data):
        location = {}
        location["city-name"] = cell.find("td", class_="column-1").text
        location["address"] = cell.find("td", class_="column-2").text
        location["start-time"] = cell.find("td", class_="column-3").text
        location["end-time"] = cell.find("td", class_="column-4").text
        locations[f"location{i}"] = location
    with open(f"./testData/{filename}", "w") as j:
        json.dump(locations, j, ensure_ascii=False)


def get_ichilov():
    URL = "https://ichilov-well.co.il/fast_test/"
    result = requests.get(URL)
    doc = BeautifulSoup(result.text, "html.parser")
    # print(doc.prettify())
    tables = doc.find_all("tbody", class_="row-hover")
    names = ["ichilovQuickTests.json", "ichilovPCRTests.json"]
    for i, table in enumerate(tables):
        rows: list[BeautifulSoup] = table.find_all("tr")
        write_ichilov(rows, names[i])

