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
import sys
import logging
from data_bases.data_creation import DataCreation
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

# seed
driver.get('https://www.falabella.com.co/falabella-co/category/CATG32130/Refrigeracion?mkid=HB_1_REF_G14_N2_1081&page=1')

# detect if there are products in the page
try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@id='testId-searchResults-products']")
        )
    )
except Exception as e:
    logging.info("No products located in the page | try other user agent")
    driver.quit()
    sys.exit()


def get_specs(spec:str):
    """
    Retrieves the specifications of a given feature from the web page.
    """
    try: 
        return driver.find_element(
            By.XPATH, f"//td[text()='{spec}']/following-sibling::td"
        ).text
    except:
        return None

pages = range(5)

for page in pages:
    xpath = "//div[@id='testId-searchResults-products']/div"
    # get all elements
    products = driver.find_elements(By.XPATH, xpath)

    for product in products:

        # get the link and open it in a new tab
        link = product.find_element(By.XPATH, "./a").get_attribute("href")
        logging.info(f"Opening product link: {link}")
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[-1])

        # get to the specifications
        path = "//button[@id='swatch-collapsed-id']"
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        element.location_once_scrolled_into_view
        element.click()

        # get information
        title = driver.find_element(
            By.XPATH, "//h1[contains(@class, 'product-name')]"
        ).text
        try:
            price = driver.find_element(
            By.XPATH, "//div[contains(@class, 'product-specifications')]"
            "//li[contains(@class, 'prices-1')]//span"
            ).text
        except:
            price = driver.find_element(
            By.XPATH, "//div[contains(@class, 'product-specifications')]"
            "//li[contains(@class, 'prices-0')]//span"
            ).text

        # get the specifications
        Color = get_specs("Color")
        depth = get_specs("Profundidad")
        width = get_specs("Ancho")
        height = get_specs("Alto")
        capacity = get_specs("Capacidad útil del refrigerador")
        electricity = get_specs("Consumo energético")
        if electricity is None:
            electricity = get_specs("Consumo de energía")

        product_link = driver.current_url

        product_info_db = {
            "link": product_link,
            "product": title,
            "price": int(price.replace("$", "").replace(".", "").strip()),
            "seller": "Falabella",
        }
        specs_db = {
            "link": product_link,
            "storage": capacity,
            "size": f"{width} x {height} x {depth}",
            "energy": electricity,
            "color": Color,
            "date": pd.to_datetime("today").date()
        }
        # store info in database
        # store in json file
        # gf.store_product_info('fallabela.json', product_info)
        dc.insert_main_data(data=product_info_db)
        dc.insert_meta_data(data=specs_db)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(random.uniform(5, 10))
    
    # go to the next page
    logging.info(f"Going to the next page: {page + 1} of {len(pages)}")
    driver.get(f"https://www.falabella.com.co/falabella-co/category/CATG32130/Refrigeracion?mkid=HB_1_REF_G14_N2_1081&page={page + 1}")

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@id='testId-searchResults-products']")
            )
        )
    except Exception as e:
        logging.info("No products located in the page | try other user agent")
        driver.quit()
        sys.exit()

driver.quit()
logging.info("Process finished successfully")
sys.exit()
