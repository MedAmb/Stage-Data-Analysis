import pandas as pd
import matplotlib.pyplot as plt

# Charger les données depuis un fichier JSON
tweets_df = pd.read_json('../DataAnalysis/analysis_result/Test.json')

# Filtrer les tweets ayant le résultat "support"
tweets_support = tweets_df[tweets_df['Result'] == 'support'].copy()  # Créez une copie explicite pour éviter le warning
print(tweets_support)
# Convertir la colonne 'time' en format datetime (avec vérification)
tweets_support['time'] = pd.to_datetime(tweets_support['time'], errors='coerce')  # Utiliser 'coerce' pour gérer les erreurs

# Vérifiez si la conversion a fonctionné
if tweets_support['time'].isnull().any():
    print("Attention : certaines valeurs de 'time' n'ont pas pu être converties en datetime.")

# Extraire la date des tweets (assurez-vous que 'time' est bien un datetime)
tweets_support['date'] = tweets_support['time'].dt.date

# Créer une plage de dates allant du 7 octobre 2023 au 31 décembre 2024 avec un intervalle de 30 jours
date_range = pd.date_range(start="2023-10-07", end="2024-12-31", freq="30D")

# Reindexer les données pour inclure toutes les dates
tweets_count = tweets_support.groupby('date').size()
print(tweets_count)
tweets_count = tweets_count.reindex(date_range, fill_value=0)
print(tweets_count)
# Tracer la courbe des tweets "support" avec des mois (plage de 30 jours)
plt.figure(figsize=(10, 6))
plt.plot(tweets_count.index, tweets_count.values, label="Tweets 'Support'", color="blue")
plt.xlabel('Date')
plt.ylabel('Nombre de tweets')
plt.title('Évolution des tweets "Support" par période de 30 jours')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
