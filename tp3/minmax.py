from numpy.random import uniform


def minMax(joueurMax, etat, n = 5):
        # On utilise un dictionnaire d'état qui sera mis à jour sur chaque récursion; la fonction est initialisée
        # avec le dictionnaire d'état de la partie en cours
        
        # Conditions limites: Le joueur 1 ou 2 remporte la partie: +- 50 de valeur au noeud
        if etat["joueurs"][0]["pos"][1] == 9:
            return 50
        elif etat["joueurs"][1]["pos"][1] == 1:
            return -50
        
        # Conditions si nombre de récursions écoulées: Score assigné selon une fonction au pif
        if not n:
            return etat["joueurs"][0]["pos"][1] - (9 - etat["joueurs"][1]["pos"][1])


        # Construction du graphe de l'état            
        graphe = construire_graphe(
            [joueur['pos'] for joueur in etat['joueurs']],
            etat['murs']['horizontaux'],
            etat['murs']['verticaux']
        )

        # La plupart du temps (~80% ou si le joueur n'a plus de murs): Déplacement du jeton 
        if uniform(0, 1, 1) < 0.99 or not etat["joueurs"][1 - joueurMax]["murs"]:
            if joueurMax:
                alpha = -1000
                nextMoves = list(graphe.successors(etat["joueurs"][0]['pos']))[:-1]
                print(nextMoves, joueurMax, n)
                for move in nextMoves:
                    print(move, joueurMax, n)
                    # Mise à jour du dictionnaire
                    etat["joueurs"][0]["pos"] = move
                    v = minMax(False, etat, n - 1)
                    if alpha <= v:
                        alpha = v
                return alpha
            else:
                beta = 1000
                nextMoves = list(graphe.successors(etat["joueurs"][1]['pos']))[:-1]
                print(nextMoves, joueurMax, n)
                for move in nextMoves:
                    print(move, joueurMax, n)
                    etat["joueurs"][1]["pos"] = move
                    v = minMax(True, etat, n - 1)
                    if v <= beta:
                        beta = v
                return beta
        
        # Sinon (~20%) placer un mur dans face du joueur adverse, renvoyer le même score que si n = 0.
        else:
            if joueurMax:
                if [etat["joueurs"][1]["pos"][0], etat["joueurs"][1]["pos"][1] - 1] not in etat["murs"]["horizontaux"]:
                    etat["murs"]["horizontaux"] += [etat["joueurs"][1]["pos"][0], etat["joueurs"][1]["pos"][1] - 1]
                    etat["joueurs"][0]["murs"] -= 1
                # Même fonction de score que si cas final
                return etat["joueurs"][0]["pos"][1] - (9 - etat["joueurs"][1]["pos"][1])
            else:
                if [etat["joueurs"][0]["pos"][0], etat["joueurs"][0]["pos"][1] + 1] not in etat["murs"]["horizontaux"]:
                    etat["murs"]["horizontaux"] += [etat["joueurs"][0]["pos"][0], etat["joueurs"][0]["pos"][1] + 1]
                    etat["joueurs"][1]["murs"] -= 1
                return etat["joueurs"][0]["pos"][1] - (9 - etat["joueurs"][1]["pos"][1])
