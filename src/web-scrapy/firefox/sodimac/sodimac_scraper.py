from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_bases.data_creation import DataCreation
import logging
from time import sleep
import random
import sys
import os
import pandas as pd

dc = DataCreation()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

opts = Options()
opts.add_argument("--window-size=1920,1080")
opts.add_argument("--log-level=3")
opts.add_argument("--headless")
opts.add_argument(os.getenv('USER_AGENT'))

driver = webdriver.Chrome(
    service = Service(GeckoDriverManager().install()), 
    options = opts
)

driver.get('https://www.homecenter.com.co/homecenter-co/'
           'category/cat10850/neveras-y-nevecones/?currentpage=1')

sleep(random.randint(5, 10))

path = 'https://www.homecenter.com.co/homecenter-co/category/cat10850/'

def get_spects(spec:str):
    """
    Retrieves the specifications of a given feature from the web page.

    Args:
        spec (str): The feature to retrieve the specifications for.

    Returns:
        str: The specifications of the given feature.
    """
    a = f"//div[contains(@class,'element key') and contains(text(),'{spec}')]"
    try:
        return driver.find_element(
            By.XPATH, a+"/following-sibling::div"
        ).text
    except Exception as e:
        logging.info(f"Specification {spec} not found")
        return None

pages = range(1, 6)  # 5 pages to scrape

for page in pages:
    # detect if there are products in the page
    try:
        nav = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,"
                "'search-results-products-container')]")
            )
        )
    except Exception as e:
        logging.info("No products located in the page | try other user agent")
        driver.quit()
        sys.exit()


    products = nav.find_elements(
        By.XPATH, "./div[@data-key]//a"
    )

    for product in products:
        # open a new tab with the product link
        link = product.get_attribute('href')
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[-1])
        logging.info(f"Opening product {link}")
        sleep(random.uniform(5, 10))

        # get information from the product
        title = driver.find_element(
            By.XPATH, "//h1[contains(@class, 'product-title')]"
        ).text
        price = driver.find_element(
            By.XPATH, "//div[contains(@class, 'regular-price homecenter-co')]"
            "//div[contains(@class, 'primary')]//span[contains(text(),'.')]"
        ).text

        # get the specifications of the product
        width = get_spects('Alto')
        height = get_spects('Ancho')
        depth = get_spects('Fondo')
        capacity = get_spects('Capacidad bruta')
        energy = get_spects('Consumo energético')

        product_info_db = {
            'link': driver.current_url,
            'product': title,
            'price': int(price.replace('.','')),
            'seller': 'sodimac'
        }
        specs_info_db = {
            'link': link,
            'size': f"{width} x {height} x {depth}",
            'storage': capacity,
            'energy': energy,
            'date': pd.to_datetime('today').date()
        }
        # store the data in a json file
        # gf.store_product_info('sodimac.json', data)
        # store data in database
        dc.insert_main_data(data=product_info_db)
        dc.insert_meta_data(data=specs_info_db)
        

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(random.uniform(5, 10))
    
    driver.get(path+f'neveras-y-nevecones/?currentpage={page+1}')
    logging.info(f"Scraping page {page+1} of {pages[-1]}")
    sleep(random.randint(5, 10))

driver.quit()
logging.info("Scraping finished")
sys.exit()
