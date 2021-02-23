# -*-coding:Utf-8 -*

import urllib
import csv
import requests
from bs4 import BeautifulSoup
import re

def soup_creation(url):
    """Fonction créant un élément BeautifulSoup à partir d'un URL"""
    url_response = requests.get(url) 
    url_response.encoding = "utf-8"
    if url_response.ok: 
        url_soup = BeautifulSoup(url_response.text, 'lxml')
    return url_soup

def category_list_creation(website_url, soup):
    """Création d'une liste d'url des catégories ainsi qu'un dictionnaires les associant avec leur
       nom de catégorie"""
    category_list = soup.find(class_="nav nav-list").find('ul').find_all('li')
    category_url_list = []
    category_title_dict = {}
    for category in category_list:
        category_url = website_url + category.find('a')['href']
        category_url_list.append(category_url)
        category_title_dict[category_url] = category.find('a').text.replace('\n', '').replace('  ', '')
    return category_url_list, category_title_dict

def csv_creation(category_url, category_dict, file_header):
    """Création d'un fichier csv pour la catégorie"""
    category_title = category_dict[category_url]
    path = "CSV/" + category_title + '.csv'
    with open(path, 'w', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=file_header)
        writer.writeheader()

def csv_add_book(category_url, category_dict, file_header, dictionary):
    """Rajout d'un livre dans le fichier csv de sa catégorie"""
    category_title = category_dict[category_url]
    path = "CSV/" + category_title + '.csv'
    with open(path, 'a', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=file_header)
        writer.writerow(dictionary)

def next_page(page_url):
    """Générer la page suivante"""
    parts = page_url.split("/")
    last_part = parts[-1]
    if last_part == 'index.html':
        return "/".join(parts[:-1]) + '/page-2.html' 
    else:
        nb = int(last_part.removeprefix('page-').removesuffix('.html')) + 1
        return "/".join(parts[:-1]) + '/page-' + str(nb) + '.html'

def page_exists(url):
    """Vérifie qu'une page existe"""
    url_response = requests.get(url)
    if url_response.ok:
        return True
    else:
        return False

def page_browser(category_url):
    """Crée une liste des pages existantes pour une catégorie de livres"""
    page_url_list = []
    while page_exists(category_url):
        page_url_list.append(category_url)
        category_url = next_page(category_url)
    return page_url_list

def book_browser(website_url, page_url):
    """Crée la liste d'url des livres d'une page"""
    book_url_list = []
    category_soup = soup_creation(page_url)
    product_list = category_soup.find_all(class_="product_pod")
    for product in product_list:
        book_url = website_url + str("catalogue/") + product.find('h3').find('a')['href'].strip("../")    
        book_url_list.append(book_url)
    return book_url_list

def review_rating(book_soup):
    """Récupération de la note du livre"""
    book_rating = book_soup.find(class_="star-rating")["class"]
    rating_dict = {'One' : 1, 'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5}
    review_rating = rating_dict[book_rating[1]]
    return review_rating

def book_table_dict_creation(book_soup):
    """Récupération des informations du tableau du livre"""
    book_table_dictionary = {} #Création d'un premier dictionnaire pour récolter les données indiqué dans un tableau du site web
    book_table_list = book_soup.find(class_="table table-striped").find_all('tr')
    for tr in book_table_list:
        book_table_dictionary[tr.th.text] = tr.td.text #Remplissage du premier dictionnaire à partir des informations du livre récoltées     
    book_table_dictionary["Availability"] = re.findall("\d+", book_table_dictionary["Availability"])[0] #Récupérer seulements les chiffres du nombre de livres
    return book_table_dictionary

def book_dict_creation(book_table_dictionary, book_url, book_title, book_description, book_category, book_rating, book_image):
    """Création d'un dictionaire à partir des informations d'un livre"""
    book_dictionary = {}
    book_dictionary["product_page_url"] = book_url
    book_dictionary["universal_product_code"] = book_table_dictionary["UPC"]
    book_dictionary["title"] = book_title
    book_dictionary["price_including_tax"] = book_table_dictionary["Price (incl. tax)"]
    book_dictionary["price_excluding_tax"] = book_table_dictionary["Price (excl. tax)"]
    book_dictionary["number_available"] = book_table_dictionary["Availability"]
    book_dictionary["product_description"] = book_description
    book_dictionary["category"] = book_category
    book_dictionary["review_rating"] = book_rating
    book_dictionary["image_url"] = book_image
    return book_dictionary

def book_scraping(website_url, book_url):
    book_soup = soup_creation(book_url)
    #Récupération des données souhaitées
    book_title = book_soup.find(class_="col-sm-6 product_main").find('h1').text #title
    book_description = book_soup.select_one('article>p').text #product_description
    book_description.replace(';', ',')
    book_image = website_url + book_soup.find(class_="item active").find('img')['src'].strip("../") #image_url
    book_category = book_soup.find(class_="breadcrumb").find_all('li')[2].text.replace('\n', '') #category
    
    #Récupération des review_rating
    book_rating = review_rating(book_soup)

    #Récupération des dernières données
    book_table_dictionary = book_table_dict_creation(book_soup)

    #Création du dictionnaire du livre avec toutes les données
    book_dictionary = book_dict_creation(book_table_dictionary, book_url, book_title, book_description, book_category, book_rating, book_image)

    return book_dictionary

def download_image(book_dictionary):
    """Télécharger une image"""
    image_url = book_dictionary['image_url']
    path = 'Images/' + str(book_dictionary['universal_product_code']) + '.jpg'
    urllib.request.urlretrieve(image_url, path)

def website_scraping(website_url, file_header):
    """Scraping du site web"""
    website_soup = soup_creation(website_url)
    category_list = category_list_creation(website_url, website_soup) #Récupération des catégories de livre
    book_count = 0
    category_count = 0
    for category_url in category_list[0]: #Parcourir les catégories du site
        csv_creation(category_url, category_list[1], file_header)
        category_count += 1
        print('catégorie ' + str(category_count) + " : " + category_list[1][category_url])
        page_url_list = page_browser(category_url)
        for page_url in page_url_list: #Parcourir les pages d'une catégorie
            book_url_list = book_browser(website_url, page_url)
            for book_url in book_url_list: #Parcourir les livres d'une page
                book_dictionary = book_scraping(website_url, book_url)
                csv_add_book(category_url, category_list[1], file_header, book_dictionary)
                download_image(book_dictionary)
                book_count += 1
                print(str(book_count) + ' livre(s) scrapé(s)')
