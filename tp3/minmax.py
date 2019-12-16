

def minMax(partie, joueurMax, n = 3):
        # La fonction est initialisée avec le dictionnaire d'état de la partie en cours
        # Conditions limites: Le joueur 1 ou 2 remporte la partie: +- 50 de valeur au noeud
        etat = partie.état_partie()
        if etat["joueurs"][0]["pos"][1] == 9:
            return 5000
        elif etat["joueurs"][1]["pos"][1] == 1:
            return -5000
        
        # Conditions si nombre de récursions écoulées: Score assigné selon une fonction au pif
        if not n:
            return 50 * (etat["joueurs"][0]["pos"][1])

        # Construction du graphe de la partie            
        graphe = construire_graphe(
            [joueur['pos'] for joueur in etat['joueurs']],
            etat['murs']['horizontaux'],
            etat['murs']['verticaux']
        )

        # 3 choix de jeu considérés à chaque noeud: Partir par le chemin le plus court pour gagner, ou placer
        # un mur horizontal devant l'adversaire ou un mur vertical à côté de lui
        if joueurMax:
            alpha = -1000

            # Cas 1: Déplacer le jeton
            partie = Quoridor(etat["joueurs"], etat["murs"])
            partie.déplacer_jeton(1, nx.shortest_path(graphe,
                                               (etat["joueurs"][0]["pos"][0],
                                                etat["joueurs"][0]["pos"][1]),
                                               'B1')[1])
            alpha = max(alpha, minMax(partie, False, n - 1))

            # S'il reste des murs au joueur: placer un mur dans face de l'adversaire  
            # Mur horizontal                
            if etat["joueurs"][0]["murs"]:
                partie = Quoridor(etat["joueurs"], etat["murs"])
                mur = placer_mur_auto(partie, 1, etat["joueurs"][1]["pos"], "horizontal")
                if mur:
                    alpha = max(alpha, minMax(partie, False, n - 1))

            # Mur vertical s'il reste des murs
            if etat["joueurs"][0]["murs"]:
                partie = Quoridor(etat["joueurs"], etat["murs"])
                mur = placer_mur_auto(partie, 1, etat["joueurs"][1]["pos"], "vertical")
                if mur:
                    alpha = max(alpha, minMax(partie, False, n - 1))
            return alpha
        else:
            beta = 1000

            # Cas 1: Déplacer le jeton
            partie = Quoridor(etat["joueurs"], etat["murs"])

            partie.déplacer_jeton(2, nx.shortest_path(graphe,
                                               (etat["joueurs"][1]["pos"][0],
                                                etat["joueurs"][1]["pos"][1]),
                                               'B2')[1])
            beta = min(beta, minMax(partie, True, n - 1))

            # S'il reste des murs au joueur: placer un mur dans face de l'adversaire  
            # Mur horizontal                
            if etat["joueurs"][1]["murs"]:
                partie = Quoridor(etat["joueurs"], etat["murs"])
                mur = placer_mur_auto(partie, 2, etat["joueurs"][0]["pos"], "horizontal")
                if mur:
                    beta = min(beta, minMax(partie, True, n - 1))

            # Mur vertical s'il reste des murs
            if etat["joueurs"][1]["murs"]:
                partie = Quoridor(etat["joueurs"], etat["murs"])
                mur = placer_mur_auto(partie, 2, etat["joueurs"][0]["pos"], "vertical")
                if mur:
                    beta = min(beta, minMax(partie, True, n - 1))
            return beta
        



# Fonction qui tente de placer un mur pour bloquer un joueur
def placer_mur_auto(partie, joueur, position, type_mur):
    x, y = position
    try:
        partie.placer_mur(joueur, position, type_mur)
    except:
        if type_mur == "horizontal":
            if x == 9:
                return False
            return placer_mur_auto(partie, joueur, (x + 1, y), "horizontal")
        if type_mur == "vertical":
            if y == 9:
                return False
            return placer_mur_auto(partie, joueur, (x, y + 1), "vertical")
    return x, y
