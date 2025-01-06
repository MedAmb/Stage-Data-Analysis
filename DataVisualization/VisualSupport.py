import pandas as pd
import matplotlib.pyplot as plt

# Charger les données depuis un fichier JSON
tweets_df = pd.read_json('../DataAnalysis/analysis_result/Test.json')

# Filtrer les tweets ayant le résultat "support"
tweets_support = tweets_df[tweets_df['Result'] == 'support'].copy()
tweets_oppose = tweets_df[tweets_df['Result'] == 'oppose'].copy()

# Convertir la colonne 'time' en format datetime
tweets_support['time'] = pd.to_datetime(tweets_support['time'], errors='coerce')
tweets_oppose['time'] = pd.to_datetime(tweets_oppose['time'], errors='coerce')

# Enlever les informations de fuseau horaire
tweets_support['time'] = tweets_support['time'].dt.tz_localize(None)
tweets_oppose['time'] = tweets_oppose['time'].dt.tz_localize(None)

# Vérification des données
if tweets_support['time'].isnull().any() or tweets_oppose['time'].isnull().any():
    print("Certaines dates n'ont pas pu être converties.")

# Filtrer les tweets entre deux dates spécifiques
start_date = pd.Timestamp('2023-10-07')
end_date = pd.Timestamp('2024-12-31')
tweets_support_filtered = tweets_support[(tweets_support['time'] >= start_date) & (tweets_support['time'] <= end_date)]
tweets_oppose_filtered = tweets_oppose[(tweets_oppose['time'] >= start_date) & (tweets_oppose['time'] <= end_date)]

# Créer une nouvelle colonne pour déterminer la période de 30 jours
tweets_support_filtered['period_30days'] = tweets_support_filtered['time'].apply(
    lambda x: pd.Timestamp(year=x.year, month=x.month, day=1) + pd.Timedelta(days=(x.day - 1) // 30 * 30))
tweets_oppose_filtered['period_30days'] = tweets_oppose_filtered['time'].apply(
    lambda x: pd.Timestamp(year=x.year, month=x.month, day=1) + pd.Timedelta(days=(x.day - 1) // 30 * 30))

# Compter les tweets dans chaque période de 30 jours
support_count = tweets_support_filtered.groupby(['period_30days']).size().reset_index(name='count')
oppose_count = tweets_oppose_filtered.groupby(['period_30days']).size().reset_index(name='count')

# Lissage des données avec une moyenne mobile sur 5 périodes
support_count['smoothed_count'] = support_count['count'].rolling(window=5).mean()
oppose_count['smoothed_count'] = oppose_count['count'].rolling(window=5).mean()

# Supprimer les NaN après le lissage (les premières valeurs peuvent être NaN)
support_count = support_count.dropna(subset=['smoothed_count'])
oppose_count = oppose_count.dropna(subset=['smoothed_count'])

# Tracer les courbes lissées
plt.figure(figsize=(10, 6))

# Tracer l'évolution des tweets "support"
plt.plot(support_count['period_30days'], support_count['smoothed_count'], label='Support', color='blue', marker='o', linestyle='-', markersize=6)

# Tracer l'évolution des tweets "oppose"
plt.plot(oppose_count['period_30days'], oppose_count['smoothed_count'], label='Oppose', color='red', marker='x', linestyle='-', markersize=6)

# Ajouter des éléments de présentation
plt.xlabel('Période de 30 jours')
plt.ylabel('Nombre de tweets')
plt.title('Évolution des tweets "Support et oppose" par période de 30 jours (7 octobre 2023 - 31 décembre 2024)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Résultat')
plt.tight_layout()

# Afficher le graphique
plt.show()
