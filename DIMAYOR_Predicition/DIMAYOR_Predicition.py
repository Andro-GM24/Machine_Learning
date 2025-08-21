#librerias necesarias

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

import sys

import zipfile
import os
import selenium
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

from selenium.webdriver.common.by import By

#tener el driver al mismo nivel en la carpeta del proyecto

#instalar los requerimientos




#asignamos el chrome drive a una variable

current_directory = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(current_directory, 'chromedriver')

cService = Service(chromedriver_path)

#usamos el webdriver

driver = webdriver.Chrome(service=cService)


#le damos la url

driver.get("https://fbref.com/en/comps/41/schedule/Primera-A-Scores-and-Fixtures")

sleep(10)

#vamos a encontrar la tabla para usar pandas y extraer toda la información

from selenium.webdriver.support import expected_conditions as EC # Importar condiciones esperadas
from selenium.webdriver.support.ui import WebDriverWait

try: 
#arregalr pop up porque cubre eso

    #pop up cookies 

    #<button class=" osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept " tabindex="0"> <!--?lit$042016611$-->Aceptar todo </button>

    try:
            #es mejor usar el css ya que tenemos las clases
        print(" se aceptó cookies")    
        boton_cookies= WebDriverWait(driver,10).until(
            
             EC.element_to_be_clickable((By.CSS_SELECTOR, "button.osano-cm-accept-all.osano-cm-button--type_accept"))
        )
        boton_cookies.click()
        time.sleep(3)

    except Exception as e:
        print(f"Ocurrió un error al buscar el boton de cookies {e}")

        #se usara la cuadrangulares apertura entonces es necesario la interacción por parte del robot
        #<a class="sr_preset" data-hide="#all_sched .section_heading, #all_sched .topscroll_div" data-show=".assoc_sched_2025_41_1" href="javascript:void(0)">Torneo Apertura</a>


    try:

        #<a class="sr_preset __web-inspector-hide-shortcut__" data-hide="#all_sched .section_heading, #all_sched .topscroll_div" data-show=".assoc_sched_2025_41_1" href="javascript:void(0)">Torneo Apertura</a>
        print(" se oprimió el boton de apertura")
        boton_apertura = WebDriverWait(driver, 10).until(
            
            EC.element_to_be_clickable((By.LINK_TEXT, "Torneo Apertura"))
        )
        #usa el nombre de link para encontrarlo
        boton_apertura.click()
        time.sleep(5)
    except Exception as e:
        print(f"Ocurrió un error al buscar el boton de apertura {e}")

    dataframe_matchlogs_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "sched_all"))
    )
    table_html = dataframe_matchlogs_element.get_attribute('outerHTML')

   
    # pd.read_html obtiene los diferentes df pero con el id solo obtenedremos uno
    df_list = pd.read_html(table_html)
    
    if df_list:#si esta lleno
        dataframe_matchlogs_df = df_list[0] # Tomamos el primer (y debería ser único) DataFrame
        print("DataFrame de registros de partidos creado con éxito:")
        print(dataframe_matchlogs_df) # Muestra las primeras filas para verificar
        dataframe_matchlogs_df.to_csv("apertura.csv")
    else:
        print("No se encontró ninguna tabla en el HTML extraído.")


except Exception as e:
    print(f"Ocurrió un error al buscar o procesar la tabla: {e}")

finally:
    # Siempre asegúrate de cerrar el navegador al final
    print("Cerrando el navegador...")
    driver.quit()    
    
# vamos a tratar los datos