""" Main du programme Jeu Quorridor - Phase 2
Écrit par :
Maxime Carpentier
Vincent Bergeron
Ousmane Touré
Le 2 décembre 2019
Ce programme contient la classe avec toutes
les méthodes pour jouer au jeu Quoridor
"""


import networkx as nx
from numpy.random import uniform


class Quoridor:
    """
    Classe Quoridor, contient toutes les fonctions nécéssaires pour
    jouer au jeu Quoridor.
    """
    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        :param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui
        débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
        Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
        l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir
        une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il
        peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.

        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun murs placé sur le jeu.

        :raises QuoridorError: si l'argument 'joueurs' n'est pas itérable.
        :raises QuoridorError: si l'itérable de joueurs en contient plus de deux.
        :raises QuoridorError: si le nombre de murs qu'un joueur peut placer est >10, ou négatif.
        :raises QuoridorError: si la position d'un joueur est invalide.
        :raises QuoridorError: si l'argument 'murs' n'est pas un dictionnaire lorsque présent.
        :raises QuoridorError: si le total des murs placés et plaçables n'est pas égal à 20.
        :raises QuoridorError: si la position d'un murs est invalide.
        """
        # On vérifie si joueur est itérable, si invalide on soulève une erreur
        if not isinstance(joueurs, list):
            raise QuoridorError
        # On vérifie le nombre de joueur, si invalide on soulève une erreur
        if len(joueurs) > 2:
            raise QuoridorError
        # On différencie si c'est une chaine de charactère ou un dictionnaire
        # et on initialise les paramètres dans un dictionnaire en fonction
        if isinstance(joueurs[0], str):
            # Charactère donc nouvelle partie
            joueur1 = {'nom' : joueurs[0], 'murs' : 10, 'pos' : (5, 1)}
            joueur2 = {'nom' : joueurs[1], 'murs' : 10, 'pos' : (5, 9)}
        elif isinstance(joueurs[0], dict):
            # Dictionnaire donc partie en cours
            joueur1 = {'nom' : joueurs[0]['nom'],
                            'murs' : joueurs[0]['murs'],
                            'pos' : joueurs[0]['pos']}
            joueur2 = {'nom' : joueurs[1]['nom'],
                            'murs' : joueurs[1]['murs'],
                            'pos' : joueurs[1]['pos']}
        # Si un joueur à un nombre de murs invalide on soulève une erreur
        if ((joueur1['murs'] < 0) or (joueur1['murs'] > 10) or
                (joueur2['murs'] < 0) or (joueur2['murs'] > 10)):
            raise QuoridorError
        # On vérifie la position des joueurs, si invalide on soulève une erreur
        if (not 1 <= joueur1['pos'][0] <= 9 or
                not 1 <= joueur1['pos'][1] <= 9 or
                not 1 <= joueur2['pos'][0] <= 9 or
                not 1 <= joueur2['pos'][1] <= 9):
            raise QuoridorError
        # On vérifie le type de murs, si invalide on soulève une erreur
        if ((murs is not None) and not isinstance(murs, dict)):
            raise QuoridorError
        # Si il y a des murs, on enregistre leurs positions
        if murs is not None:
            verticaux = murs['verticaux']
            horizontaux = murs['horizontaux']
        else:
            verticaux = []
            horizontaux = []

        # On vérifie la position des murs verticaux,
        # si invalide on soulève une erreur
        for i in verticaux:
            if (not 2 <= i[0] <= 9 or
                    not 1 <= i[1] <= 8):
                raise QuoridorError
        # On vérifie la position des murs horizontaux,
        # si invalide on soulève une erreur
        for i in horizontaux:
            if (not 1 <= i[0] <= 8 or
                    not 2 <= i[1] <= 9):
                raise QuoridorError

        # On vérifie le nombre de murs en jeu, si invalide on soulève une erreur
        if ((murs is not None) and (len(verticaux) + len(horizontaux)
                                    + joueur1['murs']
                                    + joueur2['murs'] != 20)):
            raise QuoridorError
        elif ((murs is None) and (joueur1['murs']
                                  + joueur2['murs'] != 20)):
            raise QuoridorError
        
        self.etat = {
            'joueurs': [
                joueur1,
                joueur2,
            ],
            'murs': {
                'horizontaux': horizontaux,
                'verticaux': verticaux
            }
        }


    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie.
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """

        liste = [[" " for j in range(35)] for i in range(17)]

        # Ajouter points
        for i in range(0, 17, 2):
            for j in range(1, 34, 4):
                liste[i][j] = "."

        # Ajouter lignes horizontales dans liste
        for j, i in self.etat["murs"]["verticaux"]:
            liste[i * 2 - 2][j * 4 - 5] = "|"
            liste[i * 2 - 1][j * 4 - 5] = "|"
            liste[i * 2][j * 4 - 5] = "|"

        # Ajouter lignes verticales dans la liste
        for j, i in self.etat["murs"]["horizontaux"]:
            for k in range(4 * j - 4, 4 * j + 3):
                liste[2 * i - 3][k] = "-"

        # Ajouter la position du premier joueur
        liste[2 * self.etat["joueurs"][0]["pos"][1] - 2][4 * self.etat["joueurs"][0]["pos"][0] - 3] = "1"

        # Ajouter la position du second joueur
        liste[2 * self.etat["joueurs"][1]["pos"][1] - 2][4 * self.etat["joueurs"][1]["pos"][0] - 3] = "2"

        # Inverser la liste
        liste.reverse()

        #Ajouter les numeros en avant
        for i, value in enumerate(liste):
            if not i % 2:
                liste[i] = str(9 - (i // 2)) + " |" + "".join(value) + "|"
            else:
                liste[i] = "  |" + "".join(value) + "|"

        # Ajout de la première ligne
        liste.insert(0, "Légende: 1={}, 2={}\n   -----------------------------------".format(
            self.etat["joueurs"][0]["nom"], self.etat["joueurs"][1]["nom"]))

        # Ajout de la dernière ligne
        liste.insert(18, "--|-----------------------------------\n" +
                     "  | 1   2   3   4   5   6   7   8   9")

        # Afficher la liste
        return "\n".join(liste)


    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la position est invalide (en dehors du damier).
        :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
        """
        # On vérifie si le numéro de joueur est valide, sinon on soulève
        # une erreur
        if joueur not in [1, 2]:
            raise QuoridorError

        # On vérifie si la position est valide, sinon on soulève une erreur
        if (not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9 or
                not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9):
            raise QuoridorError

        # On enregistre l'état de la partie, et on fait un graphe
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux'])

        # On vérfie le joueur sélectionné et si le coup est possible on le joue

        # Liste des coups possible
        possi = list(graphe.successors(self.etat["joueurs"][joueur - 1]['pos']))
        for i in possi:
            # Si notre coup est dans la liste on le joue 
            if position == i:
                self.etat["joueurs"][joueur - 1]['pos'] = position
        # Si on n'a pas joué de coup on soulève une erreur car la pos est
        # invalide
        if self.etat["joueurs"][joueur - 1]['pos'] != position:
            raise QuoridorError



    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {
                'horizontaux': [...],
                'verticaux': [...],
            }
        }

        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
        associée à sa position sur le damier. Une position est représentée par un tuple
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un murs horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        murs vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
        # On retourne simplement l'état de la partie dans un dictionnaire
        return self.etat


    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        murs horizontal ou vertical.
        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """
        # On vérifie si la partie est terminée, ou si le numéro de joueur est
        # mauvais, si c'est le cas on soulève une erreur
        if joueur not in [1, 2] or self.partie_terminée():
            raise QuoridorError

        # On créé le graphe pour pouvoir tester les positions possibles
        état = self.état_partie()
        graphe = construire_graphe(
            [joueur['pos'] for joueur in état['joueurs']],
            état['murs']['horizontaux'],
            état['murs']['verticaux']
        )

        # Si on avait sélectionné le joueur 1, on le place à la meilleure
        # position possible état["joueurs"][0]
        if (joueur == 1 and nx.has_path(graphe, (état["joueurs"][0]["pos"][0],
                                                 état["joueurs"][0]["pos"][1]),
                                        'B1')):
            self.déplacer_jeton(1, nx.shortest_path(graphe,
                                                   (état["joueurs"][0]["pos"][0],
                                                    état["joueurs"][0]["pos"][1]),
                                                   'B1')[1])
            return self.état_partie()["joueurs"][0]["pos"], False
        # Si on avait sélectionné le joueur 2, on le place à la meilleure
        # position possible
        if (joueur == 2 and nx.has_path(graphe, (état["joueurs"][1]["pos"][0],
                                                 état["joueurs"][1]["pos"][1]),
                                        'B2')):
            self.déplacer_jeton(2, nx.shortest_path(graphe,
                                                   (état["joueurs"][1]["pos"][0],
                                                    état["joueurs"][1]["pos"][1]),
                                                   'B2')[1])
            return self.état_partie()["joueurs"][1]["pos"], False
        
    """
    def jouer_coup(self, joueur):
        etat = self.état_partie()
        graphe = construire_graphe(
            [joueur['pos'] for joueur in etat['joueurs']],
            etat['murs']['horizontaux'],
            etat['murs']['verticaux']
        )

        if joueur == 1:
            alpha = -5000
            nextMoves = list(graphe.successors(etat["joueurs"][0]['pos']))[:-1]
            print(nextMoves)
            for move in nextMoves:
                # Mise à jour du dictionnaire
                etat["joueurs"][0]["pos"] = move
                v = minMax(False, etat)
                if v > alpha:
                    alpha = v
                    bestMove = move
        else:
            beta = 5000
            nextMoves = list(graphe.successors(etat["joueurs"][1]['pos']))[:-1]
            for move in nextMoves:
                etat["joueurs"][1]["pos"] = move
                v = minMax(True, etat)
                if v <= beta:
                    beta = v
                    bestMove = move

        if etat["murs"] != self.état_partie()["murs"]:
            return bestMove, True
        return bestMove, False
    """




    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.
        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        # On vérifie si le joueur 1 ou 2 sont à la dernière position,
        # si c'est le cas on retourne le nom du joueur. Sinon on retourne False
        if self.etat["joueurs"][0]['pos'][1] == 9:
            return self.etat["joueurs"][0]['nom']

        if self.etat["joueurs"][1] == 1:
            return self.etat["joueurs"][1]['nom']

        return False


    def placer_mur(self, joueur, position, orientation):
        """
        Pour le joueur spécifié, placer un murs à la position spécifiée.
        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du murs.
        :param orientation: l'orientation du murs ('horizontal' ou 'vertical').
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si un murs occupe déjà cette position.
        :raises QuoridorError: si la position est invalide pour cette orientation.
        :raises QuoridorError: si le joueur a déjà placé tous ses murs.
        """
        # On vérifie si le numéro de joueur est valide, sinon on
        # soulève une erreur
        if joueur not in [1, 2]:
            raise QuoridorError
        # On vérifie si l'orientation du mur est valide ou s'il y a déjà un
        # murs à cette position, sinon on soulève une erreur 
        if ((orientation == "vertical" and position in self.etat['murs']['verticaux']) or
                (orientation == "horizontal" and position in self.etat['murs']['horizontaux'])):
            raise QuoridorError

        # On vérifie la position des murs verticaux,
        # si invalide on soulève une erreur
        if orientation == 'vertical':
            if (not 2 <= position[0] <= 9 or
                    not 1 <= position[1] <= 8):
                raise QuoridorError
        # On vérifie la position des murs horizontaux,
        # si invalide on soulève une erreur
        if orientation == 'horizontal':
            if (not 1 <= position[0] <= 8 or
                    not 2 <= position[1] <= 9):
                raise QuoridorError

        # On vérifie si le joueur 1 et sélectionné et qu'il a
        # placé tous ses murs, on soulève une erreur
        if (joueur == 1 and not self.etat["joueurs"][0]["murs"]):
            raise QuoridorError

        # On vérifie si le joueur 2 et sélectionné et dans qu'il a
        # placé tous ses murs, on soulève une erreur
        if (joueur == 2 and not self.etat["joueurs"][1]["murs"]):
            raise QuoridorError

        # On place le position du murs dans sa liste correspondante si aucune
        # des erreurs possiblent n'a été soulevées
        if orientation == "vertical":
            self.etat['murs']['verticaux'].append(position)
        if orientation == "horizontal":
            self.etat['murs']['horizontaux'].append(position)

        # On incrémente le nombre de mur restant
        if joueur == 1:
            self.etat["joueurs"][0]["murs"] += -1
        if joueur == 2:
            self.etat["joueurs"][1]["murs"] += -1




class QuoridorError(Exception):
    """
    Gère les exceptions dans la class Quoridor
    """
    pass


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe











def minMax(joueurMax, etat, n = 11, verbose = False, verbose_fin = False):
        # On utilise un dictionnaire d'état qui sera mis à jour sur chaque récursion; la fonction est initialisée
        # avec le dictionnaire d'état de la partie en cours
        # Conditions limites: Le joueur 1 ou 2 remporte la partie: +- 50 de valeur au noeud
        if etat["joueurs"][0]["pos"][1] == 9:
            if verbose_fin or verbose:
                print(etat, "aaaaaaaaaaa")
            return 5000
        elif etat["joueurs"][1]["pos"][1] == 1:
            if verbose_fin or verbose:
                print(etat, "aaaaaaaaaaa")
            return -5000
        
        # Conditions si nombre de récursions écoulées: Score assigné selon une fonction au pif
        if not n:
            if verbose_fin:
                print(etat)
            return 50 * (etat["joueurs"][0]["pos"][1])


        # Construction du graphe de l'état            
        graphe = construire_graphe(
            [joueur['pos'] for joueur in etat['joueurs']],
            etat['murs']['horizontaux'],
            etat['murs']['verticaux']
        )

        # La plupart du temps (~80% ou si le joueur n'a plus de murs): Déplacement du jeton 
        if uniform(0, 1, 1) <= 1 or not etat["joueurs"][1 - joueurMax]["murs"]:
            if joueurMax:
                alpha = -1000
                nextMoves = list(graphe.successors(etat["joueurs"][0]['pos']))[:-1]
                if verbose:
                    print(nextMoves, joueurMax, n)
                for move in nextMoves:
                    if verbose:
                        print(move, joueurMax, n)
                    # Mise à jour du dictionnaire
                    etat["joueurs"][0]["pos"] = move
                    v = max(alpha, minMax(False, etat, n - 1))
                return alpha
            else:
                beta = 1000
                nextMoves = list(graphe.successors(etat["joueurs"][1]['pos']))[:-1]
                if verbose:
                    print(nextMoves, joueurMax, n)
                for move in nextMoves:
                    if verbose:
                        print(move, joueurMax, n)
                    etat["joueurs"][1]["pos"] = move
                    min(beta, minMax(True, etat, n - 1))
                return beta
        
        # Sinon (~20%) placer un mur dans face du joueur adverse, renvoyer le même score que si n = 0.
        else:
            if joueurMax:
                if list(etat["joueurs"][1]["pos"]) not in etat["murs"]["horizontaux"]:
                    etat["murs"]["horizontaux"] += list(etat["joueurs"][1]["pos"])
                    etat["joueurs"][0]["murs"] -= 1
                # Même fonction de score que si cas final
                return etat["joueurs"][0]["pos"][1] - (9 - etat["joueurs"][1]["pos"][1])
            else:
                if list(etat["joueurs"][0]["pos"]) not in etat["murs"]["horizontaux"]:
                    etat["murs"]["horizontaux"] += list(etat["joueurs"][0]["pos"])
                    etat["joueurs"][1]["murs"] -= 1
                return etat["joueurs"][0]["pos"][1] - (9 - etat["joueurs"][1]["pos"][1])