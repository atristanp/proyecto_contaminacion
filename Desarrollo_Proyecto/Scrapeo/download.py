#!/usr/bin/env python3.7
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {"download.default_directory":"/home/proyectos_contaminacion/daily_data/download"}
chrome_options.add_experimental_option("prefs",prefs)

CHROMEDRIVER_PATH = './chromedriver'
tiempo_real_diario_url = 'https://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv'

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)
driver.get(tiempo_real_diario_url)

time.sleep(3)
print(datetime.now())
driver.close()
