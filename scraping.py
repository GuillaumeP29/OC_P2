import requests
from bs4 import BeautifulSoup
import re
import csv

book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" #product_page_url
website_url = 'http://books.toscrape.com/'
category_url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
books = []
file_header = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]


category_response = requests.get(category_url) #Demande du code HTML de la catégorie Travel
if category_response.ok:
    category_soup = BeautifulSoup(category_response.text, 'lxml')
    book_category = category_soup.find(class_="page-header action").find('h1').text #category
    book_list = category_soup.find_all(class_="product_pod")
    #Création d'un fichier pour la catégorie
    with open(book_category + '.csv', 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=file_header)
        writer.writeheader()
    #Parcours des livre de la catégorie
    for book in book_list:
        book_url = website_url + str("catalogue/") + book.find('h3').find('a')['href'].strip("../")
        book_response = requests.get(book_url) #Récupération du code HTML d'un livre grâce à une requête sur son URL
        if book_response.ok: #Vérification que la requête a réussi
            print(book_response) #Affichage du status de la requête
            book_soup = BeautifulSoup(book_response.text, 'lxml') #Création du soup à partir du code HTML obtenu

            #Récupération des données souhaitées
            book_title = book_soup.find(class_="col-sm-6 product_main").find('h1').text #title
            p_list = book_soup.find_all('p')
            book_description = p_list[3].text #product_description
            book_image = website_url + book_soup.find(class_="item active").find('img')['src'].strip("../") #image_url

            #Récupération des données du tableau du livre
            book_table_dictionary = {} #Création d'un premier dictionnaire pour récolter les données indiqué sur le site
            book_dictionary = {} #Création d'un deuxième dictionnaire pour récolter les données souhaitées pour le porjet

            book_table_list = book_soup.find(class_="table table-striped").find_all('tr')
            for tr in book_table_list:
                book_table_dictionary[tr.th.text] = tr.td.text #Remplissage du premier dictionnaire à partir des informations du livre récoltées
            
            #Récupérer seulements les chiffres des prix avec et sans taxe et du nombre de livre
            book_table_dictionary["Price (incl. tax)"] = re.findall("\d+", book_table_dictionary["Price (incl. tax)"])[0] + '.' + re.findall("\d+", book_table_dictionary["Price (incl. tax)"])[1]
            book_table_dictionary["Price (excl. tax)"] = re.findall("\d+", book_table_dictionary["Price (excl. tax)"])[0] + '.' + re.findall("\d+", book_table_dictionary["Price (excl. tax)"])[1]
            book_table_dictionary["Availability"] = re.findall("\d+", book_table_dictionary["Availability"])[0]
        
            book_dictionary["product_page_url"] = book_url
            book_dictionary["universal_product_code"] = book_table_dictionary["UPC"]
            book_dictionary["title"] = book_title
            book_dictionary["price_including_tax"] = book_table_dictionary["Price (incl. tax)"]
            book_dictionary["price_excluding_tax"] = book_table_dictionary["Price (excl. tax)"]
            book_dictionary["number_available"] = book_table_dictionary["Availability"]
            book_dictionary["product_description"] = book_description
            book_dictionary["category"] = book_category
            book_dictionary["review_rating"] = '?'
            book_dictionary["image_url"] = book_image

            #Mise du dictionnaire dans une liste de livres
            books.append(book_dictionary)

            #Rajout du livre dans le fichier csv de la catégorie
            with open(book_category + '.csv', 'a', encoding='utf-8') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=file_header)
                        writer.writerow(book_dictionary)



            #Affichage du titre de chaque livre récolté, dans la console
            print(book_dictionary["title"])


    