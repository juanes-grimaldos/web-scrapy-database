import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.functions import GeneralFunctions as gf
from utils.functions import go_next_page
import pandas as pd
import logging
import os
from data_bases.data_creation import DataCreation
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


driver = webdriver.Chrome(
    service = Service(GeckoDriverManager().install()), 
    options = opts
)
wait = WebDriverWait(driver, 15)
# seed
driver.get('https://www.exito.com/electrodomesticos/refrigeracion/neveras')

# detect if there are products in the page
try:
    navigation = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//ul[@data-fs-product-grid-type='electrodomesticos']")
        )
    )
except Exception as e:
    logging.info("No products located in the page")

# detect if there are more pages with button next page available
try:
    navigation = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(@aria-label, 'Próxima Pagina')]") 
        )
    )
    pages = range(5) # 5 pages to scrape
except Exception as e:
    logging.info("No more pages available")
    pages = range(0)




for page in pages:
    sleep(random.uniform(5, 10))
    neveras = driver.find_elements(
        By.XPATH, "//ul[@data-fs-product-grid-type='electrodomesticos']/*"
    ) # list of products
    list_of_links_to_visit = []
    for nev in neveras:
        nevera_link = nev.find_element(
            By.XPATH, ".//a[@data-testid='product-link']"
        )
        link = nevera_link.get_attribute("href")
        list_of_links_to_visit.append(link)
    
    visited_links = gf.get_visited_links("Exito")
    # Convert to sets
    links_to_visit_set = set(list_of_links_to_visit)
    visited_links_set = set(visited_links)

    # Remove visited
    filtered_links = list(links_to_visit_set - visited_links_set)

    

    for link in filtered_links:
        driver.execute_script("window.open(arguments[0]);", link)
        # switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        gf.scroll_smooth(driver, 1, 5, initial_scroll=600)
        try:
            # click on 'ver mas' button to see all the specs
            more_view = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'product-specifications')]"
                "//button")
                )
            )
            
            more_view.click()
        except Exception as e:
            logging.info("No 'ver mas' button located or a pop up shows")
            try:
                pop_up = driver.find_element(By.XPATH, "//div[@id='wps-overlay']")

                # Perform a click action outside the pop-up to close it
                action = ActionChains(driver)
                action.move_to_element_with_offset(pop_up, -10, -10).click().perform()

                more_view.click()
            except Exception as e:
                logging.info('Pop-ups break the code! or \'ver mas \' is not available')


        # get info
        product_link = driver.current_url
        sleep(10)
        product_name = driver.find_element(
            By.XPATH, "//h1[contains(@class, 'product-title')]"
        ).text
        product_price = driver.find_element(
            By.XPATH, "//p[contains(@class, 'ProductPrice')]"
        ).text

        # get list of specs
        list_of_specs = [
            "Ancho", "Alto", "Profundidad", "Peso", "Capacidad", "Consumo", 
            "Descongelamiento"
        ]
        def get_spec(spec_name: str):
            '''
            Get the value of a specific spec from the product page
            Exito Only
            '''
            try:
                return driver.find_element(
                    By.XPATH,
                    f"//h2[@data-fs-title-specification='true' and contains(normalize-space(), '{spec_name}')]/following-sibling::h3[1]"
                ).text
            except Exception:
                return None
        
        # get specs and store them in a dictionary

        try:
            button = driver.find_element(
                By.XPATH,
                "//button[@data-fs-cookies-modal-button='true']"
            )
            button.click()
        except:
            pass
        sleep(10)
        try:
            driver.find_element(
                By.XPATH,
                "//div[contains(@class, 'product-specification')]//div[contains(@class, 'more-link')]"
            ).click()
        except:
            pass

        ancho = get_spec(list_of_specs[0])
        alto = get_spec(list_of_specs[1])
        profundidad = get_spec(list_of_specs[2])
        capacidad = get_spec(list_of_specs[4])
        consumo = get_spec(list_of_specs[5])
        descongelamiento = get_spec(list_of_specs[6])

        # store the product info in a dictionary
        product_info_db = {
            "link": product_link,
            "product": product_name,
            "price": int(product_price.replace("$", "").replace(".", "")),
            "seller": "Exito",
        }
        specs_db = {
            "link": product_link,
            "storage": capacidad,
            "energy": consumo,
            "date": pd.to_datetime("today").date(),
            "size": f"{ancho} x {alto} x {profundidad}",
            # no color
        }

        # store the product info in a json file
        # gf.store_product_info("product_info.json", product_info)
        # store the product info in a database
        dc.insert_main_data(data=product_info_db)
        dc.insert_meta_data(data=specs_db)

        
        # close the tab and switch to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


    # once all the products in the page are scraped, go to the next page
    if not go_next_page(driver):
        break

driver.quit()
logging.info("Scraping finished")
