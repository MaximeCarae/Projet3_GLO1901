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

class Quoridorx(quoridor.Quoridor):
    """
    Classe Quoridor, contient toutes les fonctions nécéssaires pour
    jouer au jeu Quoridor en mode graphique.
    """
    def afficher(self):
        """
        Fonction pour afficher le jeu en mode graphique
        """
        fen = turtle.Screen()
        fen.title("Jeu Quoridor")
        fen.setup(width=800, height=800)

        bord = ((0, 0), (0, 10), (600, 10), (600, 0), (0, 0))
        mur = ((0, 0), (0, 10), (-110, 10), (-110, 0), (0, 0))
        pion = ((-10, -10), (10, -10), (10, 10), (-10, 10), (-10, -10))
        turtle.addshape('pion', pion)
        turtle.addshape('bord', bord)
        turtle.addshape('mur', mur)

        # On trace les bords du plateau
        joe = turtle.Turtle()
        joe.penup()
        joe.backward(350) # avancer de 50 pixels
        joe.left(90)    # tourner de 90° en sens anti-horaire
        joe.forward(300) # avancer de 30 pixels
        joe.pendown()
        joe.shape('bord')
        joe.pencolor('black')
        joe.fillcolor('black')
        joe.stamp()

        joe.penup()
        joe.right(90)
        joe.forward(590) # avancer de 50 pixels
        joe.pendown()
        joe.shape('bord')
        joe.pencolor('black')
        joe.fillcolor('black')
        joe.stamp()

        joe.penup()
        joe.right(90)
        joe.forward(590) # avancer de 50 pixels
        joe.pendown()
        joe.shape('bord')
        joe.pencolor('black')
        joe.fillcolor('black')
        joe.stamp()

        joe.penup()
        joe.right(90)
        joe.forward(590) # avancer de 50 pixels
        joe.pendown()
        joe.shape('bord')
        joe.pencolor('black')
        joe.fillcolor('black')
        joe.stamp()
        joe.penup()

        # On place les pions
        
        alex = turtle.Turtle()
        alex.shape('pion')
        alex.penup()
        alex.pencolor('red')
        alex.fillcolor('red')
        alex.backward(55) # avancer de 50 pixels
        alex.left(90)    # tourner de 90° en sens anti-horaire
        alex.backward(280) # avancer de 30 pixels

        robot = turtle.Turtle()
        robot.shape('pion')
        robot.penup()
        robot.pencolor('green')
        robot.fillcolor('green')
        robot.backward(55) # avancer de 50 pixels
        robot.left(90)    # tourner de 90° en sens anti-horaire
        robot.forward(290) # avancer de 30 pixels

        x = (5 - self.joueur1["pos"][0])*68 - 5
        y = (self.joueur1["pos"][1] - 1)*68 + 10
        alex.forward(y)
        alex.left(90)
        alex.forward(x)

        x = (5 - self.joueur2["pos"][0])*68 - 5
        y = (9 - self.joueur2["pos"][1])*68 +16
        robot.backward(y)
        robot.right(90)
        robot.backward(x)

        # On place ce place à l'origine pour le mur

        mure = turtle.Turtle()
        mure.shape('mur')
        mure.penup()
        mure.pencolor('blue')
        mure.fillcolor('blue')
        mure.backward(370)
        mure.right(90)
        mure.forward(300)
        mure.left(90)

        for liste in self.verticaux:
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
        
        mure.right(90)

        for liste in self.horizontaux:
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
        
        mure.fillcolor('black')
        mure.pencolor('black')
        mure.left(90)
        mure.forward(10)
        mure.right(90)
        mure.backward(10)
