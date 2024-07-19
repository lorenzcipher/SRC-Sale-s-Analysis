from random import randrange
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Lire le fichier CSV avec l'encodage approprié
client_df = pd.read_csv('filted_client.csv', delimiter=",", encoding='latin-1')

# Lire le fichier CSV avec l'encodage approprié
articles_df = pd.read_csv('filted_article.csv', delimiter=",", encoding='latin-1')



# Create a new empty dataframe to store the results
result_df = pd.DataFrame(columns=client_df.columns.tolist() + articles_df.columns.tolist())

# Iterate through each client and generate 2 rows with different articles
for client_id, client_row in client_df.iterrows():
    articles_subset = articles_df.sample(randrange(3))
    for article_id, article_row in articles_subset.iterrows():
        new_row = {**client_row.to_dict(), **article_row.to_dict()}
        #print(new_row)
        result_df.loc[len(result_df)] = new_row
        #result_df = result_df.append(new_row, ignore_index=True)


result_df = result_df.reindex(columns=['SalesKey', 'DateKey', 'SalesQuantity','SaleAmount','ProfitAmount','Region','States','ProductName','ProductCategoryName','ProductSubcategoryName','Feedback'])


# Remplacer les 0 par la valeur minimale de la colonne 'column_name'
min_value = result_df['SalesQuantity'].min() +1
result_df['SalesQuantity'] = result_df['SalesQuantity'].replace([0.0, np.nan], min_value)
print(result_df.dtypes)

# Change the data type of a specific column
result_df['SalesKey'] = result_df['SalesKey'].astype('int')
result_df['DateKey'] = pd.to_datetime(result_df['DateKey'], format='%Y-%m-%d %H:%M')
result_df['SalesQuantity'] = result_df['SalesQuantity'].astype('int')
result_df['SaleAmount'] = result_df['SaleAmount'].astype('float')
result_df['ProfitAmount'] = result_df['ProfitAmount'].astype('float')
result_df['Feedback'] = result_df['Feedback'].astype('int')
result_df['SaleAmount'] = result_df['SaleAmount'].round(2)
# Display the result dataframe
print(result_df)

print(result_df.isnull().sum())
result_df = result_df.dropna(axis=0, how='any')
print(result_df.isnull().sum())
result_df = result_df.drop_duplicates()
# Drop rows where the value of 'column_name' is 0
result_df = result_df[result_df['Region'] != '0']
result_df = result_df[result_df['SaleAmount'] != 0]
result_df = result_df[result_df['States'].notnull()]
print(result_df.dtypes)
print(result_df.shape)





# Enregistrer le DataFrame sans les lignes vides dans un nouveau fichier CSV
result_df.to_csv('dataset.csv', index=False,encoding='UTF-8')