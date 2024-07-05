
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import time
import csv


#Direccion PATH del chromedriver


#Función de comprobacion de disponibilidad del sistema
def inicioComprobacionLMS(url):
    service_data = Service(executable_path="../chromedriver.exe")
    driver = webdriver.Chrome(service=service_data)

    driver.get(url)
    time.sleep(10)
    driver.quit() 
    return 0


def extraccionRecursosEntregados(url=""):
    service_data = Service(executable_path="../chromedriver.exe")
    driver = webdriver.Chrome(service=service_data)

    #url = "https://classroom.google.com/u/0/c/NDg4NjMzMzczOTgw/a/NTI3NDcyNDMwMjgx/details"
    driver.get(url)
    time.sleep(50)
    #Obtener contenido de la pagina
    page_source = driver.page_source 

    #Parsear contenido a HTML
    doc = BeautifulSoup(page_source, 'html.parser')
    #En el HTML busqueda por clase    
    elements = doc.find_all(class_="GWZ7yf AJFihd LBlAUc YkTkoe")
    list_elements = []

    elements_aux = elements[0].children
    next(elements_aux)
    next(elements_aux)
    elements_aux = next(elements_aux).children
    elements_aux = next(elements_aux).children
    next(elements_aux).children
    elements_aux = next(elements_aux).children
    for i in elements_aux:
        #list_elements.append(i.strings)
        #list_elements.append(i.contents)
        list_elements.append(i)

    driver.quit()
    return list_elements


def extraccionComentariosClases(url=""):
    service_data = Service(executable_path="../chromedriver.exe")
    driver = webdriver.Chrome(service=service_data)

    #url = "https://classroom.google.com/u/0/c/NDg4NjMzOTA4NjQy/a/NTQ4MzIyMzYxMDg1/details?hl=es"
    driver.get(url)
    time.sleep(50)
    #Obtener contenido de la pagina
    page_source = driver.page_source

    #Parsear contenido a HTML
    doc = BeautifulSoup(page_source, 'html.parser')
    #En el HTML busqueda por clase
    elements = doc.find_all(class_="Ono85c VvAAB")
    list_elements=[]

    elements_aux = elements[0].children
    for i in elements_aux:
        #list_elements.append(i.strings)
        #list_elements.append(i.contents)
        list_elements.append(i)

    driver.quit()
    return list_elements


#
def extraccionTituloDefinicion(url=""):
    service_data = Service(executable_path="../chromedriver.exe")
    driver = webdriver.Chrome(service=service_data)

    #url = "https://classroom.google.com/u/0/c/NDg4NjMzMzczOTgw/a/NTI3NDcyNDMwMjgx/details"
    driver.get(url)
    time.sleep(50)
    xpath = """//*[@id="yDmH0d"]/c-wiz[3]/div[2]/div/div[6]/div[2]/div[2]/div[1]/div[1]/div[1]/h1/span"""
    wel1 = driver.find_element(By.XPATH, xpath)
    xpath = '//*[@id="yDmH0d"]/c-wiz[3]/div[2]/div/div[6]/div[2]/div[2]/div[1]/div[2]/span'
    wel2 = driver.find_element(By.XPATH, xpath)
    
    driver.quit()
    return wel1.text, wel2.text


def text_power_point(url=""):
    service_data = Service(executable_path="../chromedriver.exe")
    driver = webdriver.Chrome(service=service_data)

    #url = "https://drive.google.com/file/d/1ORxPQkKGjdwHuY5FgmTWP3s4iozvS97b/view?hl=es"

    driver.get(url)
    time.sleep(50)
    
    #Obtener contenido de la pagina
    page_source = driver.page_source

    #Parsear contenido a HTML
    doc = BeautifulSoup(page_source, 'html.parser')
    elements = doc.find_all(class_="ndfHFb-c4YZDc-cYSp0e-DARUcf-Df1ZY-bN97Pc-haAclf")
    time.sleep(50)

    texto = """""" 
    for el in elements:
        aux = """"""
        for i in el.strings:
            if len(aux) == 0:
                aux = aux + i + " "
            else:
                aux = aux + i
        if len(aux) == 0:
            texto = texto + aux + " "
        else:
            texto = texto + aux
    texto = texto.replace('\n',' ')

    driver.quit()
    return texto


def generacionContenidoCSV(nombre_archivo="", header="", data=""):
    header = ["texto"]
    row_list = []
    row_list.append(header)
    row_list.append(data)
    with open('../recursos/contenidoHTML/'+nombre_archivo+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(row_list)
        f.close()


#https://drive.google.com/file/d/1LqE1yxAFWo2yaPTgXczRIabZBQ61qMu6/view?hl=es
#https://drive.google.com/file/d/1GHB5U0vguLBZtVqZnJ40t2Me1-R01qmp/view?hl=es
#https://drive.google.com/file/d/13BDgfsTtgVWIS1tXpkKCUJVSdtzrgJI-/view?hl=es
#https://drive.google.com/file/d/1fORpcef43VeuT192tpSNbzpF2vt8T8Hl/view?hl=es
#https://drive.google.com/file/d/1r-4hQ7z-k0mQ0S2T0fs3_LQAkkV1VmGg/view?hl=es
#https://drive.google.com/file/d/1ORxPQkKGjdwHuY5FgmTWP3s4iozvS97b/view?hl=es
"""
urls = ['https://drive.google.com/file/d/1LqE1yxAFWo2yaPTgXczRIabZBQ61qMu6/view?hl=es']
for url in urls:
    texto = text_power_point(url)
    datos = [texto]
    generacionContenidoCSV(nombre_archivo=url.split('/')[-2], data=datos).
"""

