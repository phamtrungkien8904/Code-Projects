from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, time
import time as t

driver = webdriver.Chrome()
driver.get("https://stadt.muenchen.de/buergerservice/terminvereinbarung.html#/services/10339027/locations/10187259")

while True:
    now = datetime.now().time()
    if time(6, 55) <= now <= time(23, 0):
        driver.refresh()
        try:
            # Wait explicitly (max. 1 sec) for the button that contains "Weiter zur Terminauswahl"
            button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Weiter zur Terminauswahl')]"))
            )
            button.click()
            print("Button clicked at:", datetime.now())
        except Exception as e:
            print("Button not found or not clickable:", e)
        t.sleep(5)  # Wait 5 seconds
    else:
        break

driver.quit()