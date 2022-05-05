from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import zipfile
import os
from os import remove
'''
#Tiempo real
tiempo_real_diario_url = 'https://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv'
option = webdriver.ChromeOptions()
prefs = {"download.default_directory":"C:\\Users\\nacho\\Documents\\U-TAD\\Proyectos IV\\Trabajo Grupal\\DownloadCSVS\\DownloadSelenium\\RealTime"}
option.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=".\\chromedriver.exe",options=option)
driver.get(tiempo_real_diario_url)
time.sleep(3)
driver.close()
'''
#Historicos
historic_folder = "C:\\Users\\Álvaro Tristán\\Desktop\\Proyectos IV\\HistóricoDiario\\ScrapeoNacho\\DownloadCSVS\\DownloadSelenium\\Historic"
historicos_url = 'https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=f3c0f7d512273410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default'
option = webdriver.ChromeOptions()
prefs = {"download.default_directory":historic_folder}
option.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=".\\chromedriver.exe",options=option)
driver.get(historicos_url)
time.sleep(3)
links = driver.find_elements(By.CLASS_NAME, 'asociada-link') #By.PARTIAL_LINK_TEXT,'calidad-aire-horario'
cont = 22 #Tamaño historico
urls = []
for i in links:
    urls.append(i.get_attribute('href'))
    cont -= 1
    if cont == 0:
        break
driver.close()
for url in urls:
    driver = webdriver.Chrome(executable_path=".\\chromedriver.exe", options=option)
    driver.get(url)
    time.sleep(6) #Zips tardan en descargar, modificar conforme a la velocidad de conexión
    driver.close()
    list_items_historic_folder = os.listdir(historic_folder)
    zipfiles = list(filter(lambda x: '.zip' in x, list_items_historic_folder))
    for item in zipfiles:
        with zipfile.ZipFile(historic_folder + "\\" + str(item), 'r') as zip_ref:
            zip_ref.extractall(historic_folder + "\\" + str(item[:-4]))
        remove(historic_folder + "\\" + str(item))