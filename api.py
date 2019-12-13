""" api du programme Jeu Quorridor - Phase 1
Écrit par Maxime Carpentier 111 095 058
Le 11 novembre 2019
Ce programme contient les fonctions pour
la communication avec le serveur
"""


import requests # On import requests pour les communications avec le serveur


def lister_parties(idul):
    """ Fonction lister_parties
    Recoit en argument l'idul du joueur dont on veut lister les parties
    Retourne s'il n'y a pas d'erreur une liste des 20 dernières parties.
    """
    # On note l'adresse du serveur
    url_base = 'https://python.gel.ulaval.ca/quoridor/api/'

    # On récupère les données dans l'onglet lister/ du serveur avec
    # l'idul en paramètre
    rep = requests.get(url_base+'lister/', params={'idul' : idul})
    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        try:
            # On essaie de regarder la liste des parties et de retourner
            # les 20 premières
            return rep.json()["parties"][0:19]
        except KeyError:
            pass # Si on a un message, on a une keyError et
                # on passe à la suite
        try:
            # On essaie de regarder le message d'erreur
            raise RuntimeError(rep.json()["message"]) # S'il y a un message
            # d'erreur on soulève une une erreur RuntimeError
            # et on affiche le message d'erreur
        except KeyError:
            pass # S'il n'y a pas de message on passerait à la
        # suite mais il y aurait déjà eu le retourne pour la liste de parties
    else:
        # S'il y a un problème avec la requète on affiche le message d'erreur
        # On le coupe en morceau pour ne pas dépasser la colonne 80
        erreur = f"Le GET sur {url_base+'lister'} a produit le code d'erreur"
        erreur = erreur + str(rep.status_code) + "."
        return erreur

def débuter_partie(idul):
    """ Fonction débuter_partie
    On accepte un idul en paramètre pour créer une nouvelle partie
    On returne un tuple avec l'id de la partie et son état initial.
    """
    # On note l'adresse du serveur
    url_base = 'https://python.gel.ulaval.ca/quoridor/api/'

    # On crée la partie et on récupère les données dans l'onglet débuter/
    # du serveur avec l'idul en paramètre
    rep = requests.post(url_base+'débuter/', data={'idul': idul})

    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        try: # Si on reçoit un message d'erreur on affiche une RuntimeError
             # et le message
            raise RuntimeError(rep.json()["message"])
        except KeyError:
            pass # S'il n'y a pas de message on passe à la suite
        try: # Si on a reçu l'id et l'état de la partie on les retournes
             # dans un tuple
            return (rep.json()["id"], rep.json()["état"])
        except KeyError:
            pass # Sinon on passe
    else:
        # S'il y a un problème avec la requéte on affiche l'erreur
        # On le coupe en morceau pour ne pas dépasser la colonne 80
        erreur = f"Le GET sur {url_base+'debuter'} a produit le code d'erreur"
        erreur = erreur + str(rep.status_code) + "."
        return erreur

def jouer_coup(id_partie, type_coup, position):
    """ Fonction jouer_coup
    La fonction reçoit en paramètre un id de partie, le type de coup et
    la position du coup.
    """
    # On note l'adresse du serveur
    url_base = 'https://python.gel.ulaval.ca/quoridor/api/'

    # On fait les changements en envoyant les données dans l'onglet jouer/
    # du serveur avec l'id, le type de coup et la position en paramètre
    # On reçoit soit un message d'erreur, soit un nom de gagnant soit
    # l'état de la partie
    rep = requests.post(url_base+'jouer/',
                        data={'id' : id_partie, 'type' : type_coup, 'pos' : position})

    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        try: # Si on reçoit un message on l'affiche avec une RuntimeError
            raise RuntimeError(rep.json()["message"])
        except KeyError:
            pass # Sinon on passe
        try: # Si on reçoit un gagnant on l'affiche avec une StopIteration
            raise StopIteration(rep.json()["gagnant"])
        except KeyError:
            pass # Sinon on passe
        try: # Si on reçoit le nouvel état de la partie on le retourne
            return rep.json()["état"]
        except KeyError:
            pass # Sinon on passe
    else:
        # S'il y a un problème avec la requète on affiche l'erreur
        # On le coupe en morceau pour ne pas dépasser la colonne 80
        erreur = f"Le GET sur {url_base+'jouer'} a produit le code d'erreur"
        erreur = erreur + str(rep.status_code) + "."
        return erreur
