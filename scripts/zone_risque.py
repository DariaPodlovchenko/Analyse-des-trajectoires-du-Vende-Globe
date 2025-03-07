# Le code commence par convertir les coordonnées au format décimal pour faciliter les calculs géographiques.
# Ensuite, les données de plusieurs fichiers sont chargées, les dates et heures sont extraites des noms de fichiers,
# et les itinéraires des bateaux sont organisés dans un ordre chronologique.
# Toutes les données sont combinées dans un tableau unique et triées par bateau et par heure.
# Une zone dangereuse autour des îles Canaries est définie sous forme de polygone,
# permettant de vérifier si des points ou des itinéraires de bateaux entrent ou traversent cette zone.
# Enfin, les bateaux dans la zone et les itinéraires traversant la zone sont affichés sur la carte.

import pandas as pd
import folium
from shapely.geometry import Point, LineString, Polygon

def convertir_en_decimal(coord):
    try:
        coord = coord.replace("'", "").strip()  
        degres, minutes = coord[:-1].split('°')  
        direction = coord[-1]  
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

carte = folium.Map(location=[46.0, -2.0], zoom_start=5, tiles="Esri.WorldImagery")

toutes_donnees = []

for fichier in fichiers:
    # Extraire la date du nom du fichier
    date = fichier.split('_')[2]  
    date = pd.to_datetime(date, format='%Y%m%d').strftime('%Y-%m-%d')  # format 'YYYY-MM-DD'

    # Déterminer l'heure à partir du nom du fichier
    if '03' in fichier:
        heure = '03:00'
    elif '23' in fichier:
        heure = '23:00'
    else:
        heure = '00:00'

    # Charger le fichier
    df = pd.read_csv(fichier, sep=';', encoding='latin1', header=0)
    df.columns = df.columns.str.strip()  # Nettoyer les noms des colonnes
    df.rename(columns={'Latitude Latitude': 'Latitude', 'Longitude Longitude': 'Longitude'}, inplace=True)

    df = df.dropna(subset=['Latitude', 'Longitude'])  # Supprimer les lignes avec des valeurs manquantes
    df['Latitude'] = df['Latitude'].astype(str).apply(convertir_en_decimal)  # Convertir la latitude
    df['Longitude'] = df['Longitude'].astype(str).apply(convertir_en_decimal)  # Convertir la longitude

    # Une colonne pour la date et l'heure complètes
    df['Date'] = date
    df['Heure'] = heure
    df['DateHeure'] = pd.to_datetime(df['Date'] + ' ' + df['Heure'])  # Combiner date et heure

    toutes_donnees.append(df)

# Combiner toutes les données
df_complet = pd.concat(toutes_donnees)

# Trier les données par bateau et par date/heure
df_complet = df_complet.sort_values(by=['Skipper / Bateau', 'DateHeure'])

# îles Canaries
coords_canaries = [
    [-18.2, 27.5],  # Coin inférieur gauche
    [-13.5, 27.5],  # Coin inférieur droit
    [-13.5, 29.5],  # Coin supérieur droit
    [-18.2, 29.5],  # Coin supérieur gauche
    [-18.2, 27.5]   # Retour au point initial
]
zone_canaries = Polygon(coords_canaries)

folium.Polygon(
    locations=[[lat, lon] for lon, lat in coords_canaries],
    color='blue',
    fill=True,
    fill_opacity=0.2,
    popup="Zone dangereuse - Îles Canaries"
).add_to(carte)

# Identifier les bateaux dans la zone et les routes qui traversent la zone
bateaux_zone = set()
routes_zone = set()

# Analyser les bateaux
for bateau in df_complet['Skipper / Bateau'].unique():
    donnees_bateau = df_complet[df_complet['Skipper / Bateau'] == bateau]

    # Vérifier les points de la route
    for _, ligne in donnees_bateau.iterrows():
        point = Point(ligne['Longitude'], ligne['Latitude'])
        if point.within(zone_canaries):
            bateaux_zone.add(bateau)

    # Vérifier les routes
    if len(donnees_bateau) >= 2:
        ligne_route = LineString(donnees_bateau[['Longitude', 'Latitude']].values)
        if ligne_route.intersects(zone_canaries):
            routes_zone.add(bateau)

# Ajouter les bateaux dans la zone sur la carte
for bateau in bateaux_zone:
    folium.Marker(
        location=[df_complet[df_complet['Skipper / Bateau'] == bateau]['Latitude'].iloc[0],
                 df_complet[df_complet['Skipper / Bateau'] == bateau]['Longitude'].iloc[0]],
        popup=f"Bateau {bateau} dans la zone",
        icon=folium.Icon(color='green')
    ).add_to(carte)

# Ajouter les routes traversant la zone
for bateau in routes_zone:
    donnees_bateau = df_complet[df_complet['Skipper / Bateau'] == bateau]
    coordonnees = donnees_bateau[['Latitude', 'Longitude']].values.tolist()
    folium.PolyLine(
        locations=coordonnees,
        color='red',
        weight=2.5,
        opacity=0.7,
        dash_array=[5, 5],
        popup=folium.Popup(f"Route du bateau <b>{bateau}</b> <br> traversant la zone de risque des <b>îles Canaries</b>", max_width=250)
    ).add_to(carte)

folium.LayerControl().add_to(carte)

# Ajout des points sur la trajectoire
for _, ligne in donnees_bateau.iterrows():
    color = "black" if ligne['Heure'] == "00:00" else "lightblue" if ligne['Heure'] == "03:00" else "blue"
    folium.CircleMarker(
        location=[ligne['Latitude'], ligne['Longitude']],
        radius=3,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=1,
        popup=folium.Popup(f"Bateau : {bateau}<br>Date : {ligne['Date']}<br>Heure : {ligne['Heure']}", max_width=250)
    ).add_to(carte)

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
        icon_size=(150, 140),
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

carte.save('analyse_zone_canaries.html')