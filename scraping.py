# -*-coding:Utf-8 -*
import requests
from bs4 import BeautifulSoup
import re
import csv
import urllib
import fonctions

#Création de la beautifulSoup à partir d'une fonction prenant l'url du site en paramètre
website_soup = fonctions.soup_creation(fonctions.website_url)

#Récupération de la liste de catégories tout en me débarrassant de l'entête "Books"
category_list = website_soup.find(class_="nav nav-list").find('ul').find_all('li')

fonctions.category_browser(category_list)