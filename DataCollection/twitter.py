import sys
import os
from datetime import datetime, timedelta
import time
# le chemin du dossier
sys.path.append(os.path.abspath('../External/scrapper'))

# 1. importer twitter scraper
from twitter_scraper import Twitter_Scraper

# 2. initialiser des variables user_name, user_mail, password

user_name=''
user_mail=''
Password=''

# 3. Initialiser un objet twitter scraper

My_scrape=Twitter_Scraper(mail=user_mail,username=user_name, password=Password,
max_tweets=1000, scrape_top= True)

# 4. utiliser l'objet twitter scraper pour connecter a twitter
My_scrape.login()


# 5. creer string qui pourra nous donner  1000 tweet qui ont le  hachttag #gaza pour chaque mois de
#07oct2023-07oct2024 en 2 langues arabe et anglais

start_date = datetime(2024, 10, 18)
end_date = datetime(2023, 10, 7)
query_base = '(Gaza OR palestine OR 07oct OR israel) '

i = 1
# Boucle à travers chaque mois
while start_date > end_date:
    next_month = start_date - timedelta(days=30)  # On ajoute un mois
    month_end = max(next_month, end_date)
    Query= query_base + 'lang:en ' + f'since:{next_month} '.split(' ')[0] + ' ' + f'until:{start_date} '.split(' ')[0]
    Query_AR= query_base + 'lang:ar ' + f'since:{next_month} '.split(' ')[0] + ' ' + f'until:{start_date} '.split(' ')[0]

    # Passer au mois suivant
    start_date=next_month
    print('scraping tweets for query ', Query)

    My_scrape.scrape_tweets(scrape_query=Query,max_tweets=1000)
    My_scrape.save_to_json(str(i) + "_EN")
    time.sleep(60)
    print('scraping tweets for query ', Query_AR)
    My_scrape.scrape_tweets(scrape_query=Query_AR,max_tweets=1000)
    My_scrape.save_to_json(str(i) + "_AR")
    time.sleep(60)
    i += 1