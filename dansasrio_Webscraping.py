# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 11:47:43 2018
@author: Daniel Sastre del Río
"""

from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin

# Función que recorre el contenido de la página con las gasolineras de una provincia
def rastrearProvincia(provincia, url):
    url = urljoin(web_url, url)
    pageProvincia = requests.get(url)
    soupProvincia = BeautifulSoup(pageProvincia.content)
    # Se obtiene la tabla donde están los datos con los precios de las gasolineras
    tabla = soupProvincia.find("table", class_="tablesorter ranking-table")
    cabecera = tabla.find("thead").findAll("tr")
    # Se obtiene el cuerpo de la tabla donde están los datos organizados por filas
    contenido = tabla.find("tbody").findAll("tr") 
    print(str(len(contenido)) + " GASOLINERAS EN " + provincia)
    # Se recorren todas las filas extrayendo los datos de cada gasolinera
    for gasolinera in contenido:
        nombre = gasolinera.find("th").text.replace('\n','').strip()
        datos = gasolinera.findAll("td")
        direccion = datos[0].text.replace('Dirección','').replace('\n','').strip()
        gasolina95 = datos[1].text.replace('Gasolina 95','').replace('\n','').strip()
        gasolina98 = datos[2].text.replace('Gasolina 98','').replace('\n','').strip()
        gasoleoA = datos[3].text.replace('Gasoleo A','').replace('\n','').strip()
        # Se escribe en el fichero CSV los datos de la gasolinera
        writer.writerow([provincia, nombre, direccion, gasolina95, gasolina98, gasoleoA])

web_url = "https://www.arpem.com/servicios/gasolineras-baratas/"
# Se obtiene la Web de la URL
page = requests.get(web_url)

status_code = page.status_code
# Si es correcta se realiza la lectura
if status_code == 200:

    # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
    html = BeautifulSoup(page.text, "html.parser")
    soup = BeautifulSoup(page.content)
    # Se le da un formato legible al html de la Web
    page = soup.prettify()
    # Se buscan los vínculos de las páginas de todos las provincias
    provincias = soup.find("ul", class_="provincias").findAll("li")
    print(str(len(provincias)) + " PROVINCIAS EN TOTAL")
    # Se crea el fichero CSV y se escriben las cabeceras de las columnas
    fichero = open('gasolineras.csv', 'w',  newline='\n')
    writer = csv.writer(fichero, quotechar='"', quoting=csv.QUOTE_ALL)  
    writer.writerow(['Provincia', 'Nombre', 'Dirección', 'Gasolina 95', 'Gasolina 98', 'Gasoleo A'])
    # Se recorren todos los vínculos de las páginas de las provincias
    for provincia in provincias:
        nombre_provincia=provincia.find("a").text
        a =  provincia.find("a", href=True)
        url = (a["href"])
        rastrearProvincia(nombre_provincia, url)
        
    fichero.close()

    
    
