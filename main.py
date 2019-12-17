import argparse
import api
from quoridorx import QuoridorX


def analyser_commande():
    """[Parse la commande]
    
    Returns:
        [] -- [JSP]
    """
    parser = argparse.ArgumentParser(
        description="Jeu Quoridor - phase 3"
    )

    # Nom du joueur
    parser.add_argument(
        "idul", metavar="idul", help="IDUL du joueur."
    )
    # Mode auto
    parser.add_argument(
        '-a', '--automatique', dest='auto', action = 'store_true', 
        help = 'Activer le mode automatique.'
    )
    # Mode graph
    parser.add_argument(
        '-x', '--graphique', dest='fenetre', action = 'store_true',
        help = 'Activer le mode graphique.'
    )

    return parser.parse_args()


# Classe qui encapsule une partie

class Partie:
    def __init__(self, idul, auto, fenetre, api = api):
        self.idul = idul
        self.auto = auto
        self.fenetre = fenetre
        self.api = api
        if not auto:
            print("Utilisation: <Coup> <position x> <position y>\n" +
                    "Types de coups:\nD: Déplacer le pion\nMV: Mur vertical\n" +
                    "MH: Mur horizontal", sep=""
                    )
        self.jouer_partie()
    
    # Initialise une partie
    def jouer_partie(self):
        self.id, self.etat = api.débuter_partie(self.idul)
        self.partie = QuoridorX(["auto", "serveur"])
        self.jouer_tour()
    
    
    def jouer_tour(self):
        """[Effectue un tour de la partie de jeu]

        Returns:
            [None] -- []
        """
        while(True):
            # Afficher l'état de jeu (graphique ou ASCII, selon self.fenetre)
            arg_coup = self.afficher_partie()

            # Fonction qui analyse les entrées de la ligne de commande
            def parse_move():
                string = input("Entrez votre coup ")
                if string in ("q", "Q"):
                    return "q"
                if string in ("a", "A"):
                    print("Utilisation: <Coup> <position x> <position y>\n" +
                        "Types de coups:\nD: Déplacer le pion\nMV: Mur vertical\n" +
                        "MH: Mur horizontal", sep=""
                        )
                    return parse_move()
                try:
                    string = string.split(" ")
                    return string[0], [int(string[1]), int(string[2])]
                except:
                    print("Mauvaise entrée. Réessayez")
                    return parse_move()

            # Si mode pas automatique: Analyser les entrées de la ligne de commande
            if not self.auto:
                arg_coup = parse_move()
                if arg_coup == "q":
                    return None
            # Si mode automatique: caller jouer_coup pour le joueur 1
            else:
                coup =  self.partie.jouer_coup(1)
                arg_coup = coup[0], coup[1]
                print("\n\n\n\n", arg_coup, "\n\n\n\n")
                

            # Update l'état de jeu pour rester synchronisé avec l'état de jeu du serveur 
            try:
                self.partie.etat = self.api.jouer_coup(self.id, arg_coup[0], arg_coup[1])
                # Le serveur renvoie les positions des personnages en listes et non tuples -> conversion en tuple
                for i in range(2):
                    self.partie.etat["joueurs"][i]["pos"] = tuple(self.partie.etat["joueurs"][i]["pos"])


            # Exception si joueur est gagnant
            except StopIteration as stop_iter:
                print("Joueur gagnant: {}".format(stop_iter))
                return None

            # Exception si ça plante
            except RuntimeError as run_time_error:
                print("Erreur: {}".format(run_time_error))



    def afficher_partie(self):
        if self.fenetre:
            self.coup = self.partie.afficher()
        else:
            print(self.partie)
    






if __name__ == "__main__":
    commande = analyser_commande()
    Partie(commande.idul, commande.auto, commande.fenetre)
