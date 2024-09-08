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
    # Crée une liste de tuples contenant l'indice du polygone et son aire.
    surfaces = [(i, abs(poly.area())) for i, poly in enumerate(polygons)]
    
    # Trie la liste des surfaces en fonction de l'aire.
    surfaces_triees = sorted(surfaces, key=lambda x: x[1])
    
    # Initialise la liste des indices des parents de chaque polygone.
    parent_indices = [-1] * len(polygons)
    
    # Parcours la liste triée des surfaces.
    for i, tuples in enumerate(surfaces_triees):
        # Récupère le polygone correspondant à l'indice dans la liste triée.
        poly1 = polygons[tuples[0]]
        
        # Récupère le premier point du polygone.
        point = poly1.points[0].coordinates
        
        # Parcours les polygones restants dans la liste triée.
        for j in range(i + 1, len(surfaces_triees)):
            # Récupère le polygone correspondant à l'indice dans la liste triée.
            poly2 = polygons[surfaces_triees[j][0]]
            
            # Vérifie si le point du polygone i est à l'intérieur du polygone j.
            if point_in_polygon(point, poly2):
                # Si c'est le cas, enregistre l'indice du polygone 2 comme parent du polygone 1.
                parent_indices[surfaces_triees[i][0]] = surfaces_triees[j][0]
                break  # Arrête la boucle une fois qu'un parent a été trouvé.
    
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

