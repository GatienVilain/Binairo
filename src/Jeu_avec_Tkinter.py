#-----------------------------------------------------------------------
# Titre : Jeu du binairo ou Takuzu
# Description : Takuzu ou Binairo est un jeu de réflexion consistant à remplir
#               une grille avec les chiffres 0 et 1 par déduction logique.
#
# Auteus : Pierre Giraud, Nawress Laabidi, Gatien Vilain
#
# Date de création : 20 mai 2020
#-----------------------------------------------------------------------

#-------------------- Bibliothèques ------------------------------------
from tkinter import *
from os import path,listdir

#---------------- Programmes extérieurs --------------------------------
from Binairo_sans_Tkinter import liste_egal_liste_solution,generer_solution,generer_grille_exercice,nombre_de_case_à_retirer,verification_complet,verification_3_a_la_ligne,verification_ligne_identique,verification_ligne_trop_0_ou_1,inversion_ligne_colonne
from Affichage_regle_du_jeu import regle_du_jeu

#---------------------- Fonctions --------------------------------------

# Fonction d'affichage de la grille de jeu
def afficher_grille(grille):
    police=int(250/len(grille))         #calcule la police optimale d'affichage de la grille
    global global_frame,frames,boutons
    for widget in global_frame.winfo_children():
        widget.destroy()
    frames,boutons=[],[]
    for ligne in range(len(grille)):
        for valeur in range(len(grille)):
            globals()["frame_" + str(ligne) + str(valeur)]=Frame(global_frame,bg='#41B77F',bd=1,relief=SUNKEN,highlightbackground="#41B77F", highlightcolor="#41B77F", highlightthickness=4)
            frames.append(globals()["frame_" + str(ligne) + str(valeur)])

            globals()["button_" + str(ligne) + str(valeur)]=Button(frames[ligne*len(grille)+valeur],text=grille[ligne][valeur],font=("Arial",police),bg='#41B77F',fg='white',width=2,height=1)
            boutons.append(globals()["button_" + str(ligne) + str(valeur)])
            if grille_depart[ligne][valeur]!=' ':
                boutons[ligne*len(grille)+valeur].config(fg=('black'))

            boutons[ligne*len(grille)+valeur].config(command= lambda x=boutons[ligne*len(grille)+valeur]: changer_valeur(x))

            frames[ligne*len(grille)+valeur].grid(row=ligne,column=valeur,sticky=W)
            frames[ligne*len(grille)+valeur].columnconfigure(0,weight=4)
            frames[ligne*len(grille)+valeur].rowconfigure(0,weight=4)

            boutons[(ligne)*len(grille)+valeur].grid(row=0,column=0)
    global_frame.pack(expand = YES)
    # ---------------------
    # Création d'un bouton réinitialiser
    btn_reinitialiser = Button(global_frame, text = 'Réinitialiser', font = ('Helvetica', 12), bg ='blue', fg = 'white', overrelief = SUNKEN, command= lambda : reinitialisation())
    btn_reinitialiser.grid(row = len(grille)+1, column = 0, columnspan = (len(grille))//2, sticky = W, pady = 10)
    # Création d'un bouton de vérification
    btn_verification = Button(global_frame, text = ' Vérifier ', font = ('Helvetica', 12), bg ='blue', fg = 'white', overrelief = SUNKEN, command= lambda : verification_tkinter())
    btn_verification.grid(row = len(grille)+1, column = len(grille)//2, columnspan = (len(grille))//2, sticky = E, pady = 10)
    # ------------------------

# Fonction qui change les valeurs quand on clique dessus
def changer_valeur(bouton):
    global grille_depart,grille,decalage,verification
    if verification:
        verification_tkinter()
    else:
        numero=""
        for i in range(14,str(bouton).index(".",14)):
            numero+=str(bouton)[i]
        if numero=="":
            numero=1
        numero=int(numero)-decalage-1
        ligne=int((numero/len(grille)))
        colonne=numero-ligne*len(grille)
        if grille_depart[ligne][colonne]!=' ':
            erreur=Toplevel()
            erreur.resizable(width=False,height=False)
            erreur.title("erreur du choix de la case")
            erreur_label=Label(erreur,text=" La case choisie était présente au départ, elle est donc juste ! \n Veuillez choisir une autre case").pack()
            erreur.after(5000,lambda : erreur.destroy())
        elif grille[ligne][colonne]==0:       #change un 0 en 1
            grille[ligne][colonne]=1
            bouton.config(text=1)
        elif grille[ligne][colonne]==1:     #change un 1 en "blanc"
            grille[ligne][colonne]=' '
            bouton.config(text='')
        elif grille[ligne][colonne]==' ':    #change un "blanc" en 0
            grille[ligne][colonne]=0
            bouton.config(text='0')

#------------- Fonctions gérant la demande d'une nouvelle partie --------------------

def nouveau_jeu():
    global grille,grille_depart,solution,decalage,game_window
    taille_difficulte = demander_taille_difficulte()
    solution = generer_solution(taille_difficulte[0]) # génère une liste solution
    decalage+=len(grille)**2
    grille = liste_egal_liste_solution(solution) # copie la liste solution dans la liste de jeu sans que les 2 soient liés
    grille = generer_grille_exercice(taille_difficulte[0], grille, nombre_de_case_à_retirer(taille_difficulte[0], taille_difficulte[1])) #crée la grille de jeu
    grille_depart=liste_egal_liste_solution(grille)
    afficher_grille(grille)

# Fonction demandant de rentrer la taille du plateau
def demander_taille_difficulte():
    global reponse,taille,difficulte,attente
    reponse=0
    taille_difficulte_window=Toplevel()
    taille_difficulte_window.title("Choix de la difficulté")
    taille_difficulte_window.resizable(width=False,height=False)
    question = Label(taille_difficulte_window,text="Entrez la taille du plateau : \n Veuillez entrer un nombre entier pair non nul (maximum 14)!")
    entree = Entry(taille_difficulte_window)
    validation = Button(taille_difficulte_window,text="Valider",command = lambda : valide_taille_difficulte(entree,question,taille_difficulte_window))
    question.pack()
    entree.pack()
    validation.pack()
    attente=IntVar()
    validation.wait_variable(attente)
    return(taille,difficulte)

# Fonction demandant de rentrer et la difficulté de la partie
def valide_taille_difficulte(entree,question,taille_difficulte_window):
    global reponse,taille,difficulte,attente
    if entree.get().isdigit()==False:
        entree.delete(0,END)
    elif reponse==0 and int(entree.get())%2==0 and int(entree.get())!=0 and int(entree.get())<16:
        reponse+=1
        question.config(text="Quel degré de difficulté choisissez vous ? \n 1 = facile \t 2 = moyen \t 3 = difficile")
        taille=int(entree.get())
        entree.delete(0,END)
    elif reponse==1 and int(entree.get()) in [1,2,3]:
        difficulte=int(entree.get())
        taille_difficulte_window.destroy()
        attente.set(1)
    else:
        entree.delete(0,END)

#------------------------------------------------------------------------------------------
#--------------------- Fonctions de sauvegarde et de chargement de partie -----------------

# Fonction de sauvegarde de la partie
def save(entree,grille,grille_depart,solution,sauvegarder):
    chemin="./src/saves/{}".format(entree.get())
    if path.isfile(chemin):
        sauvegarde_existe=Toplevel()
        oui_non=IntVar()
        sauvegarde_existe.resizable(width=False,height=False)
        sauvegarde_existe.title("{} existe déjà".format(entree.get()))
        existe=Label(sauvegarde_existe,text="Ce nom est déjà utilisé pour une autre sauvegarde \n Voulez vous écraser cette sauvegarde ?").grid(row=0,column=0,columnspan=2)
        oui=Button(sauvegarde_existe,text="OUI",command = lambda : oui_non.set(1))
        oui.grid(row=1,column=0)
        non=Button(sauvegarde_existe,text="NON",command = lambda : oui_non.set(0))
        non.grid(row=1,column=1)
        oui.wait_variable(oui_non)
        if oui_non.get()==1:
            file=open(chemin,"w+")
            file.write(save_state(grille,grille_depart,solution))
            file.close()
            sauvegarde_existe.destroy()
            sauvegarder.destroy()
        else:
            sauvegarde_existe.destroy()
            sauvegarder.destroy()
            save_name()
    else:
            file=open(chemin,"w+")
            file.write(save_state(grille,grille_depart,solution))
            file.close()
            sauvegarder.destroy()

def save_state(grille,grille_depart,solution):
    grille_save,grille_depart_save,solution_save="","",""
    for ligne in range(len(grille)):
        for valeur in range(len(grille)):
            grille_save+=str(grille[ligne][valeur])
            grille_depart_save+=str(grille_depart[ligne][valeur])
            solution_save+=str(solution[ligne][valeur])
    return grille_save+"\n"+grille_depart_save+"\n"+solution_save

def save_name():
    global grille,grille_depart,solution
    sauvegarder = Toplevel()
    sauvegarder.title("Sauvegarder")
    sauvegarder.resizable(width=False,height=False)
    if grille == []:
        no_grille = Label(sauvegarder,text="Il n\'y a pas de grille à sauvegarder !").pack()
        sauvegarder.after(5000,lambda : sauvegarder.destroy())
    else:
        question = Label(sauvegarder,text="Comment voulez nommer votre sauvegarde ? \n Caractères non autorisés : / \ : * ? \" ").pack()
        entree = Entry(sauvegarder)
        entree.pack()
        validation = Button(sauvegarder,text="Valider",command = lambda : save(entree,grille,grille_depart,solution,sauvegarder)).pack()

# Fonction de chargement de la partie
def load():
    saves=[name for name in listdir("./src/saves") if path.isfile("./src/saves/{}".format(name))]
    load_window=Toplevel()
    load_window.title("charger une partie")
    load_window.resizable(width=False,height=False)
    if saves==[]:
        no_saves=Label(load_window,text="Aucune partie n'a été sauvegardée").pack()
        load_window.after(5000,lambda : load_window.destroy())
    else:
        save_choice=Label(load_window,text="Veuillez choisir la sauvegarde que vous voulez chager").grid(row=0,column=0)
        numero_save=0
        for name in saves:
            numero_save+=1
            Button(load_window,text=name,command = lambda x=name: load_save(x,load_window)).grid(row=numero_save,column=0)

def load_save(name,load_window):
    save=open("./src/saves/{}".format(name),'r')
    donnees=save.readlines()
    save.close()
    global grille,grille_depart,solution,decalage
    grilles=[[],[],[]]
    for ligne in range(int(len(donnees[0])**(1/2))):
        grilles[0].append([])
        grilles[1].append([])
        grilles[2].append([])
        for valeur in range(int(len(donnees[0])**(1/2))):
            for liste in range(3):
                if donnees[liste][valeur+int(ligne*(len(donnees[0])**(1/2)))] in ["0","1"]:
                    grilles[liste][ligne].append(int(donnees[liste][valeur+int(ligne*(len(donnees[0])**(1/2)))]))
                elif donnees[liste][valeur+int(ligne*(len(donnees[0])**(1/2)))]==" ":
                    grilles[liste][ligne].append(" ")
                else:
                    sauvegarde_corrompue=Toplevel()
                    sauvegarde_corrompue.title("sauvegarde corrompue")
                    sauvegarde_corrompue.resizable(width=False,height=False)
                    corruption=Label(sauvegarde_corrompue,text="La sauvegarde est corrompue !").pack()
                    sauvegarde_corrompue.after(5000, lambda : [sauvegarde_corrompue.destroy(),load_window.destroy()])
                    return
    decalage+=len(grille)**2
    grille,grille_depart,solution=grilles[0],grilles[1],grilles[2]
    afficher_grille(grille)
    load_window.destroy()

#--------------------------------------------------------------------------------

# Fonction de reinitialisation de la grille
def reinitialisation():
    global grille,grille_depart,decalage
    if grille==[]:                            #Vérifie qu'une partie est en cours
        no_grille_window=Toplevel()
        no_grille_window.title("Pas de partie en cours")
        no_grille_window.resizable(width=False,height=False)
        no_grille_label=Label(no_grille_window,text="Il n\'y a pas de grille à réinitialiser !").pack()
        no_grille_window.after(5000, lambda : no_grille_window.destroy())
    else:
        decalage+=len(grille)**2
        grille=liste_egal_liste_solution(grille_depart)
        afficher_grille(grille)

#--------------------------------------------------------------------------------

# Fonction de vérification de la grille

def verification_tkinter():
    global decalage,verification,grille,solution
    if grille==[]:                            #Vérifie qu'une partie est en cours
        no_grille_window=Toplevel()
        no_grille_window.title("Pas de partie en cours")
        no_grille_window.resizable(width=False,height=False)
        no_grille_label=Label(no_grille_window,text="Il n\'y a pas de grille à vérfier !").pack()
        no_grille_window.after(5000, lambda : no_grille_window.destroy())

    elif grille==solution:               #Vérifie si la grille est égale à la solution
        Victoire_window=Toplevel()              #Auquel cas, le joueur a gagné
        Victoire_window.title("Pas de partie en cours")
        Victoire_window.resizable(width=False,height=False)
        Victoire_label=Label(Victoire_window,text="Bien joué, vous avez gagné !").pack()
        Victoire_window.after(5000, lambda : Victoire_window.destroy())

    elif verification_complet(grille):       #vérifie si le joueur a bien rempli entièrement la grille
        grille_incomplete=Toplevel()
        grille_incomplete.title("Pas de partie en cours")
        grille_incomplete.resizable(width=False,height=False)
        grille_incomplete_label=Label(grille_incomplete,text="La grille n'est pas remplie ! \n Veuillez remplir la grille avant de vérifier vos réponses.").pack()
        grille_incomplete.after(5000, lambda : grille_incomplete.destroy())


    else:
        liste_erreur=['ligne']
        reponse = [verification_3_a_la_ligne(grille,liste_erreur), verification_ligne_identique(grille,liste_erreur), verification_ligne_trop_0_ou_1(grille,liste_erreur)]
        grille=inversion_ligne_colonne(grille,liste_erreur)
        reponse.extend([verification_3_a_la_ligne(grille,liste_erreur), verification_ligne_identique(grille,liste_erreur), verification_ligne_trop_0_ou_1(grille,liste_erreur)])
        grille=inversion_ligne_colonne(grille,liste_erreur)
        if reponse == [True, True, True, True, True, True]:      #vérifie si le joueur a gagné en trouvant une autre solution que celle proposée dans la grille solution
            Victoire_window=Toplevel()
            Victoire_window.title("Pas de partie en cours")
            Victoire_window.resizable(width=False,height=False)
            Victoire_label=Label(Victoire_window,text="Bien joué, vous avez gagné !").pack()
            Victoire_window.after(5000, lambda : Victoire_window.destroy())

        else:                                       #affiche les erreurs du joueurs
            verification=True
            erreur_window=Toplevel()
            erreur_window.title("Affichage des erreurs")
            erreur_window.resizable(width=False,height=False)
            erreur_notice=Label(erreur_window,text="En rouge s\'affiche les chiffres identiques côte à côte en nombre supérieur à 2. \n En bleu s\'affiche les lignes ou les colonnes qui sont identiques. \n En jaune sont encadrés les cases des lignes ou des colonnes qui possèdent trop de 1 ou trop de 0. \n \n Appuyez sur fermer pour revenir au jeu.").pack()
            global global_frame,boutons,frames

            for erreur in range(1,liste_erreur.index("colonne")):
                if liste_erreur[erreur][0] == "3 à la suite":
                    for case in [liste_erreur[erreur][3],liste_erreur[erreur][4],liste_erreur[erreur][5]]:
                        boutons[liste_erreur[erreur][2]*len(grille)+case].config(fg='red')

                if liste_erreur[erreur][0] == "identique":
                    for case in range(len(grille)):
                        boutons[liste_erreur[erreur][1]*len(grille)+case].config(bg='blue')
                        boutons[liste_erreur[erreur][2]*len(grille)+case].config(bg='blue')

                if liste_erreur[erreur][0] == "trop de":
                    for case in range(len(grille)):
                        frames[liste_erreur[erreur][2]*len(grille)+case].config(highlightbackground="yellow", highlightcolor="yellow", highlightthickness=4)

            for erreur in range(liste_erreur.index("colonne"), len(liste_erreur)):
                if liste_erreur[erreur][0] == "3 à la suite":
                    for ligne in [liste_erreur[erreur][3],liste_erreur[erreur][4],liste_erreur[erreur][5]]:
                        boutons[ligne*len(grille)+liste_erreur[erreur][2]].config(fg='red')

                if liste_erreur[erreur][0] == "identique":
                    for ligne in range(len(grille)):
                        boutons[ligne*len(grille)+liste_erreur[erreur][1]].config(bg='blue')
                        boutons[ligne*len(grille)+liste_erreur[erreur][2]].config(bg='blue')

                if liste_erreur[erreur][0] == "trop de":
                    for ligne in range(len(grille)):
                        frames[ligne*len(grille)+liste_erreur[erreur][2]].config(highlightbackground="yellow", highlightcolor="yellow", highlightthickness=4)

            fermer_erreur=Button(erreur_window, text='Fermer',command= lambda : [afficher_grille(grille), erreur_window.destroy(),verification_statut()]).pack()

def verification_statut():
    global verification,decalage
    verification=False
    decalage+=len(grille)**2


#----------------------- Setup de la fenêtre ------------------------------------
game_window=Tk()
game_window.title("BINAIRO")
game_window.geometry("800x1000")
game_window.minsize(700,900)
game_window.iconphoto(True, PhotoImage(file='./src/images/icon.png'))
game_window.config(background='#41B77F')
global_frame=Frame(game_window,bg='#41B77F',bd=3)
grille,solution,decalage,verification=[],None,0,False


# ------------------------ Setup des menus ---------------------------------------
menu=Menu(game_window)

menu_fichier=Menu(menu,tearoff=0)
menu_fichier.add_command(label='sauvegarder',command = lambda : save_name())
menu_fichier.add_command(label='charger',command = lambda : load())
menu.add_cascade(label='fichier',menu=menu_fichier)

menu_jeu=Menu(menu,tearoff=0)
menu_jeu.add_command(label='règles du jeu',command = lambda : regle_du_jeu())
menu_jeu.add_command(label='nouveau jeu',command= lambda : nouveau_jeu())
menu_jeu.add_command(label='vérification de la grille',command= lambda : verification_tkinter())
menu_jeu.add_command(label='Réinitialiser la grille',command= lambda : reinitialisation())
menu.add_cascade(label='jeu',menu=menu_jeu)

menu_quitter=Menu(menu,tearoff=0)
menu_quitter.add_command(label='quitter le jeu',command= lambda : game_window.destroy())
menu.add_cascade(label='quitter',menu=menu_quitter)

game_window.config(menu=menu)

#-----------------------------------------------------------------------
#--------------------------Exécution du jeu-----------------------------
game_window.mainloop()