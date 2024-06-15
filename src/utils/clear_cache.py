from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set Chrome options
opts = Options()
#opts.add_argument("--headless")  # Optional: run in headless mode
opts.add_argument("--no-sandbox")  # May be necessary in some environments

# Set user agent
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

# Launch Chrome browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# Navigate to a webpage (replace 'https://example.com' with your desired URL)
driver.get("https://google.com")

# Execute JavaScript to clear cache
driver.execute_script("window.localStorage.clear();")
driver.execute_script("window.sessionStorage.clear();")
driver.execute_script("window.location.reload();")

# Close the browser
driver.quit()
