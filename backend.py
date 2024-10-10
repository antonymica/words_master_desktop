# backend.py
import itertools
from unidecode import unidecode

def generer_mots_possibles(lettres):
    """Générer toutes les combinaisons possibles à partir des lettres fournies."""
    # Convertir les lettres accentuées en lettres sans accent et mettre en majuscules
    lettres = unidecode(lettres).upper()
    mots_possibles = set()

    # Générer les permutations de toutes les longueurs possibles
    for longueur in range(1, len(lettres) + 1):
        for combinaison in itertools.permutations(lettres, longueur):
            mot = "".join(combinaison)
            mots_possibles.add(mot)

    return mots_possibles

def rechercher_mots_valides(mots_possibles, fichier_mots):
    """Rechercher les mots valides dans le fichier de mots français ou autre dictionnaire latin."""
    mots_valides = set()
    try:
        with open(fichier_mots, "r", encoding="utf-8") as f:
            # Convertir les mots du fichier en majuscules et sans accent
            mots_francais = set(unidecode(mot.strip()).upper() for mot in f)

        # Comparer les mots possibles sans accent avec les mots du dictionnaire
        mots_valides = mots_possibles.intersection(mots_francais)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_mots} est introuvable.")
    return mots_valides

def enregistrer_resultats(mots_valides, nom_fichier="resultats_mots.txt"):
    """Enregistrer les mots valides dans un fichier .txt."""
    with open(nom_fichier, "w", encoding="utf-8") as f:
        for mot in sorted(mots_valides):
            f.write(mot + "\n")
    print(f"Les mots valides ont été enregistrés dans {nom_fichier}.")
