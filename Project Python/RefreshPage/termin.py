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
    if time(6, 55) <= now <= time(8, 0):
        driver.refresh()
        try:
            # Warte explizit auf den Button (max. 1 Sekunden)
            button = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button-next.m-button--primary'))
            )
            button.click()
            print("Button geklickt um:", datetime.now())
        except:
            print("Button nicht gefunden.")
        t.sleep(5)  # Warte 5 Sekunden
    else:
        break

driver.quit()