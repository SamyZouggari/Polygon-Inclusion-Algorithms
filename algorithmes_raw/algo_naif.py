#!/usr/bin/env python3

import sys
from geo.segment import Segment
from geo.point import Point
from tycat import read_instance


def point_in_polygon(point, polygon):
    """
    Voir si un point est inclus dans un polygone en utilisant l'algorithme de Ray Casting, voir rapport.
    """
    cpt = 0  # Initialise le compteur du nombre d'intersections
    x, y = point  # Coordonnées du point
    segments = polygon.segments()  # Obtient les segments du polygone
    
    # Itération sur tous les segments du polygone
    for segment in segments:
        x1, y1 = segment.endpoints[0].coordinates  # Coordonnées du premier point du segment
        x2, y2 = segment.endpoints[1].coordinates  # Coordonnées du deuxième point du segment
        
        if min(y1, y2) < y <= max(y1, y2):  # Vérifie si le point est dans la plage verticale du segment
            if x < min(x1, x2):  # Vérifie si le point est à gauche du segment
                cpt += 1  # Incrémente le compteur d'intersections
            else:
                # Calcule le point d'intersection potentiel avec le segment
                x_intersection = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if x < x_intersection:  # Vérifie si le point est à gauche de l'intersection
                    cpt += 1  # Incrémente le compteur d'intersections
    
    # Vérifie si le nombre d'intersections est impair pour déterminer l'inclusion du point dans le polygone, voir rapport
    return cpt % 2 == 1

def detect_inclusion(polygons):
    "Fonction principale pour la détection d'inclusion des polygones en entrée."
    
    # Initialise une liste avec des valeurs -1, qui sera remplie avec les indices des polygones inclus.
    parent_indices = [-1] * len(polygons) 
    
    # Itération sur chaque polygone.
    for i, poly1 in enumerate(polygons):
        
        # Initialise une liste pour stocker les polygones qui incluent le polygone actuel.
        polygones_inclus = []  
        
        # Itération sur tous les autres polygones pour comparer avec le polygone actuel.
        for j, poly2 in enumerate(polygons):
            
            # Vérifie si le polygone actuel a une aire plus petite que le polygone j
            # et si un point du polygone actuel est à l'intérieur du polygone j.
            if abs(poly1.area()) < abs(poly2.area()) and i != j and point_in_polygon(poly1.points[0].coordinates, poly2):
                
                # Ajoute le tuple (indice du polygone, aire absolue du polygone) à la liste.
                polygones_inclus.append((j, abs(poly2.area()))) 

        # Vérifie s'il y a des polygones inclus dans la liste.
        if polygones_inclus:
            # Itération sur les tuples pour trouver le polygone inclus avec l'aire minimale.
            for k, tuples in enumerate(polygones_inclus):
                # Si l'aire de ce polygone inclus est la plus petite parmi les polygones inclus, 
                # son indice est enregistré comme parent du polygone courant.
                if tuples[1] == min(polygones_inclus[l][1] for l in range(len(polygones_inclus))):
                    parent_indices[i] = tuples[0]  

    # Retourne la liste des indices des parents de chaque polygone.
    return parent_indices


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = detect_inclusion(polygones)
        print(inclusions)

if __name__=="__main__":
    main()
