#-----------------------------------------------------------------------
# Titre : Jeu du binairo ou Takuzu -- version sans Tkinter
# Description : Takuzu ou Binairo est un jeu de réflexion consistant à remplir
#               une grille avec les chiffres 0 et 1 par déduction logique.
#
# Auteurs : Pierre Giraud, Nawress Laabidi, Gatien Vilain
#
# Date de création : 16 avril 2020
#-----------------------------------------------------------------------


#---------------- Bibliothèques ----------------------------------------
from numpy import random


#------------------ Fonctions ------------------------------------------

#-------- Fonctions initialisation du jeu -------------------------------
def main() :
  menu()
  choix = int(input('Quel choix désirez vous ? '))
  choix_pris(choix)


def menu() :
    print('\n \t \t BINAIRO - TAKUZU')
    print('\nTable de choix : ')
    print('1: Règle du jeu ')
    print('2: Jouer ')
    print('3: Quitter ')
    print('')


def choix_pris(choix) :
  if choix == 1 :
    regle_du_jeu()

  elif choix == 2 :
    initialisation()

  elif choix == 3 :
    print('À plus tard')
    exit()


def regle_du_jeu() :
  print('\n\t Les règles  : ')
  print('1 - On ne peut compléter les cases qu\'avec des 0 ou des 1')
  print('2 - Autant de 1 et de 0 sur chaque ligne et sur chaque colonne')
  print('3 - Pas plus de 2 chiffres identiques côte à côte')
  print("4 - 2 lignes ou 2 colonnes ne peuvent être identiques")
  input('\n Appuyez sur entrer pour revenir au menu.\n')
  main()


def taille_plateau () :
  taille = 1
  while (taille%2) == 1 :
     taille = int(input("Entrer la taille du plateau : "))

  return taille


def difficulte_jeu () :
  difficulte = 0

  while difficulte not in [1,2,3]:
    print("Quel degré de difficulté choisissez vous ? \n 1 = facile \t 2 = moyen \t 3 = difficile")
    difficulte = int(input("degré de difficulté : "))

  return difficulte


def initialisation () :
  taille = taille_plateau()
  difficulte = difficulte_jeu()
  liste_jeu_debut = generer_grille_exercice(taille, generer_solution(taille), nombre_de_case_à_retirer(taille, difficulte))
  liste_jeu = liste_egal_liste_solution(liste_jeu_debut) # copie liste_jeu_debut dans liste_jeu sans les lier pour que liste_jeu soit modifiable mais pas liste_jeu_debut
  print('\n \t A vous de jouer \'_\'')
  jeu (taille, difficulte, liste_jeu_debut, liste_jeu)


def jeu (taille_plateau, difficulte, liste_jeu_debut, liste_jeu) :
  while True :
    print('\n')
    check = None
    affichage(taille_plateau, liste_jeu)

    while check not in [0, 1]:
      check = int(input("Voulez-vous faire une verification de la grille ? \t 0 = non \t 1 = oui "))
    if check == 1:
        verification(liste_jeu)
        affichage(taille_plateau, liste_jeu)

    liste_jeu = reponse(taille_plateau, liste_jeu_debut, liste_jeu)


#----------------------------------------------------------------------
#--------- Fonctions générant la grille solution ----------------------

def generer_base(taille): #génère une liste de "taille" listes de "taille" entiers 0 ou 1
    base=[]
    for ligne in range(taille):
        ligne_base = []
        for colonne2 in range(taille):
            ligne_base.append(random.randint(0,2))
        base.append(ligne_base)
    return base


def changement_3_a_la_ligne(base): #si 3 fois la même valeur à la suite dans une ligne, change une de ces 3 valeurs au hasard et prévient que l'on a eu au mons un changement (reponse=False)
    reponse=True
    for ligne in range(len(base)):
        ligne_reponse=False
        while ligne_reponse==False:     #Tant que l'on a eu besoin de changer une valeur dans la ligne, on continue
            ligne_reponse=True
            for valeur in range(len(base)-2):
                if base[ligne][valeur]==base[ligne][valeur+1]==base[ligne][valeur+2]:
                    hasard=random.randint(0,3)
                    base[ligne][valeur+hasard]=(base[ligne][valeur+hasard]-1)**2
                    reponse=False
                    ligne_reponse=False
    return base,reponse


