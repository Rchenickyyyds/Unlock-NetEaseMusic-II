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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A7EB6BC5FF4BDF9C166BFD55089CBADC4FB62CFE9FD0A8E68AA863658159C08349B796E7B77C8644D60F074B90F81DB05FBDA93CBF567527439902B0514293595B0E73BB71362237D1DA1574C18AA4038CC6237AACE28C27DEE99359AF58C0129D05B6135EF035C73D95D1BD76C42CBE0D3879B266683DA754B00EB4B5151E99753A7D6764D2CFE12DFDB65CE11851FFD9F7A293ACEE43CB2481AAF09C5ED8A1E57164FDE34D92B1C541E8537CD5E4AD22D31F32F339CDD8A1B4405C9AB903FBC2089D8C749E9C5E4B24DC01D01838C6980D5909B55B12A93F935030B8F6EEB59370EDA25E9AFE5BCC147B4C886A326C9DB642AB0582649BF293567EDA387491ACAF833949F879F25F7DAF732BA468213F61F60128AE941FBF1CBAA572C481B70FBE1B98F18539072B1C0832DD8156DC11DC2DF7D54B5DE0DDE327A23B262D258E0844A113176348AE9D8877257BD813FFE0554A51B549D661C62AA2B08A818317BCA144DED5263E88C007740BC296019E0D07C0F0A5CFA59186EED1C7302D025FF0CD7D71C2E2B6AA5A2B927FF7CC798CF7176B6DC7D1FDF985A35E55FB4226"})
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
