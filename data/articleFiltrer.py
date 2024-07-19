import pandas as pd

# Lire le fichier CSV avec l'encodage approprié
df = pd.read_csv('article.csv', delimiter=";", encoding='latin-1')

# Renommer les colonnes
df = df.rename(columns={'Désignation': 'ProductSubcategoryName', 'Marque': 'ProductCategoryName', 'Famille': 'ProductName', 'Marge': 'ProfitAmount', 'Prix de vente HT': 'SaleAmount', 'Stock': 'SalesQuantity'})

# Calculer le SaleAmount sans la TVA
df['SaleAmount'] = df['SaleAmount'] / (1 + df['TVA'] / 100)

# Sélectionner les colonnes souhaitées
df = df[['ProductSubcategoryName', 'ProductCategoryName', 'ProductName', 'ProfitAmount', 'SaleAmount', 'SalesQuantity']]

# Supprimer les lignes vides
df_sans_vide = df.dropna(how='all')

# Supprimer les lignes avec des valeurs NaN dans la colonne 'ProductName'
df_sans_vide = df_sans_vide[~df_sans_vide['ProductName'].isna()]

# Ajouter la colonne 'ArticleKey'
df_sans_vide['ArticleKey'] = list(range(len(df_sans_vide)))
df_sans_vide['SalesQuantity'] = abs(df_sans_vide['SalesQuantity']) 

# Afficher le DataFrame
print(df_sans_vide)

# Enregistrer le DataFrame sans les lignes vides dans un nouveau fichier CSV
df_sans_vide.to_csv('filted_article.csv', index=False, encoding='latin-1')