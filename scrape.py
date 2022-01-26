from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
from bs4 import BeautifulSoup
import requests

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


def get_goodpharm():
    URL = "https://goodpharm.co.il/covtests/"
    result = requests.get(URL)
    doc = BeautifulSoup(result.text, "html.parser")
    locs = doc.find_all("h2", class_="elementor-heading-title elementor-size-default")
    for i in locs:
        print(i.text)