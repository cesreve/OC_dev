# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:19:10 2020

@author: wilders
"""
# =============================================================================
# 
# =============================================================================
from bs4 import BeautifulSoup
from requests_html import HTMLSession

import pandas as pd
import numpy as np

import time


# =============================================================================
# fonctions
# =============================================================================

# =============================================================================
# =============================================================================
def get_soup(link):
    print('Starting request...')
    session = HTMLSession()
    r = session.get(link)
    try:
        r.html.render()  # this call executes the js in the page
    except:
        pass    
    session.close()
    
    soup = BeautifulSoup(r.text, "lxml")
            
    # sécurité
    wait = np.random.uniform(2, 7)
    print(f"Waintg...{}sec")
    time.sleep(wait)
    
    return soup
# =============================================================================
# =============================================================================
def get_caracteristiques(page_annonces, nombre):
    # on crée la dataframe
    table_biens = {"nom": [],
               "prix": [],
               #"lieu": [],
               "lien": [],
               #"type": [],
               "description": [],
               "surface": [],
               "pieces": []}
               #"date": []}
                   
    # on récupère la page
    mes_annonces = get_soup(page_annonces)    
    section = mes_annonces.find('ul')
    
    i = 0       
    for _ in section.find_all('li'):
        i += 1
        if i > nombre:
            break
        try:
            #nom
            name = _.find('p', class_='_2tubl').text
            table_biens['nom'].append(name)
            #print('nom: ', '\n', name)
            
            #prix       
            price = _.find('span', class_='_1NfL7').text
            table_biens['prix'].append(price)
            #print('prix: ', '\n', price)
            
            #lien
            bien = str(_.a['href'])
            link = f'https://www.leboncoin.fr{bien}'
            table_biens["lien"].append(link)
            #print('lien: ', '\n', link)
            
            #description
            descr = get_description(link)[0]
            table_biens["description"].append(descr)
            
            #surface
            surf = get_description(link)[1]
            table_biens["surface"].append(surf)
            
            #pièces
            surf = get_description(link)[2]
            table_biens["pieces"].append(surf)
            
        except:
            pass
    
    
    return pd.DataFrame(table_biens) 

    
# =============================================================================
# =============================================================================

def get_description(lien_annonce):
    # appel fonction
    ma_soupe = get_soup(lien_annonce)
    
    # description
    desc = ma_soupe.find('span', class_='_1fFkI').text
    #adview_description_container
    
    # surface
    for item in soup.find_all(attrs={"data-qa-id": True}):
        if item['data-qa-id']=='criteria_item_square':
            surface = item.text[7:]
    surface = soup.find(attrs={"data-qa-id": "criteria_item_square"}).text[7:]
            
    # pièces            
    for item in soup.find_all(attrs={"data-qa-id": True}):
        if item['data-qa-id']=='criteria_item_rooms':
            pieces = item.text[6:]
    
    return desc, surface, pieces
# =============================================================================
# =============================================================================

# =============================================================================
# test
# =============================================================================
arm = "https://www.leboncoin.fr/recherche/?category=9&text=immeuble&locations=Armenti%C3%A8res_59280__50.64844_2.87243_6510"   


armentières = get_caracteristiques(arm, 4)

print(armentières.loc[1, 'description'])
print(link)
print(ma_soupe)
soup.find('span', class_='_1fFkI').text





