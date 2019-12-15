"""Ce module permet l'interaction de l'utilisateur avec les serveurs"""

import requests



def lister_parties(idul):
    """[Liste les parties d'un idul particulier]

    Arguments:
        idul {[string]} -- [Identifiant de la personne]

    Raises:
        RuntimeError: [Requête mal déroulée]

    Returns:
        [list] -- [parties jouées]
    """
    rep = requests.get('https://python.gel.ulaval.ca/quoridor/api/lister/', params={'idul': idul})
    if rep.status_code == 200:
        # la requête s'est déroulée normalement; décoder le JSON
        rep = rep.json()
        return rep["parties"][:20]
    raise RuntimeError(rep.status_code)


def débuter_partie(idul):
    """[Initialise une partie avec le serveur]

    Raises:
        RuntimeError: [Erreur de communication / Idul invalide]

    Returns:
        [tuple] -- [(Id, {État de jeu})]
    """
    rep = requests.post('https://python.gel.ulaval.ca/quoridor/api/débuter/', data={'idul': idul})
    rep = rep.json()
    if rep.get("message", False):
        raise RuntimeError(rep["message"])
    return rep["id"], rep["état"]


def jouer_coup(id_partie, type_coup, position):
    """[Joue un coup de la partie]

    Arguments:
        id_partie {[string]} -- [Identifiant de la partie]
        type_coup {[string]} -- [Type de coup effectué]
        position {[[list]]} -- [liste de coordonnées en ([x, y])]

    Raises:
        StopIteration: [Fin de la partie - Gagnant déclaré]
        RuntimeError: [Erreur de communication]

    Returns:
        [type] -- [description]
    """
    rep = requests.post('https://python.gel.ulaval.ca/quoridor/api/jouer/',
                        data={'id': id_partie, "type": type_coup, "pos": position})
    rep = rep.json()
    if rep.get("gagnant", False):
        raise StopIteration(rep["gagnant"])

    if rep.get("message", False):
        raise RuntimeError(rep["message"])
    return rep["état"]
