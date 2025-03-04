<h1 align="center">Analyse des trajectoires des skippers<br>du Vendée Globe avec Python et Folium</h1>

Ce projet analyse et visualise les trajectoires des bateaux du Vendée Globe, en exploitant des données géospatiales pour suivre leurs déplacements et détecter les traversées de zones à risque. L'approche combine le traitement des données en Python avec la visualisation interactive sur carte.

*Les mots clés : SIG, Python, Pandas, Folium, Shapely, Cartographie, MapBox, API*

Points clés :
- Traitement des données géospatiales : Chargement et prétraitement des données GPS des skippers à partir de fichiers CSV.
- Visualisation interactive : Création d'une carte interactive des trajets avec Folium.
- Analyse des zones à risque : Utilisation de Shapely pour détecter les skippers entrant dans une zone spécifique (ex. : autour des îles Canaries).
- Organisation des données temporelles : Agrégation et tri des trajets pour une lecture chronologique.
- Extraction et transformation des coordonnées : Conversion des coordonnées au format décimal pour standardiser les données.
- Résultats visuels : Génération d'une carte interactive affichant les parcours et les points d'entrée dans les zones à risque.

Fonctionnalités
- Pandas – Chargement et manipulation des données issues des fichiers CSV (nettoyage, tri, formatage des dates).
- Folium – Création de la carte interactive et ajout des trajets des skippers.
- Shapely – Analyse spatiale des itinéraires pour identifier les passages dans les zones à risque.



