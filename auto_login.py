# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00FB463AD97639808B5AA2748087AE0A06A7BF74F7C33669449EA18FF5EF316AF04B86E6223F13DF6AB75B6F186A5B4B5434FB38BE859464BC74381077B33A298A9C116DD8ED32429B0193F0E362DD12D34DE778EB756722B9E7DA8E91B908DDC05C5D15D52524141BE77B6106926293B8C02BA08190FE4407AA0E4956DBB117F9390237CD9E70899C005B8CC2110FA1ECEA548039D0D6CE3F2CBB9368423DE5A4447D8C7357B0275756BB099DB26D8D73355A3606DA18981520F1437E388EE18E6053CC859A4BB1EB851A366DBDD028A06EA328225E977D49AFF69C21A8AA46BDA84A23390C66304439C023DB855D67BF505D6FEBAD815867D67CD3B964FC85660E9F054B090955824DF3F2FD1412EE7184834388FE668C006E77C7C9812AEF60191A05941D54B6DBF3BFD84D9E85A81BFDD1177F68E4B22365A689C0E7BED99B0029C8CE049CAD3E691D5856D56950F727A26E1010097191624CFECA1B6A66E9AD633220043D95496D04D0DF0C18D6F6A0A45682DD2C1482CA397E5B24C89DCAC49EDC66CCC6D9073EBB71F6DD15742E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
