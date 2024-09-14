import tkinter as tk  # Importation de tkinter pour créer des interfaces graphiques
from PIL import Image, ImageDraw, ImageTk  # Importation de PIL pour manipuler des images
import math  # Importation du module math pour les calculs mathématiques avancés

# Fonction pour créer une image avec des coins arrondis
def creer_rectangle_arrondi(largeur, hauteur, rayon, couleur):
    # Crée une nouvelle image avec transparence
    image = Image.new("RGBA", (largeur, hauteur), (0, 0, 0, 0))
    # Initialise l'outil de dessin
    draw = ImageDraw.Draw(image)
    # Dessine un rectangle arrondi avec la couleur spécifiée
    draw.rounded_rectangle((0, 0, largeur, hauteur), radius=rayon, fill=couleur)
    return image

# Fonction pour évaluer une expression mathématique
def evaluer(expression):
    try:
        # Vérifie si l'expression contient une racine carrée
        if '√' in expression:
            parts = expression.split('√')
            if parts[0] == '':
                # Si l'expression commence par '√', calcule la racine carrée du nombre suivant
                result = math.sqrt(float(parts[1]))
            else:
                # Sinon, multiplie le nombre avant '√' par la racine carrée du nombre suivant
                result = float(parts[0]) * math.sqrt(float(parts[1]))
        # Vérifie si l'expression contient une exponentiation
        elif 'e^' in expression:
            parts = expression.split('e^')
            if parts[0] == '':
                # Si l'expression commence par 'e^', calcule l'exponentielle du nombre suivant
                result = math.exp(float(parts[1]))
            else:
                # Sinon, multiplie le nombre avant 'e^' par l'exponentielle du nombre suivant
                result = float(parts[0]) * math.exp(float(parts[1]))
        else:
            # Remplace les symboles par leurs équivalents Python et évalue l'expression
            result = eval(expression.replace('×', '*').replace('÷', '/').replace('−', '-').replace('^', '**').replace('x²', '**2'))
        return f"= {result}"
    except Exception as e:
        # En cas d'erreur, retourne "Erreur"
        return "Erreur"

# Fonction pour afficher la calculatrice avec tkinter
def afficher_calculatrice():
    root = tk.Tk()  # Crée une nouvelle fenêtre
    root.title("Calculatrice")  # Définit le titre de la fenêtre
    root.configure(bg='#8E7ECE')  # Définit la couleur de fond de la fenêtre

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    main_width = 1000  # Largeur de la fenêtre principale
    main_height = 700  # Hauteur de la fenêtre principale
    main_radius = 15  # Rayon des coins arrondis de la fenêtre principale
    main_color = "#8E7ECE"  # Couleur de fond de la fenêtre principale

    # Calcule la position pour centrer la fenêtre sur l'écran
    x = (screen_width - main_width) // 2
    y = (screen_height - main_height) // 2

    # Définit la taille et la position de la fenêtre
    root.geometry(f"{main_width}x{main_height}+{x}+{y}")

    # Crée une image de fond arrondie pour la fenêtre principale
    main_image = creer_rectangle_arrondi(main_width, main_height, main_radius, main_color)
    main_tk_image = ImageTk.PhotoImage(main_image)

    # Crée un label pour afficher l'image de fond
    main_label = tk.Label(root, image=main_tk_image, bg='#8E7ECE')
    main_label.image = main_tk_image  # Garde une référence de l'image
    main_label.pack(padx=20, pady=20)

    calc_width = 800  # Largeur de la calculatrice
    calc_height = 600  # Hauteur de la calculatrice
    calc_radius = 15  # Rayon des coins arrondis de la calculatrice
    calc_color = "#2D2A37"  # Couleur de fond de la calculatrice

    # Crée une image de fond arrondie pour la calculatrice
    calc_image = creer_rectangle_arrondi(calc_width, calc_height, calc_radius, calc_color)
    calc_tk_image = ImageTk.PhotoImage(calc_image)

    # Crée un label pour afficher l'image de fond de la calculatrice
    calc_label = tk.Label(main_label, image=calc_tk_image, bg='#8E7ECE')
    calc_label.image = calc_tk_image  # Garde une référence de l'image
    calc_label.place(relx=0.5, rely=0.5, anchor="center", width=calc_width, height=calc_height)

    # Crée l'interface de la calculatrice
    creer_interface_calculatrice(calc_label)

    root.mainloop()  # Démarre la boucle principale de l'application

# Fonction pour créer l'interface de la calculatrice
def creer_interface_calculatrice(parent):
    # Définition des boutons de la calculatrice
    boutons = [
        ['x^y', '(', ')', 'DEL'],
        ['e^', 'x²', '√', '÷'],
        ['7', '8', '9', '×'],
        ['4', '5', '6', '−'],
        ['1', '2', '3', '+'],
        ['.', '0', '⌫', '=' ]
    ]

    # Crée un champ d'affichage pour la calculatrice
    affichage = tk.Entry(parent, font=("Arial", 24), bg="#2D2A37", fg="white", justify="right", bd=0)
    affichage.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    parent.affichage = affichage  # Associe le champ d'affichage au parent

    # Crée les boutons de la calculatrice
    for i, row in enumerate(boutons):
        for j, button in enumerate(row):
            # Crée un bouton avec le texte spécifié et les propriétés de style
            btn = tk.Button(parent, text=button, font=("Arial", 18), bg="#3B3A4F" if button.isdigit() else "#5E5A8B", fg="white", bd=0, relief="flat")
            btn.grid(row=i+1, column=j, padx=10, pady=10, sticky="nsew")
            # Associe la fonction de clic au bouton
            btn.config(command=lambda b=button: clic_bouton(parent, b))

    # Configure les poids des lignes et colonnes pour le redimensionnement
    for i in range(len(boutons)):
        parent.rowconfigure(i+1, weight=1)
    for j in range(4):
        parent.columnconfigure(j, weight=1)

# Fonction appelée lors du clic sur un bouton
def clic_bouton(parent, button):
    affichage = parent.affichage  # Récupère le champ d'affichage
    texte_actuel = affichage.get()  # Récupère le texte actuel du champ d'affichage

    if texte_actuel == "Erreur" and button.isdigit():
        affichage.delete(0, tk.END)  # Efface le texte actuel si c'est "Erreur" et que le bouton est un chiffre
        texte_actuel = ""

    if button == '⌫':
        affichage.delete(len(texte_actuel) - 1, tk.END)  # Supprime le dernier caractère
    elif button == 'DEL':
        affichage.delete(0, tk.END)  # Supprime tout le texte
    elif button == '=':
        result = evaluer(texte_actuel)  # Évalue l'expression
        affichage.delete(0, tk.END)  # Efface le texte actuel
        affichage.insert(tk.END, result)  # Affiche le résultat
    elif button == 'x^y':
        affichage.insert(tk.END, '^')  # Insère '^' pour la puissance
    elif button == 'e^':
        affichage.insert(tk.END, 'e^')  # Insère 'e^' pour l'exponentielle
    elif button == '√':
        affichage.insert(tk.END, '√')  # Insère '√' pour la racine carrée
    elif button == 'x²':
        affichage.insert(tk.END, 'x²')  # Insère 'x²' pour le carré
    else:
        affichage.insert(tk.END, button)  # Insère le texte du bouton

# Lancement de l'application
afficher_calculatrice()
