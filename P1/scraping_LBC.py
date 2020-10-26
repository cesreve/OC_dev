# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 15:15:18 2020

@author: wilders
"""
# =============================================================================
# 
# =============================================================================
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
import lxml
import html5lib

# =============================================================================
# 
# =============================================================================
lbc = "https://www.leboncoin.fr/recherche/?text=immeuble%20de%20rapport&locations=Roubaix_59100__50.68777_3.18415_2930"
m5 = 'https://www.leboncoin.fr/recherche/?category=2&text=bmw%20m5'

# =============================================================================
# 
# =============================================================================
session = HTMLSession()
r = session.get(m5)
r.html.render()  # this call executes the js in the page
session.close()

# =============================================================================
# 
# =============================================================================
soup = BeautifulSoup(r.text, "lxml")
#soup = BeautifulSoup(resp.text, "lxml")
print(soup.prettify())

section = soup.find('ul')
print(section)
for _ in section.find_all('li'):
    try:
        car = str(_.a['href'])
        link = f'https://www.leboncoin.fr{car}'
        print(link)
    except:
        pass  
