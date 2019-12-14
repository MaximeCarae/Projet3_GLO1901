""" Main du programme Jeu Quorridor - Phase 1
Écrit par Maxime Carpentier 111 095 058
Le 11 novembre 2019
Ce programme communique avec un serveur pour jouer
au jeu Quorridor, et affiche le résultat à l'écran
"""


import argparse # Pour les lignes de commande
import api # On récupère le fichier api
import quoridor # On récupère la classe quoridor
import quoridorx # On récupère la classe quoridorx


def analyser_commande():
    """ Fonction pour analyser la ligne de commande
    Ne prend pas d'argument d'entrée et retourne les options
    de la ligne de commande.
    """
    # On crée l'analyseur de ligne de commande, avec un titre
    parser = argparse.ArgumentParser(description="Jeu Quoridor - phase 3")
    # Premier argument qui servira à activer le mode automatique
    parser.add_argument(
        '-a', '--automatique',
        dest="automatique", action="store_true",
        help="Activer le mode automatique."
    )
    # Second argument pour le mode graphique
    parser.add_argument(
        '-x', '--graphique',
        dest="graphique", action="store_true",
        help="Activer le mode graphique."
    )

    # On crée une argument aui nous servira à récupérer l'idul
    parser.add_argument(
        'idul',
        type=str, help='IDUL du joueur.'
    )

    return parser.parse_args() # On retourne les arguments


ARGS = analyser_commande() # Analyse la liste de commande
 
if ARGS.automatique: # Si l'option -a est entrée on lance le mode automatique
    DEBUT = api.débuter_partie(ARGS.idul) # On commence la partie
    PARTIE = quoridor.Quoridor(DEBUT[1]["joueurs"], DEBUT[1]["murs"]) 
    # On place la partie dans la classe Quoridor
    boucle = 1
    while boucle == 1:
        print(str(PARTIE))
        liste = api.lister_parties(ARGS.idul)
        # On joue notre coup
        PARTIE.jouer_coup(1)
        for liste in liste:
            if liste["id"] == DEBUT[0]:
                # On regarde si on a placé un mur ou si on c'est déplacé
                if PARTIE.joueur1["murs"] == liste["état"]["joueurs"][0]["murs"]:
                    # Si il y a un déplacement
                    api.jouer_coup(DEBUT[0], "D", (PARTIE.joueur1["pos"][0],
                                                   PARTIE.joueur1["pos"][0]))
                elif PARTIE.horizontaux != liste["état"]["murs"]["horizontaux"]:
                    # Si il y a un placement de mur horizontal
                    api.jouer_coup(DEBUT[0], "MH", (liste["état"]["murs"]["horizontaux"][0]))
                else:
                    # Si il y a placement de mur vertical
                    api.jouer_coup(DEBUT[0], "MV", (liste["état"]["murs"]["verticaux"][0]))

    # On va récupérer le coup jouer par le serveur
    liste = api.lister_parties(ARGS.idul)

    for liste in liste:
        if liste["id"] == DEBUT[0]:
            PARTIE.joueur2["murs"] = liste["état"]["joueurs"][1]["murs"]
            PARTIE.joueur2["pos"] = liste["état"]["joueurs"][1]["pos"]
            PARTIE.horizontaux = liste["état"]["murs"]["horizontaux"]
            PARTIE.verticaux = liste["état"]["murs"]["verticaux"]

if ARGS.graphique: # Si l'option 2 -x est entrée lance le mode graphique
    DEBUT = api.débuter_partie(ARGS.idul) # On commence la partie
    PARTIE = quoridorx.Quoridorx(DEBUT[1]["joueurs"], DEBUT[1]["murs"]) 
    # On place la partie dans la classe Quoridor
    boucle = 1
    while boucle == 1:
        # On affiche la partie
        PARTIE.afficher()
        # On va récupérer le coup de l'utilisateur
        TYPE_COUP = input("Entrez votre coup, (D, MH ou MV) : ") # Type de coup
        x = input("Entrez votre valeur x : ") # Pos x
        y = input("Entrez votre valeur y : ") # pos y

        api.jouer_coup(DEBUT[0], TYPE_COUP, (x, y)) # Pour jouer notre coup
        # sur le serveur
        # On change les valeurs dans notre classe
        x = int(x)
        y = int(y)
        if TYPE_COUP == "D":
            PARTIE.déplacer_jeton(1, (x, y))
        elif TYPE_COUP == "MH":
            PARTIE.placer_mur(1, (x, y), "horizontal")
        else:
            PARTIE.placer_mur(1, (x, y), "vertical")

        # On va récupérer le coup jouer par le serveur
        liste = api.lister_parties(ARGS.idul)

        for liste in liste:
            if liste["id"] == DEBUT[0]:
                PARTIE.joueur2["murs"] = liste["état"]["joueurs"][1]["murs"]
                PARTIE.joueur2["pos"] = liste["état"]["joueurs"][1]["pos"]
                PARTIE.horizontaux = liste["état"]["murs"]["horizontaux"]
                PARTIE.verticaux = liste["état"]["murs"]["verticaux"]

DEBUT = api.débuter_partie(ARGS.idul) # On commence la partie
PARTIE = quoridor.Quoridor(DEBUT[1]["joueurs"], DEBUT[1]["murs"]) 
# On place la partie dans la classe Quoridor
boucle = 1
while boucle == 1:

    print(str(PARTIE))
    # On va récupérer le coup de l'utilisateur
    TYPE_COUP = input("Entrez votre coup, (D, MH ou MV) : ") # Type de coup
    x = input("Entrez votre valeur x : ") # Pos x
    y = input("Entrez votre valeur y : ") # pos y

    api.jouer_coup(DEBUT[0], TYPE_COUP, (x, y)) # Pour jouer notre coup
    # sur le serveur
    # On change les valeurs dans notre classe
    x = int(x)
    y = int(y)
    if TYPE_COUP == "D":
        PARTIE.déplacer_jeton(1, (x, y))
    elif TYPE_COUP == "MH":
        PARTIE.placer_mur(1, (x, y), "horizontal")
    else:
        PARTIE.placer_mur(1, (x, y), "vertical")

    # On va récupérer le coup jouer par le serveur
    liste = api.lister_parties(ARGS.idul)

    for liste in liste:
        if liste["id"] == DEBUT[0]:
            PARTIE.joueur2["murs"] = liste["état"]["joueurs"][1]["murs"]
            PARTIE.joueur2["pos"] = liste["état"]["joueurs"][1]["pos"]
            PARTIE.horizontaux = liste["état"]["murs"]["horizontaux"]
            PARTIE.verticaux = liste["état"]["murs"]["verticaux"]