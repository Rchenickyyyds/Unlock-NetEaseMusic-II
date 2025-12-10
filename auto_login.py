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
    browser.add_cookie({"name": "MUSIC_U", "value": "00603521D31D2822FF8D4E4B0291CA9284844E95347A61F04F7ED6EAF6E491BCD29286DF3A858E9835232FB793E2B3774FE0B61F5DDE9DFC28F52F8A204D0C8680DBC29B9D89632CA3681C2EEA17079864607BF17C12E35EA020FF47A670E05C38E11F69662CF8AFB8FAB9F9CE21336142524FB15DDD146D21E225E1E1EDF7F70F45C581127D7AAB72461E6050675E492408C77E86035E91A74718AA9D24A59EE5FAFA9517A340111CB675818E698F1544D1D1E56192CA231E4AC3E3C1EC5D04031B5BFBEA17A3A77F789B7DDD216AE680085C78AF137CF5A1F19D8EEFEE285E685126FD383906903520967CA416C52E03AA543AFF9EA18631390CA0D07B594C135046B16988D62A575F7E520D45A813FC3B05C4183D8D6F2C29F1AD2F89ECC51D370BE56B6FCC5FED9276F76AC62A1064F9714BA85BF35A0987B014D4C940D7B3A2B5BC6287F2A1E4C68AD2031FFC3B6FACD696F7F84A01A0B1F44E3A7E35BAD204B529B8E9C49533807BF38F401F53B142121A43F43F05B5C1CA3286D6C766EDFC31C2F124BCC5A290A793FFAC5E02E9CF637312389EC6071791338E1CA5804B"})
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
