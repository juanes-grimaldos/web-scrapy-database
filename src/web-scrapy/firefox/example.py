from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time

# Set up Firefox options
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")

# Initialize the Firefox WebDriver
driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()),
    options=options
)

# URL to scrape
url = "https://www.alkosto.com/electrodomesticos/grandes-electrodomesticos/refrigeracion/c/BI_0610_ALKOS"

try:
    # Open the URL
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)  # Adjust the sleep time as needed
    
    # Example: Find an element by its tag name (h1) and print its text
    element = driver.find_element(By.TAG_NAME, "h1")
    print("Heading:", element.text)
    
    # Example: Find elements by their class name and print their texts
    elements = driver.find_elements(By.CLASS_NAME, "example-class")
    for elem in elements:
        print("Element text:", elem.text)
        
    # You can use various methods to find elements, such as:
    # - driver.find_element(By.ID, "element-id")
    # - driver.find_element(By.NAME, "element-name")
    # - driver.find_element(By.XPATH, "//tag[@attribute='value']")
    # - driver.find_element(By.CSS_SELECTOR, "css.selector")
    
finally:
    # Close the driver
    driver.quit()
