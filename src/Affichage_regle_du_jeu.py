#---------------------------------------------------------------------
# Fonction d'affichage des règles du Binairo - Takuzu
# Description : Petit guide des règles du jeu de Binairo avec affichage d'exemple.
#
# Auteur : Gatien Vilain
# Date de création : 12 mai 2020
#---------------------------------------------------------------------

#---------------------- Bibliothèques --------------------------------
from tkinter import *

#-------------------- Fonctions tkinter ------------------------------
#------------------ Fenêtre Règles du jeu ----------------------------
def regle_du_jeu():
    # Crée la fenêtre règles du jeu
    fenetre_regles = Toplevel()
    color = '#4065A4'
    fenetre_regles.title('Règles du Binairo')
    fenetre_regles.geometry('500x300')
    fenetre_regles.resizable(width = False, height = False)
    fenetre_regles.config(background = color)


    # Création des encadrements
    boite_principale = Frame(fenetre_regles, bg = color) # crée une boite principale contenant toutes les règles.
    boite_principale.grid(row = 1, column = 0, pady = 6, padx = 16, sticky="ew")
    boite_exemple = Frame(fenetre_regles, bg = color) # crée une boite secondaire contenant une explication imagé de la règle choisie.


    # Création d'un titre
    resume_regles = Button(
        fenetre_regles, 
        text = 'Règles du jeu',
        font = ('Helvetica', 16), 
        bg = color, 
        fg = 'red', 
        relief = FLAT,
        overrelief = SUNKEN,
        command = lambda : changement_de_page(0)) # retour au menu principale à tout moment.
    resume_regles.grid(row = 0, column = 0, pady = 7)


    # Menu principale
    btn_regle_que_0_ou_1 = Button(
        boite_principale,
        text = '1 - La grille ne doit contenir que des 0 et des 1.',
        font = ('Helvetica', 11),
        bg = color,
        fg = 'white',
        relief = FLAT,
        overrelief = SUNKEN,
        command = lambda : changement_de_page(1))
    btn_regle_que_0_ou_1.pack(fill = X, pady = 3)
    btn_regle_autant_0_et_1 = Button(
        boite_principale,
        text = '2 - Autant de 1 et de 0 sur chaque ligne et sur chaque colonne',
        font = ('Helvetica', 10),
        bg = color,
        fg = 'white',
        relief = FLAT,
        overrelief = SUNKEN,
        command = lambda : changement_de_page(2))
    btn_regle_autant_0_et_1.pack(fill = X, pady = 3)
    btn_regle_pas_plus_de_2 = Button(
        boite_principale,
        text = '3 - Pas plus de 2 chiffres identiques côte à côte',
        font = ('Helvetica', 11),
        bg = color,
        fg = 'white',
        relief = FLAT,
        overrelief = SUNKEN,
        command = lambda : changement_de_page(3))
    btn_regle_pas_plus_de_2.pack(fill = X, pady = 3)
    btn_regle_2_identiques = Button(
        boite_principale,
        text = '4 - 2 lignes ou 2 colonnes ne peuvent être identiques',
        font = ('Helvetica', 11),
        bg = color,
        fg = 'white',
        relief = FLAT,
        overrelief = SUNKEN,
        command = lambda : changement_de_page(4))
    btn_regle_2_identiques.pack(fill = X, pady = 3)
    txt_menu = Label(
        boite_principale, 
        text = 'Cliquez sur les règles pour plus d\'explications', 
        font = ("Helvetica", 10, "bold italic"), 
        bg = color, 
        fg = 'white',
        pady = 10)
    txt_menu.pack(fill = X)


    # Création de la fenêtre d'exemple
    # Création de l'image d'exemple de la règle sélectionnée
    img_exemple = PhotoImage(file = './src/images/lignes_identique.png')
    grille_exemple = Label(boite_exemple, image = img_exemple, bg = color)
    grille_exemple.image = img_exemple
    grille_exemple.grid(row = 0, column = 1, padx = 20)
    # Création d'un texte d'explication de la règle selectionnée
    txt_exemple = Label(
        boite_exemple, 
        text = '#', 
        font = ("Helvetica", 12), 
        bg = color, 
        fg = 'white',
        padx = 10)
    txt_exemple.grid(row = 0, column = 0, padx = 20)
    # Création d'un bouton retour
    btn_precedent = Button(
        boite_exemple, 
        text = 'Précédent', 
        font = ('Helvetica', 12), 
        bg ='green', 
        fg = 'white',
        overrelief = SUNKEN)
    btn_precedent.grid(row = 1, column = 0, padx = 20, pady = 10, sticky="w")
    # Création d'un bouton suivant
    btn_suivant = Button(
        boite_exemple, 
        text = ' Suivant ', 
        font = ('Helvetica', 12), 
        bg ='green', 
        fg = 'white',
        overrelief = SUNKEN)
    btn_suivant.grid(row = 1, column = 1, padx = 20, pady = 10, sticky="e")


    # Fonctions de changement de page
    def changement_de_page(page):
        if page == 0: # menu principale
            boite_principale.grid(row = 1, column = 0, pady = 6, padx = 16, sticky="ew")
            boite_exemple.grid_forget()
        else : 
            boite_principale.grid_forget()
            boite_exemple.grid(row = 1, column = 0, sticky="ew")
            # règle 1 : On ne peut compléter les cases qu'avec des 0 ou des 1.
            if page == 1: 
                img_exemple.config(file = './src/images/grille_remplie.png')
                txt_exemple.config(text = 'On ne peut compléter les  \n cases de la grille qu\'avec \n des 0 ou des 1')
                btn_precedent.config(command = lambda : changement_de_page(0))
                btn_suivant.config(command = lambda : changement_de_page(2))
            # règle 2 : Autant de 1 et de 0 sur chaque ligne et sur chaque colonne.
            elif page == 2: 
                img_exemple.config(file = './src/images/autant_éléments.png')
                txt_exemple.config(text = 'Il doit y avoir autant de 1 \n et de 0 sur chaque ligne et\n sur chaque colonne')
                btn_precedent.config(command = lambda : changement_de_page(1))
                btn_suivant.config(command = lambda : changement_de_page(3))
            # règle 3 : Pas plus de 2 chiffres identiques côte à côte.
            elif page == 3:
                img_exemple.config(file = './src/images/trop_éléments.png')
                txt_exemple.config(text = 'On ne peut pas avoir plus \n  de 2 chiffres identiques  \n côte à côte')
                btn_precedent.config(command = lambda : changement_de_page(2))
                btn_suivant.config(command = lambda : changement_de_page(4))
            # règle 4 : 2 lignes ou 2 colonnes ne peuvent être identique.
            elif page == 4:
                img_exemple.config(file = './src/images/lignes_identique.png')
                txt_exemple.config(text = '2 lignes ou 2 colonnes \n ne peuvent être identiques')
                btn_precedent.config(command = lambda : changement_de_page(3))
                btn_suivant.config(command = lambda : changement_de_page(0))
        return page


# ------------- Afficher la fenêtre principale -----------------
if __name__ == '__main__':
    app = Tk()
    buttonExample = Button(
        app,
        text = "Affichage des règles du jeu",
        command = regle_du_jeu)
    buttonExample.pack()
    app.mainloop()