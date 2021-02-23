## Créer l'environnement virtuel afin de pouvoir exécuter le programme de scraping du site book.toscrape :

1. Dans le terminal, se rendre jusqu'au dossier ou est enregistré le programme.
2. \
_**Windows :**_ \
créer l'environnement virtuel avec la commande du terminal suivante : "python -m venv env" \
_**Linux :**_ \
créer l'environnement virtuel avec la commande du terminal suivante : "python3 -m venv env"
3. \
_**Windows :**_ \
Activer l'environnement virutel depuis le terminal grâce à la commande suivante : "env/scripts/activate" \
_**Linux :**_ \
Activer l'environnement virutel depuis le terminal grâce à la commande suivante : "source myvenv/bin/activate"
4. Une fois l'environnement virtuel activé, lancer le téléchargements des modules indiqués dans le fichier requirements à l'aide de la commande suivante : "pip install -r requirements.txt"
5. Créer deux dossiers vides : "CSV" et "Images" pour le bon déroulement du script.
6. Lancer le scripts à l'aide de la commande : "python scraping.py"