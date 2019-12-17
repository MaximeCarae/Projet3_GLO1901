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
from copy import deepcopy

###### si le mode automatique est lent, réduire nDemitours

nDemitours = 8

######

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
        if (murs is not None) and (len(verticaux) + len(horizontaux)
                                    + joueur1['murs']
                                    + joueur2['murs']) != 20:
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
        
        x, y = position
        # On vérifie si la position est valide, sinon on soulève une erreur
        if not (1 <= x <= 9 and 1 <= y <= 9):
            raise QuoridorError

        # On enregistre l'état de la partie, et on fait un graphe
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux'])

        # On vérfie le joueur sélectionné et si le coup est possible on le joue

        # Liste des coups possible
        moves = list(graphe.successors(self.etat["joueurs"][joueur - 1]['pos']))
        for move in moves:
            # Si notre coup est dans la liste on le joue 
            if position == move:
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
            
        if joueur not in [1, 2] or self.partie_terminée():
            raise QuoridorError
        
        etat = deepcopy(self.état_partie())

        partie1 = Quoridor(deepcopy(etat["joueurs"]), deepcopy(etat["murs"]))
        partie2 = Quoridor(deepcopy(etat["joueurs"]), deepcopy(etat["murs"]))
        partie3 = Quoridor(deepcopy(etat["joueurs"]), deepcopy(etat["murs"]))

        # Construction du graphe de la partie            
        graphe = construire_graphe(
            [joueur['pos'] for joueur in etat['joueurs']],
            etat['murs']['horizontaux'],
            etat['murs']['verticaux']
        )

        # Même principe que la fonction minMax, mais on récupère le move le plus payant

        # 3 choix de jeu considérés à chaque noeud: Partir par le chemin le plus court pour gagner, ou placer
        # un mur horizontal devant l'adversaire ou un mur vertical à côté de lui
        if joueur == 1:
            alpha = -1000

            # Cas 1: Déplacer le jeton
            move = "D", nx.shortest_path(graphe,
                                               (partie1.etat["joueurs"][0]["pos"][0],
                                                partie1.etat["joueurs"][0]["pos"][1]),
                                               'B1')[1]

            partie1.déplacer_jeton(1, move[1])
            alpha = max(alpha, minMax(partie1, False))

            # S'il reste des murs au joueur: placer un mur dans face de l'adversaire  
            # Mur horizontal                
            if partie2.etat["joueurs"][0]["murs"]:
                mur = partie2.placer_mur_auto(1, nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][1]["pos"][0],
                                                partie3.etat["joueurs"][1]["pos"][1]),
                                               'B2')[1], "horizontal")
                if mur:
                    if alpha > minMax(partie2, False):
                        move = "MH", mur

            # Mur vertical s'il reste des murs

            if partie3.etat["joueurs"][0]["murs"] and nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][1]["pos"][0],
                                                partie3.etat["joueurs"][1]["pos"][1]),
                                               'B2')[1][1] == partie3.etat["joueurs"][1]["pos"][1]:
                mur = partie3.placer_mur_auto(1, nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][1]["pos"][0],
                                                partie3.etat["joueurs"][1]["pos"][1]),
                                               'B2')[1], "vertical")
                if mur:
                    if alpha > minMax(partie3, False):
                        move = "MV", mur

                        
            
        else:
            beta = 1000

            # Cas 1: Déplacer le jeton
            move = nx.shortest_path(graphe,
                                               (partie1.etat["joueurs"][1]["pos"][0],
                                                partie1.etat["joueurs"][1]["pos"][1]),
                                               'B2')[1]
            partie1.déplacer_jeton(1, move)
            beta = min(beta, minMax(partie1, True))

            # S'il reste des murs au joueur: placer un mur dans face de l'adversaire  
            # Mur horizontal                
            if partie2.etat["joueurs"][1]["murs"]:
                mur = partie2.placer_mur_auto(2, nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][0]["pos"][0],
                                                partie3.etat["joueurs"][0]["pos"][1]),
                                               'B1')[1], "horizontal")
                if mur:
                    if beta < minMax(partie2, True):
                        move = "MH", mur

            # Mur vertical s'il reste des murs

            if partie3.etat["joueurs"][1]["murs"] and nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][0]["pos"][0],
                                                partie3.etat["joueurs"][0]["pos"][1]),
                                               'B1')[1][1] == partie3.etat["joueurs"][0]["pos"][1]:
                mur = partie3.placer_mur_auto(2, nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][0]["pos"][0],
                                                partie3.etat["joueurs"][0]["pos"][1]),
                                               'B1')[1], "vertical")
                if mur:
                    if beta < minMax(partie3, True):
                        move = "MV", mur

        return move
        
            
        




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
        Pour le joueur spécifié, placer un mur à la position spécifiée.
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
        if (joueur not in [1, 2]) or (orientation not in ["vertical", "horizontal"]):
            raise QuoridorError

        x, y = position
        # On vérifie si l'orientation du mur est valide ou s'il y a déjà un
        # mur à cette position, sinon on soulève une erreur 
        if orientation == "horizontal":
            for i in range(x - 1, x + 2):
                if [i, y] in self.etat["murs"]["horizontaux"]:
                    raise QuoridorError
            if [x + 1, y - 1] in self.etat["murs"]["verticaux"]:
                raise QuoridorError
        else:
            for j in range(y - 1, y + 2):
                if [x, j] in self.etat["murs"]["verticaux"]:
                    raise QuoridorError
            if [x - 1, y + 1] in self.etat["murs"]["horizontaux"]:
                raise QuoridorError
                

        # Vérifie si un joueur est sur la position
        if list(position) in [self.etat["joueurs"][0]["pos"], self.etat["joueurs"][1]["pos"]]:
            raise QuoridorError

        # On vérifie la position des murs horizontaux si invalide on soulève une erreur
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
        
        # Vérifier si le mur empêche un joueur d'accéder à son objectif (contre les règles)
        etat_futur = deepcopy(self.état_partie())
        if orientation == "vertical":
            etat_futur['murs']['verticaux'].append(position)
        if orientation == "horizontal":
            etat_futur['murs']['horizontaux'].append(position)
        
        graphe = construire_graphe(
            [joueur['pos'] for joueur in etat_futur['joueurs']], 
            etat_futur['murs']['horizontaux'],
            etat_futur['murs']['verticaux']
        )

        if not (nx.has_path(graphe, etat_futur["joueurs"][0]["pos"], 'B1') and nx.has_path(graphe, etat_futur["joueurs"][1]["pos"], 'B2')):
            raise QuoridorError
        

        # On place le position du murs dans sa liste correspondante si aucune
        # des erreurs possiblent n'a été soulevées
        if orientation == "vertical":
            self.etat['murs']['verticaux'].append(position)
        if orientation == "horizontal":
            self.etat['murs']['horizontaux'].append(position)

        # On incrémente le nombre de murs restant
        if joueur == 1:
            self.etat["joueurs"][0]["murs"] -= 1
        if joueur == 2:
            self.etat["joueurs"][1]["murs"] -= 1
        


    # Fonction qui tente de placer un mur pour bloquer un joueur
    def placer_mur_auto(self, joueur, position, type_mur):
        x, y = position
        if joueur == 1:
            biaisXY = 1
            biaisYX = -1
        else:
            biaisXY = 0
            biaisYX = 0
        
        if type_mur == "horizontal":
            for i in [x, x - 1]:
                try:
                    self.placer_mur(joueur, (i, y + biaisXY), type_mur)
                    return i, y + biaisXY
                except:
                    continue
        else:
            if x > 5:
               for i in [x]:
                    try:
                        self.placer_mur(joueur, (i, y + biaisYX), type_mur)
                        return i, y + biaisYX
                    except:
                        continue
            else:
                for i in [x]:
                    try:
                        self.placer_mur(joueur, (i, y + biaisYX), type_mur)
                        return i, y + biaisYX
                    except:
                        continue
        return False





