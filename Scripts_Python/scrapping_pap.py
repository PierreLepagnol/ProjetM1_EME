# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:07:38 2019

@author: plepagnol
"""

import requests
from bs4 import BeautifulSoup 
from function_pap import *
import re


def GetHTMLPage(url_str):
    try:
        requete = requests.get(url_str,headers={'User-Agent':'Mozilla/5.0'})
        html_file  = requete.content
        soup = BeautifulSoup(html_file,'html.parser')
#        print(soup)
        return soup
    except :
        print("Erreur")
    
def GetSet_URL_Bien(soup):
    liste_hrefs=set()
    spans_bien=soup.find_all('div',class_="search-list-item")
    for item in spans_bien:
        str_href=item.find('a').get('href')
        liste_hrefs.add(str_href)        
    return liste_hrefs

def GetURLSET(site_main,nmax):
    res=set()
    for number in range(1,nmax+1):
        url_str=site_main+'/annonce/vente-immobiliere-paris-75-g439-'+str(number)
        soup=GetHTMLPage(url_str)
        temp=GetSet_URL_Bien(soup)
        res=res|temp
    return res

def condition_keep(string):
    substring_list = ("/annonces/appartement-paris","/annonces/maison-paris")
    if (string.startswith(substring_list)):
        return True
    else:
        return False

def CleanIDset(IDset):
    keep_set=set()
    for item in IDset:
        if(condition_keep(item)):
            keep_set.add(item)    
    return keep_set


def GetDetails(site_main,URLset):
    res=[]
    for url_detail in URLset:
#        print(url_detail)
        url_str=site_main+url_detail
        soup_ID = GetHTMLPage(url_str)
        to_append=ScrapDetail(soup_ID)
        to_append['url']=url_detail;
        res.append(to_append)
#        res[ID] = ScrapDetail(soup_ID)
    return res


site_main='https://www.pap.fr'
URLset=GetURLSET(site_main,20)
URLset=CleanIDset(URLset)
data=GetDetails(site_main,URLset)    
exportdata(data)
