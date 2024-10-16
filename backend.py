# backend.py
from itertools import combinations
from collections import Counter
from unidecode import unidecode
import itertools


def generer_mots_possibles(lettres):
    """Générer toutes les combinaisons possibles à partir des lettres fournies."""
    # Convertir les lettres accentuées en lettres sans accent et mettre en majuscules
    lettres = unidecode(lettres).upper()
    mots_possibles = set()

    # Compter les occurrences de chaque lettre
    compteur = Counter(lettres)

    # Générer des mots de 1 à la longueur des lettres
    for longueur in range(1, len(lettres) + 1):
        # Générer toutes les combinaisons de lettres avec la longueur spécifiée
        for comb in itertools.combinations(compteur.keys(), longueur):
            # Générer les permutations pour chaque combinaison
            for perm in itertools.permutations(comb):
                # Construire le mot en respectant le compteur
                mot = ""
                temp_compteur = compteur.copy()  # Créer une copie du compteur pour gérer les lettres utilisées
                for lettre in perm:
                    if temp_compteur[lettre] > 0:
                        mot += lettre
                        temp_compteur[lettre] -= 1
                
                if mot:  # S'assurer que le mot n'est pas vide
                    mots_possibles.add(mot)

    return mots_possibles

def rechercher_mots_valides(mots_possibles, fichier_mots):
    """
    Rechercher les mots valides dans le fichier de mots français ou autre dictionnaire latin.
    """
    mots_valides = set()
    try:
        with open(fichier_mots, "r", encoding="utf-8") as f:
            # Convertir les mots du fichier en majuscules et sans accent pour un accès plus rapide
            mots_dictionnaire = set(unidecode(mot.strip()).upper() for mot in f)

        # Comparer les mots possibles sans accent avec les mots du dictionnaire
        mots_valides = mots_possibles.intersection(mots_dictionnaire)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_mots} est introuvable.")
    return mots_valides

def enregistrer_resultats(mots_valides, nom_fichier="resultats_mots.txt"):
    """
    Enregistrer les mots valides dans un fichier .txt.
    """
    with open(nom_fichier, "w", encoding="utf-8") as f:
        for mot in sorted(mots_valides):
            f.write(mot + "\n")
    print(f"Les mots valides ont été enregistrés dans {nom_fichier}.")