def changement_ligne_identique(base): #si une ligne A est identique à une ligne B, change une valeur au hasard dans cette ligne A  et prévient que l'on a eu au moins 1 changement (reponse=False)
    reponse=True
    for ligne_A in range(len(base)-1):
        for ligne_B in range(ligne_A+1):
            if base[ligne_A+1]==base[ligne_B]:
                hasard=random.randint(0,len(base))
                base[ligne_A+1][hasard]=(base[ligne_A+1][hasard]-1)**2
                reponse=False
    return base,reponse


def changement_ligne_trop_0_ou_1(base): #si une ligne comporte trop de 0 ou de 1, en change un au hasard et prévient que l'on a eu au moins 1 changement (reponse=False)
    reponse=True
    for ligne in range(len(base)):
        if base[ligne].count(0)<base[ligne].count(1):
            hasard=random.randint(0,int(len(base)*3/4)) #int(len(base)*3/4) correspond au rang le plus faible où peut se trouver le zero de rang le plus haut dans la ligne
            base[ligne][base[ligne].index(1,hasard)]=0
            reponse=False
        if base[ligne].count(0)>base[ligne].count(1):
            hasard=random.randint(0,int(len(base)*3/4))
            base[ligne][base[ligne].index(0,hasard)]=1
            reponse=False
    return base,reponse


# inverse les lignes et les colonnes
def inversion_ligne_colonne(liste_jeu,liste_erreur):
    base=[]
    liste_erreur.append("colonne")
    for colonne in range(len(liste_jeu)):
        nouvelle_ligne=[]
        for ligne in range(len(liste_jeu)):
            nouvelle_ligne.append(liste_jeu[ligne][colonne]) #nouvelle_ligne = ligne formée à partir de la colonne de la grille précédente
        base.append(nouvelle_ligne)
    liste_jeu=base
    return liste_jeu


# génère une grille puis effectue les fonctions précédentes jusqu'à ce qu'elle respecte les règles
def generer_solution(taille):
    base=generer_base(taille)
    reponse=False
    if taille==2:
        while reponse!=[True,True,True,True]:
            base,reponse_identique=changement_ligne_identique(base)
            base,reponse_trop=changement_ligne_trop_0_ou_1(base)
            reponse=[reponse_identique,reponse_trop] #previent si l'on a eu au moins un changement dans chacune des fonctions dans les lignes
            base=inversion_ligne_colonne(base,[])
            base,reponse_identique=changement_ligne_identique(base)
            base,reponse_trop=changement_ligne_trop_0_ou_1(base)
            reponse.extend([reponse_identique,reponse_trop]) #à la reponse précédente s'ajoute si l'on a eu au moins un changement dans chacune des fonctions dans les colonnes
            base=inversion_ligne_colonne(base,[])
    else:
        while reponse!=[True,True,True,True,True,True]:
            base,reponse_3=changement_3_a_la_ligne(base)    #vérification des lignes
            base,reponse_identique=changement_ligne_identique(base)
            base,reponse_trop=changement_ligne_trop_0_ou_1(base)
            reponse=[reponse_3,reponse_identique,reponse_trop] #previent si l'on a eu au moins un changement dans chacune des fonctions dans les lignes
            base=inversion_ligne_colonne(base,[])
            base,reponse_3=changement_3_a_la_ligne(base)    #vérification des colonnes
            base,reponse_identique=changement_ligne_identique(base)
            base,reponse_trop=changement_ligne_trop_0_ou_1(base)
            reponse.extend([reponse_3,reponse_identique,reponse_trop]) #à la reponse précédente s'ajoute si l'on a eu au moins un changement dans chacune des fonctions dans les colonnes
            base=inversion_ligne_colonne(base,[])
    return base

#-------------------------------------------------------------------------

