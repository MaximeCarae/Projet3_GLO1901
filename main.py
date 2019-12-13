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
    a = 2# Lancement auto

if ARGS.graphique: # Si l'option 2 -x est entrée lance le mode graphique
    a = 1# Lancement graphique

DEBUT = api.débuter_partie(ARGS.idul) # On commence la partie
PARTIE = quoridor.Quoridor(DEBUT[1]["joueurs"], DEBUT[1]["murs"]) 
# On place la partie dans la classe Quoridor

