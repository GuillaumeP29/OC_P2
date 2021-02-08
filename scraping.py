import requests
from bs4 import BeautifulSoup

book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" #product_page_url


response = requests.get(book_url) #Récupération du code HTML d'un livre grâce à une requête sur son URL
if response.ok: #Vérification que la requête a réussi
    print(response) #Affichage du status de la requête
    book_soup = BeautifulSoup(response.text, 'lxml') #Création du soup à partir du code HTML obtenu

    #Récupération des données souhaitées
    book_title = book_soup.find(class_="col-sm-6 product_main").find('h1').text #title
    

    #Affichage des données récoltées dans la console
    print(book_url)
    print(book_title)
    