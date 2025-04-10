<h1 align="center">Analyse des trajectoires des skippers<br>du Vendée Globe avec Python (Folium)</h1>

Ce projet analyse et visualise les trajectoires des bateaux du Vendée Globe, en exploitant des données géospatiales pour suivre leurs déplacements et détecter les traversées de zones à risque. L'approche combine le traitement des données en Python avec la visualisation interactive sur carte.

*Les mots clés : SIG, Python, Pandas, Folium, Shapely*

Points clés :
- Traitement des données géospatiales : Chargement et prétraitement des données GPS des skippers à partir de fichiers CSV.
- Extraction et transformation des coordonnées : Conversion des coordonnées au format décimal pour standardiser les données.
- Organisation des données temporelles : Agrégation et tri des trajets pour une lecture chronologique.
- Visualisation interactive : Création d'une carte interactive des trajets avec Folium.
- Analyse des zones à risque : Utilisation de Shapely pour détecter les skippers entrant dans une zone spécifique (ex. : autour des îles Canaries).
- Résultats visuels : Génération d'une carte interactive affichant les parcours et les points d'entrée dans les zones à risque.

Fonctionnalités
- Pandas – Chargement et manipulation des données issues des fichiers CSV (nettoyage, tri, formatage des dates).
- Folium – Création de la carte interactive et ajout des trajets des skippers.
- Shapely – Analyse spatiale des itinéraires pour identifier les passages dans les zones à risque.

Cette carte visualise les trajectoires des yachts participant au tour du monde Vendée Globe. Elle est construite à partir de **données géospatiales GPS** et utilise des outils interactifs comme Folium (Python).  
Éléments principaux de la carte :
- Point de départ – marqué par un cercle rouge dans la ville de Les Sables-d'Olonne, port officiel du départ de la course.
- Trajectoires des yachts – représentées par des lignes en pointillés, illustrant le parcours des participants à travers l’océan Atlantique.
- Points intermédiaires – leur couleur indique l'heure d'enregistrement des coordonnées :  Bleu clair (`lightblue`) – enregistré à 03:00, Bleu (`blue`) – enregistré à 23:00.
- Fenêtres interactives – en cliquant sur un point, on peut voir le nom du bateau, la date et l'heure de l'enregistrement.  

<div align="center">
    <img src="https://github.com/DariaPodlovchenko/Analyse-des-trajectoires-du-Vende-Globe/raw/main/itineraire.jpg" width="600">
</div>

Cette carte affiche uniquement le trajet d’un bateau du Vendée Globe qui traverse la zone de risque située autour des îles Canaries.
Éléments principaux de la carte :
- Point de départ – représenté par un cercle rouge à Les Sables-d'Olonne (France), port officiel du départ de la course.
- Trajectoire du bateau sélectionné – affichée en rouge en pointillés, indiquant son passage dans la zone de risque.
- Zone de risque – les îles Canaries sont entourées d’un polygone bleu pour marquer la zone à surveiller.
- Points intermédiaires – leur couleur indique l'heure d'enregistrement des coordonnées :  Bleu clair (`lightblue`) – enregistré à 03:00, Bleu (`blue`) – enregistré à 23:00.
- Fenêtres interactives – permettent d’afficher uniquement le nom du bateau en cliquant sur la trajectoire.

<div align="center">
    <img src="https://github.com/DariaPodlovchenko/Analyse-des-trajectoires-du-Vende-Globe/raw/main/zone_risque.jpg" width="600">
</div>

*Dans le dossier **VendeeGlobe**, se trouvent les **données utilisées pour la réalisation de ce project**.  
Le dossier **scripts** contient **les scripts de traitement et de génération des cartes**, notamment **`vendee_globe_tracking.py` et `zone_risque.py`**.*
