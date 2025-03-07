import pandas as pd
import folium

# Fonction pour convertir les coordonnées en format décimal
def convertir_en_decimal(coord):
    try:
        coord = coord.replace("'", "").strip()  # Supprime les symboles '
        degres, minutes = coord[:-1].split('°')  # Sépare les degrés et les minutes
        direction = coord[-1]  # Le dernier caractère 
        decimal = float(degres) + float(minutes) / 60
        if direction in ['S', 'W']:
            decimal = -decimal
        return decimal
    except Exception as e:
        print(f"Erreur")
        return None

fichiers = [
    'vendeeglobe_leaderboard_20241110_start.csv',
    'vendeeglobe_leaderboard_20241112_03.csv',
    'vendeeglobe_leaderboard_20241112_23.csv',
    'vendeeglobe_leaderboard_20241113_23.csv',
    'vendeeglobe_leaderboard_20241114_23.csv',
    'vendeeglobe_leaderboard_20241115_03.csv',
    'vendeeglobe_leaderboard_20241115_23.csv',
    'vendeeglobe_leaderboard_20241120_03.csv',
    'vendeeglobe_leaderboard_20241120_23.csv',
    'vendeeglobe_leaderboard_20241125_03.csv',
    'vendeeglobe_leaderboard_20241125_23.csv'
]

#carte = folium.Map(location=[46.0, -2.0], zoom_start=5)
#carte = folium.Map(location=[46.0, -2.0], zoom_start=5, tiles="CartoDB dark_matter")
carte = folium.Map(location=[46.0, -2.0], zoom_start=5, tiles="Esri.WorldImagery")

toutes_donnees = []

for chemin_fichier in fichiers:
    # Extraction de la date à partir du nom du fichier
    date = chemin_fichier.split('_')[2]  # Par exemple, '20241110'
    date = pd.to_datetime(date, format='%Y%m%d').strftime('%Y-%m-%d')  # Conversion au format 'YYYY-MM-DD'

    # Détermination de l'heure à partir du nom du fichier
    if '03' in chemin_fichier:
        heure = '03:00'
    elif '23' in chemin_fichier:
        heure = '23:00'
    else:
        heure = '00:00'  

    # Chargement du fichier
    df = pd.read_csv(chemin_fichier, sep=';', encoding='latin1', header=0)
    df.columns = df.columns.str.strip()  # Suppression des espaces dans les noms de colonnes
    df.rename(columns={'Latitude Latitude': 'Latitude', 'Longitude Longitude': 'Longitude'}, inplace=True)

    df = df.dropna(subset=['Latitude', 'Longitude'])  # Suppression des lignes avec des valeurs manquantes
    df['Latitude'] = df['Latitude'].astype(str).apply(convertir_en_decimal)  # Conversion de la latitude
    df['Longitude'] = df['Longitude'].astype(str).apply(convertir_en_decimal)  # Conversion de la longitude

    # Création de la colonne pour l'horodatage complet
    df['Date'] = date
    df['Heure'] = heure
    df['Horodatage'] = pd.to_datetime(df['Date'] + ' ' + df['Heure'])  # Fusion date et heure

    toutes_donnees.append(df)

# Fusion de toutes les données
df_complet = pd.concat(toutes_donnees)

# Tri des données par bateau et par horodatage
df_complet = df_complet.sort_values(by=['Skipper / Bateau', 'Horodatage'])

# Liste des bateaux 
tous_bateaux = df_complet['Skipper / Bateau'].unique()

# Regroupement des bateaux par groupes de 5
groupes = [tous_bateaux[i:i + 5] for i in range(0, len(tous_bateaux), 5)]

# Création des couches
for idx, groupe in enumerate(groupes, start=1):
    couche_groupe = folium.FeatureGroup(name=f'Groupe {idx}', show=(idx == 1))  # Affiché par défaut
    
    # Traitement des bateaux dans le groupe
    for bateau in groupe:
        donnees_groupe = df_complet[df_complet['Skipper / Bateau'] == bateau]

        # Trajet
        coordonnees = donnees_groupe[['Latitude', 'Longitude']].values.tolist()

        # Ligne représentant le trajet
        folium.PolyLine(
            locations=coordonnees,
            color='lightgrey', 
            weight=1.5,
            opacity=0.7,
            dash_array=[5, 5],
            popup=f"Trajet du bateau : {bateau}"
        ).add_to(couche_groupe)

        # Points du trajet
        for _, ligne in donnees_groupe.iterrows():
            color = (
                "black" if ligne['Heure'] == "00:00" 
                else "lightblue" if ligne['Heure'] == "03:00" 
                else "blue"
            )
            
            popup_text = folium.Popup(
                f"Bateau : {bateau}<br>Date : {ligne['Date']}<br>Heure : {ligne['Heure']}",
                max_width=250
            )
            
            folium.CircleMarker(
                location=[ligne['Latitude'], ligne['Longitude']],
                radius=2,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=1,
                popup=popup_text
            ).add_to(couche_groupe)

    couche_groupe.add_to(carte)

# Point représentant la ville
vendee_city = [46.4963, -1.7834]

folium.CircleMarker(
    location=vendee_city,
    radius=4,  
    color="red",  
    fill=True,
    fill_color="red",  
    fill_opacity=1
).add_to(carte)

folium.map.Marker(
    [46.4963, -1.7834],  
    icon=folium.DivIcon(
        icon_size=(150, 40),
        icon_anchor=(0, 0),
        html='''
        <div style="
            font-size: 8pt;
            color: black;
            text-shadow: 2px 2px 4px white, -2px -2px 4px white;">
            Les Sables-d'Olonne (Vendée)
        </div>
        ''',
    )
).add_to(carte)


# Résultats affichés en HTML
folium.LayerControl().add_to(carte)
carte.save('vendeeglobe.html')
