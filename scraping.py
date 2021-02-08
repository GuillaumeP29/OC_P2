import requests
from bs4 import BeautifulSoup
import re
import csv

website_url = 'http://books.toscrape.com/'
website_response = requests.get(website_url) #Demande du code HTML de la page d'accueil du site book.toscrap
books = []
file_header = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

if website_response.ok: 
    website_soup = BeautifulSoup(website_response.text, 'lxml')

    #Récupération de la liste de catégories tout en me débarrassant de l'entête "Books"
    category_list = website_soup.find(class_="nav nav-list").find('ul').find_all('li')

    #Boucle parcourant les catégories
    for category in category_list:
        category_title = category.text.replace("  ", "").replace("\n", "") #Récupération du titre de chaque catégorie
        category_url = website_url + category.find('a')['href'] #Création de l'URL de la catégorie à partir de son titre et de l'URL du site
        category_response = requests.get(category_url) #Demande du code HTML de la catégorie Travel
        
        page_number = 1

        #Création d'un fichier pour la catégorie
        with open("CSV/" + category_title + '.csv', 'w', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=file_header)
            writer.writeheader()
        
        while category_response.ok: #Boucle while qui s'effectue si la page demandée existe
            print(category_title + ' ' + str(page_number) + ' ' + 'ok')
            category_soup = BeautifulSoup(category_response.text, 'lxml')
            book_category = category_title #category
            book_list = category_soup.find_all(class_="product_pod")            
            
            #Parcours des livre de la catégorie
            for book in book_list:
                book_url = website_url + str("catalogue/") + book.find('h3').find('a')['href'].strip("../") #product_page_url
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
                
                    book_dictionary[file_header[0]] = book_url
                    book_dictionary[file_header[1]] = book_table_dictionary["UPC"]
                    book_dictionary[file_header[2]] = book_title
                    book_dictionary[file_header[3]] = book_table_dictionary["Price (incl. tax)"]
                    book_dictionary[file_header[4]] = book_table_dictionary["Price (excl. tax)"]
                    book_dictionary[file_header[5]] = book_table_dictionary["Availability"]
                    book_dictionary[file_header[6]] = book_description
                    book_dictionary[file_header[7]] = book_category
                    book_dictionary[file_header[8]] = '?'
                    book_dictionary[file_header[9]] = book_image

                    #Mise du dictionnaire dans une liste de livres
                    books.append(book_dictionary)

                    #Rajout du livre dans le fichier csv de la catégorie
                    with open("CSV/" + category_title + '.csv', 'a', encoding='utf-8') as csv_file:
                                writer = csv.DictWriter(csv_file, fieldnames=file_header)
                                writer.writerow(book_dictionary)

                break #Ne prendre qu'un seul livre par catégorie pour racourcir le temps d'essai
            
            #Modifie l'URL pour demander la page suivante
            page_number +=1
            category_url = category_url.replace('index', 'page-' + str(page_number))
            category_url = category_url.replace(str(page_number - 1), str(page_number))
            category_response = requests.get(category_url)

        ###break #Ne faire que la première catégorie pour raccourcir le tempss