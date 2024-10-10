# frontend.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from backend import generer_mots_possibles, rechercher_mots_valides, enregistrer_resultats

# Variable globale pour stocker le chemin et le nom du fichier dictionnaire
dictionnaire_fichier = None

def choisir_dictionnaire():
    """Ouvre une boîte de dialogue pour sélectionner le fichier dictionnaire."""
    global dictionnaire_fichier
    dictionnaire_fichier = filedialog.askopenfilename(
        title="Choisir un fichier dictionnaire",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    
    if dictionnaire_fichier:
        # Extraire le nom du fichier sans le chemin complet
        nom_fichier = dictionnaire_fichier.split("/")[-1]
        messagebox.showinfo("Dictionnaire sélectionné", f"Dictionnaire sélectionné : {nom_fichier}")
        # Mettre à jour le label avec le nom du fichier sélectionné
        lbl_dictionnaire_selectionne.config(text=f"Dictionnaire : {nom_fichier}")
    else:
        messagebox.showwarning("Aucun fichier sélectionné", "Veuillez choisir un fichier dictionnaire valide.")

def rechercher():
    """Exécute la recherche de mots valides et met à jour l'interface avec les résultats."""
    if not dictionnaire_fichier:
        messagebox.showwarning("Dictionnaire manquant", "Veuillez choisir un fichier dictionnaire avant de rechercher.")
        return

    lettres = entry_lettres.get().strip()
    if not lettres:
        messagebox.showwarning("Champ vide", "Veuillez entrer des lettres pour rechercher.")
        return

    # Générer les mots possibles à partir des lettres saisies
    mots_possibles = generer_mots_possibles(lettres)
    
    # Rechercher les mots valides dans le dictionnaire
    mots_valides = rechercher_mots_valides(mots_possibles, dictionnaire_fichier)
    
    # Mettre à jour la liste des résultats
    result_box.delete("1.0", "end")  # Effacer les anciens résultats
    if mots_valides:
        result_box.insert("end", "\n".join(sorted(mots_valides)))
    else:
        result_box.insert("end", "Aucun mot valide trouvé.")

def enregistrer_resultat():
    """Enregistre les résultats de la recherche dans un fichier .txt choisi par l'utilisateur."""
    mots_valides = result_box.get("1.0", "end").strip()
    if not mots_valides or mots_valides == "Aucun mot valide trouvé.":
        messagebox.showinfo("Pas de résultat", "Aucun résultat à enregistrer.")
        return

    # Ouvrir la boîte de dialogue pour choisir le nom et le dossier de sauvegarde
    fichier_enregistrement = filedialog.asksaveasfilename(
        title="Enregistrer les résultats",
        defaultextension=".txt",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
        initialfile="resultats_mots.txt"
    )
    
    if fichier_enregistrement:
        # Enregistrer les résultats dans le fichier choisi par l'utilisateur
        enregistrer_resultats(mots_valides.splitlines(), fichier_enregistrement)
        messagebox.showinfo("Succès", f"Les résultats ont été enregistrés avec succès dans {fichier_enregistrement}!")
    else:
        messagebox.showwarning("Annulé", "L'enregistrement a été annulé.")

def effacer_champs():
    """Efface les champs de saisie et de résultats."""
    entry_lettres.delete(0, "end")
    result_box.delete("1.0", "end")
    lbl_dictionnaire_selectionne.config(text="Aucun dictionnaire sélectionné.")

# Créer l'interface principale avec ttkbootstrap
root = ttk.Window(themename="darkly")
root.title("WORDS MASTER")

# Grand Titre
titre = ttk.Label(root, text="WORDS MASTER", font=("Helvetica", 24, "bold"))
titre.pack(pady=20)

# Bouton pour sélectionner le dictionnaire
btn_choisir_dico = ttk.Button(root, text="Choisir le Dictionnaire", bootstyle="info", command=choisir_dictionnaire)
btn_choisir_dico.pack(pady=10)

# Label affichant le dictionnaire sélectionné
lbl_dictionnaire_selectionne = ttk.Label(root, text="Aucun dictionnaire sélectionné.", font=("Helvetica", 12))
lbl_dictionnaire_selectionne.pack(pady=5)

# Champ de saisie + Bouton de recherche
frame_search = ttk.Frame(root)
frame_search.pack(pady=10)

entry_lettres = ttk.Entry(frame_search, width=30, font=("Helvetica", 14))
entry_lettres.pack(side=LEFT, padx=5)

btn_rechercher = ttk.Button(frame_search, text="Rechercher", bootstyle="success", command=rechercher)
btn_rechercher.pack(side=LEFT, padx=5)

# Champ de résultats (Text Widget)
result_box = ttk.Text(root, height=15, width=50, font=("Helvetica", 12))
result_box.pack(pady=20)

# Boutons d'actions (Enregistrer, Effacer)
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

btn_enregistrer = ttk.Button(frame_buttons, text="Enregistrer", bootstyle="primary", command=enregistrer_resultat)
btn_enregistrer.pack(side=LEFT, padx=10)

btn_effacer = ttk.Button(frame_buttons, text="Effacer", bootstyle="danger", command=effacer_champs)
btn_effacer.pack(side=LEFT, padx=10)

# Démarrer l'application
root.mainloop()