class QuoridorError(Exception):
    """
    Gère les exceptions dans la classe Quoridor
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









def minMax(partie, joueurMax, n = nDemitours, verbose = False):
        """[summary]
        
        Arguments:
            partie {[Quodidor]} -- [Une instance de Quoridor]
            joueurMax {[type]} -- [Joueur qui minimise ou maximise le score]
        
        Keyword Arguments:
            n {int} -- [Nombre de récursions] (default: {6})
            verbose {bool} -- [Renvoyer les états de jeu] (default: {False})
        
        Returns:
            [int] -- [Valeur d'un noeud]
        """
        biais = -30
        biaisMur = 50
        etat = deepcopy(partie.état_partie())

        if etat["joueurs"][0]["pos"][1] == 9:
            return 10000
        elif etat["joueurs"][1]["pos"][1] == 1:
            return -10000

        # Construction du graphe de la partie            
        graphe = construire_graphe(
            [joueur['pos'] for joueur in etat['joueurs']],
            etat['murs']['horizontaux'],
            etat['murs']['verticaux']
        )
        
        # Conditions si nombre de récursions écoulées: Score assigné selon une fonction au pif
        if not n:
            return 40 * (etat["joueurs"][1]["pos"][1] + (9 - etat["joueurs"][0]["pos"][1])) + 20 * (len(nx.shortest_path(graphe, etat["joueurs"][1]["pos"], 'B2')) - len(nx.shortest_path(graphe, etat["joueurs"][0]["pos"], 'B1')))

        # La fonction est initialisée avec le dictionnaire d'état de la partie en cours
        # Conditions limites: Le joueur 1 ou 2 remporte la partie: +- 50 de valeur au noeud
        partie1 = Quoridor(deepcopy(etat["joueurs"]), deepcopy(etat["murs"]))
        partie2 = Quoridor(deepcopy(etat["joueurs"]), deepcopy(etat["murs"]))
        partie3 = Quoridor(deepcopy(etat["joueurs"]), deepcopy(etat["murs"]))

        # 3 choix de jeu considérés à chaque noeud: Partir par le chemin le plus court pour gagner, ou placer
        # un mur horizontal ou un mur vertical dans le chemin le plus court de l'adversaire
        if joueurMax:
            alpha = -10000

            # Cas 1: Déplacer le jeton
            partie1.déplacer_jeton(1, nx.shortest_path(graphe,
                                               (partie1.etat["joueurs"][0]["pos"][0],
                                                partie1.etat["joueurs"][0]["pos"][1]),
                                               'B1')[1])
            if verbose:                                   
                print("-----------------------------------------\nCas 1: Joueur Max", partie1.etat, n)
            alpha = max(alpha, minMax(partie1, False, n - 1)) + biais

            # Cas 2
            # S'il reste des murs au joueur: placer un mur dans face de l'adversaire  
            # Mur horizontal                
            if partie2.etat["joueurs"][0]["murs"]:
                mur = partie2.placer_mur_auto(1, nx.shortest_path(graphe,
                                               (partie2.etat["joueurs"][1]["pos"][0],
                                                partie2.etat["joueurs"][1]["pos"][1]),
                                               'B2')[1], "horizontal")
                if mur:
                    if verbose:
                        print("-----------------------------------------\nCas 2: Joueur Max", partie2.etat, n)
                    alpha = max(alpha, minMax(partie2, False, n - 1)) + biaisMur

            # Mur vertical s'il reste des murs et que le chemin le plus court pour l'autre joueur est un déplacement vertical
        
            if partie3.etat["joueurs"][0]["murs"] and nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][1]["pos"][0],
                                                partie3.etat["joueurs"][1]["pos"][1]),
                                               'B2')[1][1] == partie3.etat["joueurs"][1]["pos"][1]:
                mur = partie3.placer_mur_auto(1, nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][1]["pos"][0],
                                                partie3.etat["joueurs"][1]["pos"][1]),
                                               'B2')[1], "vertical")
                if mur:
                    if verbose:
                        print("-----------------------------------------\nCas 3: Joueur Max", partie3.etat, n)
                    alpha = max(alpha, minMax(partie3, False, n - 1))
            return alpha
        
        else:
            beta = 10000

            # Cas 1: Déplacer le jeton

            partie1.déplacer_jeton(2, nx.shortest_path(graphe,
                                               (partie1.etat["joueurs"][1]["pos"][0],
                                                partie1.etat["joueurs"][1]["pos"][1]),
                                               'B2')[1])
            if verbose:
                print("-----------------------------------------\nCas 1: Joueur Min", partie1.etat, n)
            beta = min(beta, minMax(partie1, True, n - 1)) - biais

            # S'il reste des murs au joueur: placer un mur dans face de l'adversaire  
            # Mur horizontal

            if partie2.etat["joueurs"][1]["murs"]:
                mur = partie2.placer_mur_auto(2, nx.shortest_path(graphe,
                                               (partie2.etat["joueurs"][0]["pos"][0],
                                                partie2.etat["joueurs"][0]["pos"][1]),
                                               'B1')[1], "horizontal")
                if mur:
                    if verbose:
                        print("-----------------------------------------\nCas 2: Joueur Min", partie2.etat, n)
                    beta = min(beta, minMax(partie2, True, n - 1)) - biaisMur

            # Mur vertical s'il reste des murs

            if partie3.etat["joueurs"][1]["murs"] and nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][0]["pos"][0],
                                                partie3.etat["joueurs"][0]["pos"][1]),
                                               'B1')[1][1] == partie3.etat["joueurs"][0]["pos"][1]:
                mur = partie3.placer_mur_auto(2, nx.shortest_path(graphe,
                                               (partie3.etat["joueurs"][0]["pos"][0],
                                                partie3.etat["joueurs"][0]["pos"][1]),
                                               'B1')[1], "vertical")
                if mur:
                    if verbose:
                        print("-----------------------------------------\nCas 3: Joueur Max", partie3.etat, n)
                    beta = min(beta, minMax(partie3, True, n - 1))
            return beta
