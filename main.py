""" Main du programme Jeu Quorridor - Phase 1
Écrit par Maxime Carpentier 111 095 058
Le 11 novembre 2019
Ce programme communique avec un serveur pour jouer
au jeu Quorridor, et affiche le résultat à l'écran
"""


import argparse # Pour les lignes de commande
import api # On récupère le fichier api


def analyser_commande():
    """ Fonction pour analyser la ligne de commande
    Ne prend pas d'argument d'entrée et retourne les options
    de la ligne de commande.
    """
    # On crée l'analyseur de ligne de commande, avec un titre
    parser = argparse.ArgumentParser(description="Jeu Quoridor - phase 1")
    # Premier argument qui servira à afficher une liste
    parser.add_argument(
        '-l', '--lister',
        dest="lister", action="store_true",
        help="Lister les identifiants de vos 20 dernières parties."
    )
    # On crée une argument aui nous servira à récupérer l'idul
    parser.add_argument(
        'idul',
        type=str, help='IDUL du joueur.'
    )

    return parser.parse_args() # On retourne les arguments

def afficher_damier_ascii(dicto):
    """ Fonction pour afficher le Damier
    Elle prend en argument un dictionnaire avec l'état de la partie
    Elle retourne une chaine de caractère représentant le damier.
    """
    # On commence la chaine sous forme de liste avec la première ligne
    chaine = 3*[' '] + 35*['-'] + [' \n']
    # On remplis toutes les lignes du milieu
    for i in range(9, 0, -1): # On compte à l'envers pour placer bien les (y)
        chaine += str(i) + ' | ' + 8*'.   ' + '. |'
        if i != 1:
            chaine += '\n  |' + 34 * ' ' + ' |\n'
    # On met la ligne de la limite du damier
    chaine += '\n--|' + 35*'-' + '\n  | '
    # On met la ligne avec les nombres horizontaux (x)
    for i in range(1, 10):
        chaine += str(i) + '   '

    # On lit la liste des murs horizontaux
    for dicto["murs"]["horizontaux"] in dicto["murs"]["horizontaux"]:
        # Il y a 6 caractères pour les murs horizontaux donc on les place
        for i in range(7):
            chaine[42+ (19 - dicto["murs"]["horizontaux"][1]*2)*40 +
                   4*(dicto["murs"]["horizontaux"][0]-1)+i] = '-'

    # On lit la liste des murs verticaux
    for dicto["murs"]["verticaux"] in dicto["murs"]["verticaux"]:
        # Il y a 3 caractères pour les murs verticaux donc on les place
        for j in range(3):
            chaine[35 + (16 - dicto["murs"]["verticaux"][1]*2 + j)*40 +
                   4*(dicto["murs"]["verticaux"][0]-1)+i] = '|'

    # On lit et on place le joueur 1
    chaine[37 + (16 - dicto["joueurs"][0]["pos"][1]*2+2)*40 +
           4*(dicto["joueurs"][0]["pos"][0]-1)+6] = '1'

    # On lit et on place le joueur 2
    chaine[37 + (16 - dicto["joueurs"][1]["pos"][1]*2+2)*40 +
           4*(dicto["joueurs"][1]["pos"][0]-1)+6] = '2'

    # On retourne la chaine de caractère en ajoutant la légende et en faisant
    # un join() sur la liste. On sépare en trois fois pour ne pas
    # dépasser la colonne 80
    legende = 'Légende: 1=' + str(dicto["joueurs"][0]["nom"])
    legende = legende + ', 2=' + str(dicto["joueurs"][1]["nom"])
    return  legende +'\n' + ''.join(chaine)


ARGS = analyser_commande() # Analyse la liste de commande

if ARGS.lister: # Si l'option -l est entrée on affiche la liste
    print(api.lister_parties(ARGS.idul)) # des parties pour l'idul actuel


DEBUT = api.débuter_partie(ARGS.idul) # On commence la partie
DIC = DEBUT[1]
# On enregistre le premier état dans un dictionnaire pour plus tard
LISTE = [] # On crée une liste vide

a = 1
while a == 1: # Pour faire une boucle infinie, jusqu'à un gagnant ou erreur

    # Dans la suite on va lire la liste des états et remettre notre valeur dans
    # dico comme ça si un joueur prend le même idul que celui de notre partie
    # on pourra tout de même continuer notre partie sans problème
    LISTE = api.lister_parties(ARGS.idul)
    # Liste prend la valeur de tous les états de cette idul
    for LISTE in LISTE: # On lit la liste
        if LISTE["id"] == DEBUT[0]: # Si on a le bon id de partie
            DIC = LISTE["état"] # La variable dico prend la valeur du bon état

    print(afficher_damier_ascii(DIC)) # On affiche le damier actuel

    # On va récupérer le coup de l'utilisateur
    TYPE_COUP = input("Entrez votre coup, (D, MH ou MV) : ") # Type de coup
    x = input("Entrez votre valeur x : ") # Pos x
    y = input("Entrez votre valeur y : ") # pos y

    DIC = api.jouer_coup(DEBUT[0], TYPE_COUP, (x, y)) # Pour jouer notre coup
