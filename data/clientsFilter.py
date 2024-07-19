from random import random
import numpy as np
import pandas as pd

# Lire le fichier CSV avec l'encodage approprié
df = pd.read_csv('clients.csv', delimiter=";", encoding='latin-1')


df = df.rename(columns={'Ville': 'States', 'Code postal': 'Region'})


# Ajouter une nouvelle colonne avec des valeurs aléatoires entre 0 et 10
df['Feedback'] = np.random.randint(0, 11, size=len(df))

df = df[['States', 'Region', 'SalesKey','Civilité','Feedback']]




# Create a new column 'Date_Truncated' and assign the first 8 characters of the 'Date' column
df = df.assign(DateKey=df['SalesKey'].str[:8])





# Supprimer les lignes vides
df_sans_vide = df.dropna(how='all')
#Check if the 'SalesKey' column has any NaN values
if df_sans_vide['SalesKey'].isna().any():
    # Drop rows with NaN values
    df_sans_vide = df_sans_vide[~df_sans_vide['SalesKey'].isna()]

# Filter the DataFrame to keep only rows where the 'SalesKey' column matches the regex pattern
df_sans_vide = df_sans_vide[df_sans_vide['SalesKey'].str.match(r'^[0-9]*$')]

df_sans_vide['DateKey'] = pd.to_datetime(df_sans_vide['DateKey'], format='%Y%m%d').dt.strftime('%Y-%m-%d')

df_sans_vide['SalesKey'] = list(range(len(df_sans_vide)))





# Afficher le DataFrame
print(df_sans_vide)

# Enregistrer le DataFrame sans les lignes vides dans un nouveau fichier CSV
df_sans_vide.to_csv('filted_client.csv', index=False,encoding='latin-1')