# Fonction déterminant le nombre de case à retirer selon la difficulté
def nombre_de_case_à_retirer(taille, difficulte):
    if taille<=10:
        if difficulte==1:
            nombre=int(67/100*taille**2)

        elif difficulte==2:
            nombre=int((75/100)*taille**2)

        elif difficulte==3:
            nombre=int((80/100)*taille**2)-1
    else:
        if difficulte==1:
            nombre=int(75/100*taille**2)

        elif difficulte==2:
            nombre=int((78/100)*taille**2)

        elif difficulte==3:
            nombre=int((83/100)*taille**2)-1
    return nombre


# Fonction permettant de copier une liste avec des liste à l'interieurs sans les liés
def liste_egal_liste_solution(liste_solution):
    liste=[]
    for valeur in range(len(liste_solution)):
        ligne_liste=[]
        for valeur_2 in range(len(liste_solution)):
            ligne_liste.append(liste_solution[valeur][valeur_2])
        liste.append(ligne_liste)
    return liste


# Fonction générant la grille de jeu (grille solution avec élément manquant)
def generer_grille_exercice(taille, liste, nombre) :
  numeros_retires = []
  while len(numeros_retires) < nombre:
      numero_a_retirer = random.randint(0,taille**2)
      if numero_a_retirer not in numeros_retires:
          numeros_retires.append(numero_a_retirer)
          liste[numero_a_retirer // taille][numero_a_retirer % taille] = ' '
  return liste


# Fonction gérant l'affichage de la grille
def affichage(taille_plateau, liste_jeu):
    for i in range (int(taille_plateau)) :
        print('\t ', end = '')
        print('----'*taille_plateau)
        print('\t', end = ' | ')
        for j in range (int(taille_plateau)) :
            print(liste_jeu[i][j], end = ' | ')

        print('\n')

    print('\t ', end = '')
    print('----'*taille_plateau)


# Fonction d'interaction avec l'utilisateur lors du jeu
# Il modifie les valeur de la grille au fur et à mesure du jeu
def reponse(taille_plateau, liste_jeu_début, liste_jeu):
  ligne = int(taille_plateau + 1)
  colonne = int(taille_plateau + 1)
  valeur = None
  while valeur == None :
    # Récupére les choix de l'utilisateur
    while (0 > ligne or ligne > taille_plateau) :
        ligne = int(input('Entrer le numéro de la ligne que vous voulez modifier : '))

    while (0 > colonne or colonne > taille_plateau) :
        colonne = int(input('Entrer le numéro de la colonne que vous voulez modifier : '))

    while valeur not in [0,1,''] :
        valeur = input('Quel valeur souhaiter vous entrer dans la case ? (appuyez directemet sur entrée pour remettre la case à vide) ')
        if valeur in ['0','1']:
            valeur=int(valeur)

    # Modifie la valeur de la liste si celle-ci n'ait pas une valeur non modifiable
    if liste_jeu_début[ligne-1][colonne-1] == ' ' :
        liste_jeu[ligne-1][colonne-1] = valeur
    else :
        affichage(taille_plateau, liste_jeu)
        print(' La case sélectionnée était présente dans la \n grille au départ et de ce fait, elle est juste. \n Veuillez modifier une autre case. \n')
        ligne = int(taille_plateau + 1)
        colonne = int(taille_plateau + 1)
        valeur = None
  return liste_jeu

#--------------------- Fonction de vérification------------------------

# Fonction de vérification de la grille et affichage des erreurs ou victoire
def verification(liste_jeu):
    if verification_complet(liste_jeu):
        print(" La grille n'est pas complétée. \n Veuillez compléter la grille avant de faire une vérification.")
        input("appuyez sur entrée pour continuez")
    else:
        liste_erreur = ["ligne"]
        reponse = [verification_3_a_la_ligne(liste_jeu,liste_erreur), verification_ligne_identique(liste_jeu,liste_erreur), verification_ligne_trop_0_ou_1(liste_jeu,liste_erreur)]
        liste_jeu = inversion_ligne_colonne(liste_jeu,liste_erreur)
        reponse.extend([verification_3_a_la_ligne(liste_jeu,liste_erreur), verification_ligne_identique(liste_jeu,liste_erreur), verification_ligne_trop_0_ou_1(liste_jeu,liste_erreur)])

        if reponse == [True,True,True,True,True,True]:
            print('\n Pas d\'erreur, c\'est un victoire !!!') # Affichage de la victoire si il n'y a pas d'erreur.
            input('\n Appuyez sur entrer pour revenir au menu.\n') # et retour au menu
            main()
        else:
            print("\n Grille non résolue \n")
            # Affichage des erreurs en fonction de leur categorie
            for erreur in range(1,liste_erreur.index("colonne")):
                if liste_erreur[erreur][0] == "3 à la suite":
                    print("Il y a 3 fois {} à la suite sur la ligne {} et aux colonnes {}, {}, {}.".format(liste_erreur[erreur][1], liste_erreur[erreur][2]+1, liste_erreur[erreur][3]+1, liste_erreur[erreur][4]+1, liste_erreur[erreur][5]+1))

                if liste_erreur[erreur][0] == "identique":
                    print("Les lignes {} et {} sont identiques.".format(liste_erreur[erreur][1]+1, liste_erreur[erreur][2]+1))

                if liste_erreur[erreur][0] == "trop de":
                    print("Il y a trop de {} sur la ligne {}.".format(liste_erreur[erreur][1], liste_erreur[erreur][2]))

            for erreur in range(liste_erreur.index("colonne"), len(liste_erreur)):
                if liste_erreur[erreur][0] == "3 à la suite":
                    print("Il y a 3 fois {} à la suite sur la colonne {} et aux lignes {}, {}, {}.".format(liste_erreur[erreur][1], liste_erreur[erreur][2]+1, len(liste_jeu)-liste_erreur[erreur][3]-1, len(liste_jeu)-liste_erreur[erreur][4]-1, len(liste_jeu)-liste_erreur[erreur][5]-1))

                if liste_erreur[erreur][0] == "identique":
                    print("Les colonnes {} et {} sont identiques.".format(liste_erreur[erreur][1]+1, liste_erreur[erreur][2]+1))

                if liste_erreur[erreur][0] == "trop de":
                    print("Il y a trop de {} sur la colonne {}.".format(liste_erreur[erreur][1], liste_erreur[erreur][2]+1))
            input("appuyez sur entrée pour continuez")

#vérifie si la grille est complétée entièrement
def verification_complet(liste_jeu):
    erreur=False
    for ligne in range(len(liste_jeu)):
        for valeur in range(len(liste_jeu)):
            if liste_jeu[ligne][valeur]==' ':
                erreur=True
    return erreur

# vérifie si 3 cases à la suite dans une ligne ont la même valeur
def verification_3_a_la_ligne(liste_jeu, liste_erreur):
    reponse = True
    for ligne in range(len(liste_jeu)):
        for valeur in range(len(liste_jeu) - 2):
            if liste_jeu[ligne][valeur] == liste_jeu[ligne][valeur + 1] == liste_jeu[ligne][valeur + 2]:
                reponse = False
                liste_erreur.append(["3 à la suite", liste_jeu[ligne][valeur], ligne , valeur, valeur + 1,valeur + 2])
            valeur += 1
        ligne += 1
    return reponse

# vérifie si 2 ligne sont identique
def verification_ligne_identique(liste_jeu, liste_erreur):
    reponse = True
    for ligne in range(len(liste_jeu) - 1):
        for ligne_B in range(ligne + 1,len(liste_jeu)):
            if liste_jeu[ligne] == liste_jeu[ligne_B]:
                reponse = False
                liste_erreur.append(["identique", ligne_B, ligne])
    return reponse

# vérifie si les ligne comporte le même nombre de 0 et de 1
def verification_ligne_trop_0_ou_1(liste_jeu, liste_erreur):
    reponse = True
    for ligne in range(len(liste_jeu)):
        if liste_jeu[ligne].count(0) != liste_jeu[ligne].count(1):
            reponse = False
            if liste_jeu[ligne].count(0) < liste_jeu[ligne].count(1):
                trop_de = 1

            if liste_jeu[ligne].count(0) > liste_jeu[ligne].count(1):
                trop_de = 0

            liste_erreur.append(["trop de", trop_de, ligne])
    return reponse


#-----------------------------------------------------------------------
#--------------------------Exécution du jeu-----------------------------
if __name__ == '__main__':
  main()