# -*-coding:Utf-8 -*
import fonctions
import urllib
import csv
import requests
from bs4 import BeautifulSoup
import re

website_url = 'http://books.toscrape.com/'
file_header = [
    "product_page_url", "universal_product_code", "title", "price_including_tax",
    "price_excluding_tax", "number_available", "product_description", "category",
    "review_rating", "image_url"
]

fonctions.website_scraping(website_url, file_header)