from tabulate import tabulate
import tkinter as tk


class Joueur():
    def __init__(self):
        self.pseudo = ""
        self.personnage = []
        self.seed = ""
        self.game = 0
        self.gamePrise = 0
        self.gamePerdu = 0
        self.point = 0

    def setPseudo(self, pseudo):
        self.pseudo = pseudo

    def setSeed(self, seed):
        self.seed = seed

    def setPersonnage(self, personnage):
        self.personnage.append(personnage)

    def setGame(self,game):
        self.game = game

    def setGamePrise(self,gamePrise):
        self.gamePrise = gamePrise

    def setGamePerdu(self,gamePerdu):
        self.gamePerdu = gamePerdu

    def setPoint(self,point):
        self.point = point

    def getPseudo(self):
        return self.pseudo

    def getSeed(self):
        return self.seed

    def getPersonnage(self):
        return self.personnage

    def getGame(self):
        return self.game

    def getGamePrise(self):
        return self.gamePrise

    def getGamePerdu(self):
        return self.gamePerdu

    def getPoint(self):
        return self.point

class Match():
    def __init__(self):
        self.joueur1 = Joueur()
        self.joueur2 = Joueur()
        self.score = ""

    def setJoueur1(self, joueur1):
        self.joueur1 = joueur1

    def setJoueur2(self, joueur2):
        self.joueur2 = joueur2

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def ecrireMatch(self):
        fi = Fichier()
        fi.path = "games.txt"
        fi.mode = "a"
        fi.open()
        fi.inp.write(self.joueur1.getPseudo() + ";")
        print(self.joueur1.getPseudo())
        fi.inp.write(",".join(self.joueur1.getPersonnage()) + ";")
        print(",".join(self.joueur1.getPersonnage()))
        fi.inp.write(self.joueur2.getPseudo() + ";")
        print(self.joueur2.getPseudo())
        fi.inp.write(",".join(self.joueur2.getPersonnage()) + ";")
        print(",".join(self.joueur2.getPersonnage()) + ";")
        fi.inp.write(self.getScore())
        print(self.getScore())
        fi.inp.write("\n")
        fi.close()


class Fichier():
    def __init__(self):
        self.path = ""
        self.mode = ""

    def open(self):
        self.inp = open(self.path, self.mode)

    def close(self):
        self.inp.close()

    def lireCsv(self):
        data = []
        ligne = self.inp.readline()
        while ligne != "":
            data.append(ligne.replace("\n", "").split(";"))
            ligne = self.inp.readline()
        return data


class TableauResultat():
    def __init__(self):
        self.nb_joueurs = 0
        self.data = []
        self.tableau = []

    def nombreDeJoueur(self, joueurs):
        self.nb_joueurs = len(joueurs)
        self.tableau = [["0-0" for i in range(self.nb_joueurs)] for j in range(self.nb_joueurs)]

    def lireFichierResult(self):
        fi = Fichier()
        fi.path = "games.txt"
        fi.mode = "r"
        fi.open()
        self.data = fi.lireCsv()
        fi.close()

    def genererTableauResultats(self, joueurs):
        if self.data != "":
            for match in self.data:
                for joueur in joueurs:
                    score_joueur1 = match[-1].split("-")[0]
                    score_joueur2 = match[-1].split("-")[1]
                    if match[0] == joueur.getPseudo():
                        i = int(joueur.getSeed()) - 1
                    if match[2] == joueur.getPseudo():
                        j = int(joueur.getSeed()) - 1
                self.tableau[i][j] = match[-1]

                score_inverse = match[-1].split("-")
                score_inverse = score_inverse[-1] + "-" + score_inverse[0]
                self.tableau[j][i] = score_inverse
        else:
            print("Vous n'avez pas charger le fichier des résultats")




class Main():
    def __init__(self):
        self.liste_joueur = {}

    def creationJoueur(self):
        fi = Fichier()
        fi.path = "joueur.txt"
        fi.mode = "r"
        fi.open()
        data = fi.lireCsv()
        fi.close()
        for i in range(len(data)):
            new_joueur = Joueur()
            new_joueur.setPseudo(data[i][0])
            new_joueur.setSeed(data[i][1])
            self.liste_joueur[i + 1] = new_joueur

    def choixListe(self):
        print("1 - Saisir un nouveau match")
        print("2 - Génerer le tableau des scores")
        print("q - Quitter")

    def choix(self):
        self.choixListe()
        choix = input("Quel est votre choix : ")
        return choix

    def newMatch(self):
        joueurs = []
        liste_personnage = []
        for joueur in self.liste_joueur.values():
            soustab = []
            soustab.append(joueur.getSeed())
            soustab.append(joueur.getPseudo())
            joueurs.append(soustab)
        print(tabulate(joueurs, headers=["Choix", "Pseudo"]))
        joueur1 = int(input("Joueur 1 : "))
        while joueur1 not in self.liste_joueur.keys():
            joueur1 = input("Votre choix n'était pas dans la liste veuillez choisir parmis la liste  : ")
        joueur2 = int(input("Joueur 2 : "))
        while joueur2 not in self.liste_joueur.keys():
            joueur2 = input("Votre choix n'était pas dans la liste veuillez choisir parmis la liste  : ")
        match = Match()
        match.setJoueur1(self.liste_joueur.get(joueur1))
        match.setJoueur2(self.liste_joueur.get(joueur2))
        score = input("Quel est le score du match : ")
        match.setScore(score)
        personnage1 = input("Quel personnage a joué " + match.joueur1.getPseudo() + " : ")
        if "," in personnage1:
            liste_personnage = personnage1.split(",")
        else:
            liste_personnage.append(personnage1)
        for personnage in liste_personnage:
            match.joueur1.setPersonnage(personnage)
        liste_personnage = []
        personnage2 = input("Quel personnage a joué " + match.joueur2.getPseudo() + " : ")
        if "," in personnage2:
            liste_personnage = personnage2.split(",")
        else:
            liste_personnage.append(personnage2)
        for personnage in liste_personnage:
            match.joueur2.setPersonnage(personnage)
        match.ecrireMatch()
        self.liste_joueur.get(joueur1).personnage = []
        self.liste_joueur.get(joueur2).personnage = []


    def genererCSV(self):
        tab = TableauResultat()
        tab.nombreDeJoueur(self.liste_joueur.values())
        tab.lireFichierResult()
        tab.genererTableauResultats(self.liste_joueur.values())
        i = 0
        while i < len(tab.tableau):
            nom_joueur = self.liste_joueur[i + 1].getPseudo()
            tab.tableau[i].insert(0, nom_joueur)
            i += 1
        fo = open("results.csv", "a")
        fo.write(";")
        for joueur in self.liste_joueur.values():
            fo.write(joueur.getPseudo() + ";")
        fo.write("\n")
        for match in tab.tableau:
            for score in match:
                fo.write(score + ";")
            fo.write("\n")


    def aiguillage(self, choix):
        if choix == "1":
            self.newMatch()
        if choix == "2":
            self.genererCSV()

    def mainloop(self):
        self.creationJoueur()
        choix = self.choix()
        while choix != "q":
            self.aiguillage(choix)
            choix = self.choix()


go = Main()
go.mainloop()
