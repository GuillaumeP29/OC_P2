import requests
from bs4 import BeautifulSoup

book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" #product_page_url
website_url = 'http://books.toscrape.com/'


response = requests.get(book_url) #Récupération du code HTML d'un livre grâce à une requête sur son URL
if response.ok: #Vérification que la requête a réussi
    print(response) #Affichage du status de la requête
    book_soup = BeautifulSoup(response.text, 'lxml') #Création du soup à partir du code HTML obtenu

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


    
    book_dictionary["product_page_url"] = book_url
    book_dictionary["universal_product_code"] = book_table_dictionary["UPC"]
    book_dictionary["title"] = book_title
    book_dictionary["price_including_tax"] = book_table_dictionary["Price (incl. tax)"]
    book_dictionary["price_excluding_tax"] = book_table_dictionary["Price (excl. tax)"]
    book_dictionary["number_available"] = book_table_dictionary["Availability"]
    book_dictionary["product_description"] = book_description
    book_dictionary["category"] = '?'
    book_dictionary["review_rating"] = '?'
    book_dictionary["image_url"] = book_image

    #Affichage des données récoltées dans la console
    print(book_dictionary)


    