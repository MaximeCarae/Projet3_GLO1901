""" Class Quoridorx - Phase 3
Écrit par :
Maxime Carpentier
Vincent Bergeron
Ousmane Touré
Le 16 décembre 2019
Ce programme contient la classe avec toutes
les méthodes pour jouer au jeu Quoridor en graphique
"""

import quoridor
import turtle


class QuoridorX(quoridor.Quoridor):
    """
    Classe Quoridor, contient toutes les fonctions nécéssaires pour
    jouer au jeu Quoridor en mode graphique.
    """
    def afficher(self):
        """
        Fonction pour afficher le jeu en mode graphique
        """
        # On crée la fenêtre
        fen = turtle.Screen()
        fen.title("Jeu Quoridor")
        fen.setup(width=800, height=800)

        # On définie nos formes, les bords, les murs et les pions
        bord = ((0, 0), (0, 10), (600, 10), (600, 0), (0, 0))
        mur = ((0, 0), (0, 10), (-110, 10), (-110, 0), (0, 0))
        pion = ((-10, -10), (10, -10), (10, 10), (-10, 10), (-10, -10))
        turtle.addshape('pion', pion)
        turtle.addshape('bord', bord)
        turtle.addshape('mur', mur)

        # On trace les bords du plateau
        # On va ce placer dans le coin inférieur droit du plateau
        joe = turtle.Turtle()
        joe.penup()
        joe.backward(350)
        joe.left(90)
        joe.forward(300)
        joe.pendown()
        joe.shape('bord')
        joe.pencolor('black')
        joe.fillcolor('black')
        joe.stamp()

        # On fait tous les bords un par un
        joe.penup()
        joe.right(90)
        joe.forward(590)
        joe.pendown()
        joe.stamp()

        joe.penup()
        joe.right(90)
        joe.forward(590)
        joe.pendown()
        joe.stamp()

        joe.penup()
        joe.right(90)
        joe.forward(590)
        joe.pendown()
        joe.stamp()
        joe.penup()

        # On place les pions
        
        # On définie le pion du joueur 1 en rouge
        alex = turtle.Turtle()
        alex.shape('pion')
        alex.penup()
        alex.pencolor('red')
        alex.fillcolor('red')
        alex.backward(55)
        alex.left(90)
        alex.backward(280)

        # On définie le pion du joueur 2 en vert
        robot = turtle.Turtle()
        robot.shape('pion')
        robot.penup()
        robot.pencolor('green')
        robot.fillcolor('green')
        robot.backward(55)
        robot.left(90)
        robot.forward(290)

        # On place le pion du joueur 1 en fonction des coordonées
        x = (5 - self.etat["joueurs"][0]["pos"][0])*68 - 5
        y = (self.etat["joueurs"][0]["pos"][1] - 1)*68 + 10
        alex.forward(y)
        alex.left(90)
        alex.forward(x)

        # On place le pion du joueur 2 en fonction des coordonées
        x = (5 - self.etat["joueurs"][1]["pos"][0])*68 - 5
        y = (9 - self.etat["joueurs"][1]["pos"][1])*68 +16
        robot.backward(y)
        robot.right(90)
        robot.backward(x)

        # On place ce place à l'origine pour les murs

        # On définie le turtle pour les murs
        mure = turtle.Turtle()
        mure.shape('mur')
        mure.penup()
        mure.pencolor('blue')
        mure.fillcolor('blue')
        mure.backward(370)
        mure.right(90)
        mure.forward(300)
        mure.left(90)

        # On place d'abord tous les murs verticaux un par un en lisant la liste
        for liste in self.etat["murs"]["verticaux"]:
            x = (liste[0] - 1)*68 + 10
            y = (liste[1] - 1)*68 + 15
            mure.forward(x)
            mure.left(90)
            mure.forward(y)
            mure.right(90)
            mure.stamp()
            mure.left(90)
            mure.backward(y)
            mure.right(90)
            mure.backward(x)
        
        # On change le sens de la forme
        mure.right(90)

        # On place les murs horizontaux
        for liste in self.etat["murs"]["verticaux"]:
            x = (liste[0] - 1)*68 + 30
            y = (liste[1] - 1)*68
            mure.backward(y)
            mure.left(90)
            mure.forward(x)
            mure.right(90)
            mure.stamp()
            mure.left(90)
            mure.backward(x)
            mure.right(90)
            mure.forward(y)
        
        # On cache le turtle des murs dans les bords du plateau
        mure.fillcolor('black')
        mure.pencolor('black')
        mure.left(90)
        mure.forward(10)
        mure.right(90)
        mure.backward(10)

        