#!/usr/bin/env python3

import sys
from geo.segment import Segment
from geo.point import Point
from geo.quadrant import Quadrant
from tycat import read_instance

def quadrants(polygons):
    # Initialise une liste pour stocker les indices des polygones, leurs aires et leurs quadrants.
    surfaces = [[i, abs(poly.area()), 0] for i, poly in enumerate(polygons)]
    
    # Parcours chaque polygone dans la liste donnée.
    for i, poly in enumerate(polygons):
        # Obtient le quadrant du polygone.
        q = poly.bounding_quadrant()
        
        # Enregistre le quadrant dans la liste des surfaces pour le polygone correspondant.
        surfaces[i][2] = q
    
    # Retourne la liste des indices des polygones, leurs aires et leurs quadrants.
    return surfaces


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
    # Initialise la liste des indices des parents de chaque polygone avec des valeurs -1.
    parent_indices = [-1] * len(polygons)
    
    # Trie les polygones par aire en ordre décroissant.
    surfaces_triees = sorted(quadrants(polygons), key=lambda x: x[1], reverse=True)
    n = len(surfaces_triees)
    
    # Si toutes les aires sont égales, il n'y a pas d'inclusions.
    if min(surfaces_triees[i][1] for i in range(n)) == max(surfaces_triees[i][1] for i in range(n)):
        return parent_indices
    
    # Parcours les polygones triés en commençant par le plus grand.
    for i in range(n - 1, 0, -1):
        tuples = surfaces_triees.pop()  # Récupère le polygone courant
        
        poly1 = polygons[tuples[0]]  # Polygone courant
        quadrant1 = tuples[2]  # Quadrant du polygone courant
        point = poly1.points[0].coordinates  # Premier point du polygone courant
        surface1 = tuples[1]  # Aire du polygone courant
        
        # Parcours les polygones restants dans la liste triée en commençant par le plus grand.
        for j in range(0, i):
            tuples2 = surfaces_triees[i - 1 - j]
            
            poly2 = polygons[tuples2[0]]  # Polygone à comparer
            quadrant2 = tuples2[2]  # Quadrant du polygone à comparer
            surface2 = tuples2[1]  # Aire du polygone à comparer
            
            # Vérifie si le polygone courant est plus petit que le polygone à comparer
            # et s'il y a intersection entre les quadrants
            # et si un point du polygone courant est à l'intérieur du polygone à comparer.
            if surface1 < surface2 and quadrant1.intersect(quadrant2) and point_in_polygon(point, poly2):
                # Enregistre l'indice du polygone à comparer comme parent du polygone courant.
                parent_indices[tuples[0]] = tuples2[0]
                break
    
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
