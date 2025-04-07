import undetected_chromedriver as uc
import threading
import time

from scraper import mouse
from scraper import course
from scraper.torrey import Torrey
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium import webdriver
from userdata import config

if __name__ == '__main__':
    options = Options()
    options.page_load_strategy = 'none'
    driver = uc.Chrome(options=options)
    driver.maximize_window()

    # Login to Torrey Pines
    torrey = Torrey(driver)
    torrey.login()

    # Re-start the browser every ~10 minutes.
    # 5 minutes of sleep time + each run taking 1 minute
    while True:
        # Search for Torrey Pines!
        # Torrey is checked on every loop
        try:
            driver.switch_to.window(driver.window_handles[0])
            torrey.find_tee_time()
        except:
            print('DEBUG: Failed to retrieve Torrey Pines tee times')

        # Sleep for 30 seconds before the next query
        time.sleep(10)
        if config.Enable_auto_mouse_move:
            mouse.wiggle()

