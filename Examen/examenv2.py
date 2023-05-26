import datetime


class QCM:
    def __init__(self, numero_qcm, nombre_questions, duree):
        self.numero_qcm = numero_qcm
        self.nombre_questions = nombre_questions
        self.duree = duree
        self.questions = []

    def ajouter_question(self, question, reponses, reponse_correcte):
        self.questions.append((question, reponses, reponse_correcte))

    def enregistrer_qcm(self):
        nom_fichier = f"QCM{self.numero_qcm}_{datetime.date.today().year}.txt"
        with open(nom_fichier, "w") as fichier:
            fichier.write(f"Numéro du QCM : {self.numero_qcm}\n")
            fichier.write(f"Nombre de questions : {self.nombre_questions}\n")
            fichier.write(f"Durée : {self.duree} minutes\n")
            fichier.write("\n")
            for i, (question, reponses, reponse_correcte) in enumerate(self.questions, start=1):
                fichier.write(f"Question {i}: {question}\n")
                for j, reponse in enumerate(reponses, start=1):
                    fichier.write(f"   {j}. {reponse}\n")
                fichier.write(f"   -> Réponse correcte : {reponse_correcte}\n")
                fichier.write("\n")

    def charger_qcm(self, numero_qcm):
        nom_fichier = f"QCM{numero_qcm}_{datetime.date.today().year}.txt"
        with open(nom_fichier, "r") as fichier:
            lines = fichier.readlines()
            self.numero_qcm = int(lines[1].split(":")[1].strip())
            self.nombre_questions = int(lines[2].split(":")[1].strip())
            self.duree = int(lines[3].split(":")[1].strip())
            questions = lines[5:]

            self.questions = []
            i = 0
            while i < len(questions):
                question = questions[i].split(":")[1].strip()
                reponses = [questions[i + j].strip() for j in range(1, 5)]
                reponse_correcte = int(questions[i + 5].split(":")[1].strip())
                self.ajouter_question(question, reponses, reponse_correcte)
                i += 6


class Eleve:
    def __init__(self, nom, numero_inscription, annee_naissance):
        self.nom = nom
        self.numero_inscription = numero_inscription
        self.annee_naissance = annee_naissance

    def creer_compte(self):
        nom_fichier = f"{self.nom}_{self.numero_inscription}.txt"
        with open("eleves.txt", "a") as fichier:
            fichier.write(f"Nom : {self.nom}\n")
            fichier.write(f"Numéro d'inscription : {self.numero_inscription}\n")
            fichier.write(f"Année de naissance : {self.annee_naissance}\n")
            fichier.write("\n")
        with open(nom_fichier, "w") as fichier:
            pass

    def passer_test(self):
        qcms_non_effectues = self.obtenir_qcms_non_effectues()
        if len(qcms_non_effectues) == 0:
            print("Aucun QCM disponible.")
            return

        print("Liste des QCM disponibles :")
        for i, qcm in enumerate(qcms_non_effectues, start=1):
            print(f"{i}. QCM {qcm.numero_qcm} - Durée : {qcm.duree} minutes")

        choix = int(input("Sélectionnez un QCM : ")) - 1
        if choix < 0 or choix >= len(qcms_non_effectues):
            print("Choix invalide.")
            return

        qcm_selectionne = qcms_non_effectues[choix]
        qcm_selectionne.enregistrer_qcm()
        self.marquer_qcm_effectue(qcm_selectionne)

    def obtenir_qcms_non_effectues(self):
        qcms = []
        # Récupérer la liste des QCM disponibles depuis un fichier ou une autre source
        # et vérifier si l'élève a déjà effectué chaque QCM.
        # Ajouter les QCM non effectués à la liste `qcms`.
        return qcms

    def marquer_qcm_effectue(self, qcm):
        # Marquer le QCM comme étant effectué par l'élève dans un fichier ou une autre source
        pass


class Professeur:
    def __init__(self, nom):
        self.nom = nom

    def creer_qcm(self):
        numero_qcm = int(input("Numéro du QCM : "))
        nombre_questions = int(input("Nombre de questions : "))
        duree = int(input("Durée (en minutes) : "))

        qcm = QCM(numero_qcm, nombre_questions, duree)

        for i in range(nombre_questions):
            print(f"\nQuestion {i+1}")
            question = input("Enoncé de la question : ")

            reponses = []
            for j in range(4):
                reponse = input(f"Réponse {j+1} : ")
                reponses.append(reponse)

            reponse_correcte = int(input("Numéro de la réponse correcte : "))
            qcm.ajouter_question(question, reponses, reponse_correcte)

        qcm.enregistrer_qcm()

    def afficher_qcms(self):
        # Afficher la liste des QCM disponibles depuis un fichier ou une autre source
        pass


def menu_principal():
    choix = input("Choisissez un mode : (P)rofesseur, (E)léve, (Q)uitter\n").upper()
    if choix == "P":
        menu_professeur()
    elif choix == "E":
        menu_eleve()
    elif choix == "Q":
        print("Au revoir !")
    else:
        print("Choix invalide.")
        menu_principal()


