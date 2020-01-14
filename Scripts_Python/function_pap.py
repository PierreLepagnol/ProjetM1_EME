#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 16:18:32 2020

@author: pierre
"""

from unidecode import unidecode
import json
import re
import datetime
import ast

def Cleandataset(data):        
    keys=['.','EUR le m']
    for key in keys:
        if key in data.keys():
            del data[key]
        else :continue            
    return data

def GetDetailsBien(div_desc,res):
    patterns= [r'\D+']
    
    list_item_tag=div_desc.find(class_='item-tags')
    list_item_tag=[unidecode(item.strong.text) for item in list_item_tag.find_all('li')]
    for item in list_item_tag:     
        for p in patterns:
            matches= re.findall(p, item)
        for match in matches:
            res[unidecode(match).strip()]=format_list_tag(item)
    res=Cleandataset(res)
#    print('res={}\n\n'.format(res))


    return res

def exportdata(dict_data):
    x = datetime.datetime.now()
    x=x.strftime("%H-%M-%S")
    with open('result-'+x+'.json', 'w') as fp:
        json.dump(dict_data, fp)
    return x
def format_list_tag(item):
    item=re.sub('m2','',item)
    item=re.sub('[^\d]','',item)
    return int(item)

def ScrapDetail(soup):
    res={}
    type_bien=soup.find(class_='item-title').text
#    print(type_bien.split())
    res['type']=type_bien.split()[1]
    nb_photo=len(soup.find_all(class_='img-liquid owl-thumb-item'))
    res['nb_photo']=nb_photo
    
    div_desc=soup.find('div',class_="item-description")
#   Collecte du prix du bien
    tarif=soup.find(class_='item-price').text
    tarif=re.sub('[^\d]','',tarif)
    res['prix']=tarif
    
#   Collecte du code postal
    zipcode=div_desc.find('h2').text
    zipcode= re.findall(r"(\b\d{5}\b)", zipcode)[0]
    res['code postal']=zipcode
##    Collecte des Stations de métro
    list_station=div_desc.find_all(class_='item-transports')
    
    list_name_station=[]
    for item in list_station :
        to_append=item.find(class_='label')
        if(type(to_append)!=type(None)):
                list_name_station.append(to_append.text)

    res['transport']=list_name_station

##    Collecte des détails
    GetDetailsBien(div_desc,res)
##    Collecte des coordonées
    GetCoord(soup,res)
    return res

def GetCoord(soup,res):
    carte_item=soup.find(id='carte_mappy').attrs
#    print(carte_item)
    carte_item=ast.literal_eval(carte_item['data-mappy'])
    res['lat']=float(carte_item['center'][0])
    res['lon']=float(carte_item['center'][1])
    return res