import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.functions import GeneralFunctions as gf
from data_bases.data_creation import DataCreation
import sys
import logging
import pandas as pd
import os

dc = DataCreation()
"""
Ejemplo con Neveras
# TODO: crear otros scripts con otros productos
"""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

opts = Options()
opts.add_argument(os.getenv('USER_AGENT'))
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--window-size=1920,1080")
opts.add_argument('log-level=3')

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()), 
    options = opts
)

def get_specs(spec:str):
    """
    Retrieves the specifications of a given feature from the web page.

    Args:
        spec (str): The feature to retrieve the specifications for.

    Returns:
        str: The specifications of the given feature.
    """
    a ="//div[@class='new-container__table__classifications']"
    b = "//div[@class='new-container__table__classifications___type__item"
    c = f"_feature' and contains(text(), '{spec}')]"
    d = "/following-sibling::div"
    spec = driver.find_element(
        By.XPATH, f"{a}{b}{c}{d}"
    ).text
    return spec

# seed
driver.get('https://www.alkosto.com/electrodomesticos/grandes-electrodomesticos/refrigeracion/c/BI_0610_ALKOS')

# detect if there are products in the page
try:
    navigation = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//ol[@class='ais-InfiniteHits-list product__list']")
        )
    )
except Exception as e:
    logging.info("No products located in the page | try other user agent")
    driver.quit()
    sys.exit()

visited_links = [0]

for i in range(5):    
    xpath = "//button[contains(@class,'ais-InfiniteHits-loadMore')]"
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )

    # Execute the JS script
    element.location_once_scrolled_into_view
    sleep(5)
    element.location_once_scrolled_into_view
    sleep(5)
    element.location_once_scrolled_into_view
    sleep(5)
    driver.execute_script("window.scrollBy(0, -100);")
    sleep(5)

    # store the elements
    children_elements = navigation.find_elements(
        By.XPATH, "//ol[@class='ais-InfiniteHits-list product__list']/li"
    )

    children_elements = [
        item for item in children_elements if item not in visited_links
    ]

    visited_links += children_elements

    for child in children_elements:
        # get the product name
        product_link = child.find_element(
            By.XPATH, ".//a[@href]"
        ).get_attribute('href')
        logging.info(product_link)

        # open a new tab with the product link
        logging.info(f"Opening product link: {product_link}")
        driver.execute_script("window.open(arguments[0]);", product_link)

        # switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        gf.scroll_smooth(driver, 1, 5, initial_scroll=1200)
        sleep(random.uniform(5, 10))

        # get info
        product_link = driver.current_url
        product_title = driver.find_element(
            By.XPATH, "//div[@class='new-container__header__title']//h1"
        ).text
        price = driver.find_element(
            By.XPATH, "//span[@id='js-original_price']"
        ).text
        price = price.replace("$", "").replace(".", "").strip()
        # get the specs
        storage = get_specs('Almacenamiento')
        size = get_specs('Medidas Externas (Ancho x Alto x Fondo)')
        energy_consumption = get_specs('Consumo Minimo Energetico')
        color = get_specs('Tonalidad de Color')

        # store the info
        product_info_db = {
            "link": product_link, 
            "product": product_title,
            "price": int(price.replace('\nHoy', '')),
            "seller": "Alkosto"
        }
        specs_db = {
            "link": product_link,
            "storage": storage,
            "size": size,
            "energy": energy_consumption,
            "color": color,
            "date": pd.to_datetime("today").date()
        }
        # store the data in a json file
        # create a single dic with specs and product_info
        # gf.store_product_info('alkosto_neveras.json', product_info)
        # store the data in a database
        dc.insert_main_data(data=product_info_db)
        dc.insert_meta_data(data=specs_db)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
    try:
        element.click()
    except Exception as e:
        logging.info(
            f"An error occurred while clicking the button at iteration {i}"
        )
        break

driver.quit()
logging.info("Process finished")
