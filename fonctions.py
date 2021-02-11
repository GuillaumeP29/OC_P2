# -*-coding:Utf-8 -*
import requests
from bs4 import BeautifulSoup
import re
import csv
import urllib

website_url = 'http://books.toscrape.com/'
image_number = 0
page_number = 1
category_response = ''
book_category = ''
book_number = 0
category_title = ''
csv_path = ''
category_number = 0
category_url = ''
file_header = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

def soup_creation(url):
    #Fonction créant un élément BeautifulSoup à partir d'un URL
    url_response = requests.get(url) #Demande du code HTML de la page d'accueil du site book.toscrap
    if url_response.ok: 
        url_soup = BeautifulSoup(url_response.text, 'lxml')
    return url_soup

def csv_creation(path, file_header):
    #Créer le CSV de la catégorie parcourue
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=file_header)
        writer.writeheader()

def csv_add_file (path, file_header, dictionary):
    #Rajouter un livre dans le CSV
    with open(path, 'a', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=file_header)
        writer.writerow(dictionary)

def download_image (url, name):
    #Télécharger une image
    urllib.request.urlretrieve(url, name)
    global image_number
    image_number += 1
    print(str(image_number) + " image(s) téléchargée(s)")

def next_page():
    #Passer à la page suivante
    global page_number
    global category_response
    global category_url
    
    page_number +=1
    category_url = category_url.replace('index', 'page-' + str(page_number))
    category_url = category_url.replace('page-' + str(page_number - 1), 'page-' + str(page_number))
    category_response = requests.get(category_url)

def book_browser(book_list):
    #Parcours des livre de la catégorie
    for book in book_list:
        book_url = website_url + str("catalogue/") + book.find('h3').find('a')['href'].strip("../") #product_page_url
        book_response = requests.get(book_url) #Récupération du code HTML d'un livre grâce à une requête sur son URL
        book_response.encoding = 'utf-8'
        if book_response.ok: #Vérification que la requête a réussi
            global csv_path
            global book_number
            global book_category
            book_soup = BeautifulSoup(book_response.text, 'lxml') #Création du soup à partir du code HTML obtenu

            #Récupération des données souhaitées
            book_title = book_soup.find(class_="col-sm-6 product_main").find('h1').text #title
            book_description = book_soup.select_one('article>p').text #product_description
            book_description.replace(';', ',')
            book_image = website_url + book_soup.find(class_="item active").find('img')['src'].strip("../") #image_url
            book_category = category_title #category

            #Récupération des données du tableau du livre
            book_table_dictionary = {} #Création d'un premier dictionnaire pour récolter les données indiqué sur le site
            book_dictionary = {} #Création d'un deuxième dictionnaire pour récolter les données souhaitées pour le porjet

            book_table_list = book_soup.find(class_="table table-striped").find_all('tr')
            for tr in book_table_list:
                book_table_dictionary[tr.th.text] = tr.td.text #Remplissage du premier dictionnaire à partir des informations du livre récoltées
                
            #Récupérer seulements les chiffres des prix avec et sans taxe et du nombre de livre
            ###book_table_dictionary["Price (incl. tax)"] = re.findall("\d+", book_table_dictionary["Price (incl. tax)"])[0] + '.' + re.findall("\d+", book_table_dictionary["Price (incl. tax)"])[1]
            ###book_table_dictionary["Price (excl. tax)"] = re.findall("\d+", book_table_dictionary["Price (excl. tax)"])[0] + '.' + re.findall("\d+", book_table_dictionary["Price (excl. tax)"])[1]
            book_table_dictionary["Availability"] = re.findall("\d+", book_table_dictionary["Availability"])[0]

            #Récupération des review_rating
            book_rating = book_soup.find(class_="star-rating")["class"]
            rating_dict = {'One' : 1, 'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5}
            review_rating = rating_dict[book_rating[1]]
            
            book_dictionary["product_page_url"] = book_url
            book_dictionary["universal_product_code"] = book_table_dictionary["UPC"]
            book_dictionary["title"] = book_title
            book_dictionary["price_including_tax"] = book_table_dictionary["Price (incl. tax)"]
            book_dictionary["price_excluding_tax"] = book_table_dictionary["Price (excl. tax)"]
            book_dictionary["number_available"] = book_table_dictionary["Availability"]
            book_dictionary["product_description"] = book_description
            book_dictionary["category"] = book_category
            book_dictionary["review_rating"] = review_rating
            book_dictionary["image_url"] = book_image

            book_number += 1
            print(str(book_number) + " livre(s) scrapé(s)")

            

            #Rajout du livre dans le fichier csv de la catégorie
            csv_add_file(csv_path, file_header, book_dictionary)                        
            
            image_path = "Images/" + book_dictionary["universal_product_code"] + ".jpg"
            #Télécharger l'image du livre
            download_image(book_image, image_path)

        break #Ne prendre qu'un seul livre


def category_browser(category_list):
    #Boucle parcourant les catégories de livre
    for category in category_list:
        global category_title
        category_title = category.text.replace("  ", "").replace("\n", "") #Récupération du titre de chaque catégorie

        global category_number
        global page_number
        global csv_path
        global category_url
        global category_response
        category_number += 1
        print("catégorie " + str(category_number) + " : " + category_title)
        category_url = website_url + category.find('a')['href'] #Création de l'URL de la catégorie à partir de son titre et de l'URL du site
        category_response = requests.get(category_url) #Demande du code HTML de la catégorie Travel
        page_number = 1
        
        csv_path = "CSV/" + category_title + '.csv'
        
        #Création d'un fichier pour la catégorie
        csv_creation(csv_path, file_header)

        while category_response.ok: #Boucle while qui s'effectue si la page demandée existe            
            print(category_title + ' page ' + str(page_number) + ' :')
            category_soup = BeautifulSoup(category_response.text, 'lxml')
            book_list = category_soup.find_all(class_="product_pod") 

            #Parcourir les livres
            book_browser(book_list)

            #Modifie l'URL pour demander la page suivante
            next_page()

        break #Ne faire que la première catégorie pour raccourcir le temps