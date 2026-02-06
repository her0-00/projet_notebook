"""
📝 **Instructions** :
- Installez toutes les bibliothèques nécessaires en fonction des imports présents dans le code, utilisez la commande suivante :conda create -n projet python pandas numpy ..........
- Complétez les sections en écrivant votre code où c’est indiqué.
- Ajoutez des commentaires clairs pour expliquer vos choix.
- Utilisez des emoji avec windows + ;
- Interprétez les résultats de vos visualisations (quelques phrases).
"""

### 1. Importation des librairies et chargement des données
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Chargement des données
import kagglehub

# Télécharger le dataset
path = kagglehub.dataset_download("arnabchaki/data-science-salaries-2023")

# Charger le fichier CSV
df = pd.read_csv(os.path.join(path, "ds_salaries.csv"))



### 2. Exploration visuelle des données
#votre code 
st.title("📊 Visualisation des Salaires en Data Science")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")


if st.checkbox("Afficher un aperçu des données"):
    st.write(df.head())


#Statistique générales avec describe pandas 
st.subheader("📌 Statistiques générales")
st.write(df.describe())



### 3. Distribution des salaires en France par rôle et niveau d'expérience, uilisant px.box et st.plotly_chart
st.subheader("📈 Distribution des salaires en France")
df_france = df[df['company_location'] == 'FR']
fig = px.box(df_france, x='experience_level', y='salary_in_usd', color='experience_level')
st.plotly_chart(fig)




### 4. Analyse des tendances de salaires :
#### Salaire moyen par catégorie : en choisisant une des : ['experience_level', 'employment_type', 'job_title', 'company_location'], utilisant px.bar et st.selectbox
st.subheader("💼 Salaire moyen par catégorie")
categorie = st.selectbox("Choisir une catégorie", ['experience_level', 'employment_type', 'job_title', 'company_location'])
salaire_moyen = df.groupby(categorie)['salary_in_usd'].mean().reset_index()
fig = px.bar(salaire_moyen, x=categorie, y='salary_in_usd')
st.plotly_chart(fig) 



### 5. Corrélation entre variables
# Sélectionner uniquement les colonnes numériques pour la corrélation
st.subheader("🔗 Corrélations entre variables numériques")
df_numeric = df.select_dtypes(include=[np.number])

# Calcul de la matrice de corrélation
corr_matrix = df_numeric.corr()

# Affichage du heatmap avec sns.heatmap
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)




### 6. Analyse interactive des variations de salaire
# Une évolution des salaires pour les 10 postes les plus courants
st.subheader("📉 Évolution des salaires pour les postes courants")
top_jobs = df['job_title'].value_counts().head(10).index
df_top = df[df['job_title'].isin(top_jobs)]
salaire_evolution = df_top.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
fig = px.line(salaire_evolution, x='work_year', y='salary_in_usd', color='job_title')
st.plotly_chart(fig) 





### 7. Salaire médian par expérience et taille d'entreprise
# utilisez median(), px.bar
st.subheader("🏢 Salaire médian par expérience et taille d'entreprise")
salaire_median = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median().reset_index()
fig = px.bar(salaire_median, x='experience_level', y='salary_in_usd', color='company_size', barmode='group')
st.plotly_chart(fig) 




### 8. Ajout de filtres dynamiques
#Filtrer les données par salaire utilisant st.slider pour selectionner les plages
st.subheader("🎚️ Filtrage par salaire")
min_sal, max_sal = st.slider("Sélectionnez la plage de salaire", int(df['salary_in_usd'].min()), int(df['salary_in_usd'].max()), (int(df['salary_in_usd'].min()), int(df['salary_in_usd'].max())))
df_filtered = df[(df['salary_in_usd'] >= min_sal) & (df['salary_in_usd'] <= max_sal)]
st.write(f"Nombre d'enregistrements : {len(df_filtered)}")
st.write(df_filtered) 




### 9.  Impact du télétravail sur le salaire selon le pays
st.subheader("🏠 Impact du télétravail sur le salaire")
salaire_remote = df.groupby(['company_location', 'remote_ratio'])['salary_in_usd'].mean().reset_index()
fig = px.bar(salaire_remote, x='company_location', y='salary_in_usd', color='remote_ratio', barmode='group')
st.plotly_chart(fig)




### 10. Filtrage avancé des données avec deux st.multiselect, un qui indique "Sélectionnez le niveau d'expérience" et l'autre "Sélectionnez la taille d'entreprise"
st.subheader("🔍 Filtrage avancé")
experience = st.multiselect("Sélectionnez le niveau d'expérience", df['experience_level'].unique(), default=df['experience_level'].unique())
taille = st.multiselect("Sélectionnez la taille d'entreprise", df['company_size'].unique(), default=df['company_size'].unique())
df_filtre = df[(df['experience_level'].isin(experience)) & (df['company_size'].isin(taille))]
st.write(f"Nombre d'enregistrements filtrés : {len(df_filtre)}")
st.write(df_filtre) 