def menu_professeur():
    print("\n=== Mode Professeur ===")
    professeur = Professeur(input("Nom du professeur : "))
    choix = input("Que souhaitez-vous faire ?\n"
                  "(C)réer un QCM\n"
                  "(A)fficher la liste des QCM\n"
                  "(R)etourner au menu principal\n").upper()
    if choix == "C":
        professeur.creer_qcm()
    elif choix == "A":
        professeur.afficher_qcms()
    elif choix == "R":
        menu_principal()
    else:
        print("Choix invalide.")
        menu_professeur()


def menu_eleve():
    print("\n=== Mode Élève ===")
    eleve = Eleve(input("Nom de l'élève : "),
                  input("Numéro d'inscription : "),
                  input("Année de naissance : "))
    choix = input("Que souhaitez-vous faire ?\n"
                  "(C)réer un compte\n"
                  "(P)asser un test\n"
                  "(R)etourner au menu principal\n").upper()
    if choix == "C":
        eleve.creer_compte()
    elif choix == "P":
        eleve.passer_test()
    elif choix == "R":
        menu_principal()
    else:
        print("Choix invalide.")
        menu_eleve()


menu_principal()
---------------------



class Eleve:
    def __init__(self, nom, numero_inscription, annee_naissance):
        self.nom = nom
        self.numero_inscription = numero_inscription
        self.annee_naissance = annee_naissance

    def creer_compte(self):
        # Créer un compte pour l'élève dans une base de données ou une autre source
        pass

    def passer_test(self):
        qcms_non_effectues = self.obtenir_qcms_non_effectues()
        if not qcms_non_effectues:
            print("Aucun QCM disponible.")
            return

        print("QCM disponibles :")
        for i, qcm in enumerate(qcms_non_effectues):
            print(f"{i+1}. QCM {qcm.numero_qcm} - Durée : {qcm.duree} minutes")

        choix = int(input("Sélectionnez un QCM : ")) - 1
        if choix < 0 or choix >= len(qcms_non_effectues):
            print("Choix invalide.")
            return

        qcm_selectionne = qcms_non_effectues[choix]
        qcm_selectionne.enregistrer_qcm()
        self.marquer_qcm_effectue(qcm_selectionne)

    def obtenir_qcms_non_effectues(self):
        qcms = []
        # Récupérer la liste des QCM disponibles depuis un fichier ou une autre source
        # et vérifier si l'élève a déjà effectué chaque QCM.
        # Ajouter les QCM non effectués à la liste `qcms`.
        return qcms

    def marquer_qcm_effectue(self, qcm):
        # Marquer le QCM comme étant effectué par l'élève dans un fichier ou une autre source
        pass


class Professeur:
    def __init__(self, nom):
        self.nom = nom

    def creer_qcm(self):
        numero_qcm = int(input("Numéro du QCM : "))
        nombre_questions = int(input("Nombre de questions : "))
        duree = int(input("Durée (en minutes) : "))

        qcm = QCM(numero_qcm, nombre_questions, duree)

        for i in range(nombre_questions):
            print(f"\nQuestion {i+1}")
            question = input("Enoncé de la question : ")

            reponses = []
            for j in range(4):
                reponse = input(f"Réponse {j+1} : ")
                reponses.append(reponse)

            reponse_correcte = int(input("Numéro de la réponse correcte : "))
            qcm.ajouter_question(question, reponses, reponse_correcte)

        qcm.enregistrer_qcm()

    def afficher_qcms(self):
        # Afficher la liste des QCM disponibles depuis un fichier ou une autre source
        pass


def menu_principal():
    print("\n=== MENU PRINCIPAL ===")
    print("(P)rofesseur")
    print("(E)léve")
    print("(Q)uitter")
    choix = input("Choisissez une option : ").upper()
    if choix == "P":
        menu_professeur()
    elif choix == "E":
        menu_eleve()
    elif choix == "Q":
        print("Au revoir !")
    else:
        print("Choix invalide.")
        menu_principal()


def menu_professeur():
    print("\n=== MENU PROFESSEUR ===")
    print("(C)réer un QCM")
    print("(A)fficher les QCM")
    print("(R)etourner au menu principal")
    choix = input("Choisissez une option : ").upper()
    if choix == "C":
        professeur.creer_qcm()
    elif choix == "A":
        professeur.afficher_qcms()
    elif choix == "R":
        menu_principal()
    else:
        print("Choix invalide.")
        menu_professeur()


def menu_eleve():
    print("\n=== MENU ELEVE ===")
    print("(C)réer un compte")
    print("(P)asser un test")
    print("(R)etourner au menu principal")
    choix = input("Choisissez une option : ").upper()
    if choix == "C":
        eleve.creer_compte()
    elif choix == "P":
        eleve.passer_test()
    elif choix == "R":
        menu_principal()
    else:
        print("Choix invalide.")
        menu_eleve()


professeur = Professeur("John Doe")
eleve = Eleve("Alice", "2021001", 2005)

menu_principal()
