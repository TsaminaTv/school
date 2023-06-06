import os
import time
import threading



class Style:
    WHITE = '\033[97m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    CLEAR = '\033c'
    REMOVECURSOR = '\033[?25l'
    SHOWCURSOR = '\033[?25h'


defaultColor = Style.WHITE
appHeaderColor = Style.DARKCYAN
backgroundColor = Style.CYAN
headerColor = Style.YELLOW
questionColor = Style.BLUE
correctColor = Style.GREEN
errorColor = Style.RED
goodbyeColor = Style.YELLOW


class GestionExamens:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.folderName = ""
    

    def Quit(self):
        '''
        Permet de quitter l'application
        '''
        print(Style.CLEAR)
        print(Style.CLEAR + goodbyeColor + "Au revoir!" + defaultColor)
        exit()

    
    def Timer(self, timerDuration):
        global myTimer
        myTimer = timerDuration

        # Start the timer
        for i in range(myTimer):
            myTimer -= 1
            time.sleep(1)
    print(errorColor + "\nTemps écoulé !  Entrez votre dernière réponse (si la réponse est déjà écrite, appuyez sur entrer): " + defaultColor)

    
    def CountDown(self, duration):
        print(errorColor + f"Vous avez {duration} seconds pour répondre à chaque question !" + defaultColor)

        # On affiche un décompte
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)


    def ActionForm(self, actions):
        '''
            Afficher un menu avec les actions à effectuer
        '''
        while True:
            for key in actions:
                # Afficher l'action 
                print(f"{key}: {actions[key][0]}")
            # Demander le choix de l'utilisateur
            choice = input(backgroundColor + f"Entrez votre choix ({', '.join(actions.keys())}) : " + defaultColor).lower()
            # On vérifie que le choix de l'utilisateur est un choix possible
            if choice in actions:
                # Exécution du choix 
                actions[choice][1]()
                return choice
            else:
                print(errorColor + "Choix invalide" + backgroundColor)


    def mainMenu(self):
        '''
        Affichage du menu principal 
        '''
        print(Style.BOLD + appHeaderColor + "APPLICATION DE GESTION DE QCM" + Style.END)
        print(backgroundColor + "*****************************")
        print(Style.BOLD + headerColor + "MENU PRINCIPAL" + Style.END)
        print(backgroundColor + "*****************************")

        self.ActionForm({
            '1': ("Mode PROFESSEUR", lambda: self.checkAccount("PROF")),
            '2': ("Mode ELEVE", lambda: self.checkAccount("ELEVE")),
            'q': ("Quitter", lambda: self.Quit())
            })


    def checkAccount(self, user):
        '''
        Vérification si l'utilisateur a déjà un compte
        Vérification si l'utilisateur est étudiant ou prof et afficher le bon menu
        '''
        answer = input(backgroundColor + "Avez vous un compte? (oui/non) : " + defaultColor)
        while True:
            # Verification si l'utilisateur a un compte
            if answer == "oui":
                # Si l'utilisateur a un compte, verifier si c'est un prof ou un élève
                if user == "PROF" and self.login() == "PROF":
                    self.teacherMode()
                elif user == "ELEVE" and self.login() == "ELEVE":
                    self.studentMode()
                else:
                    #Si l'utilisateur n'est pas un prof ou un élève, afficher un message d'erreur et rédirection au menu principal
                    print(Style.CLEAR + Style.PURPLE + "Vous n'avez pas la permission\n" + backgroundColor)
                    time.sleep(1)
                    print(Style.CLEAR, end="")
                    self.mainMenu()
                break
            elif answer == "non":
                #Si l'utilisateur n'a pas de compte, en créer un 
                self.register(user, user)
                break
            else:
                answer = input(errorColor + "Veuillez entrez une réponse valide (oui/non) : " + defaultColor)


    def register(self, whoRegister, whoCreatedAccount):
        '''
        Fonction de création de compte
        '''
        while True:
            # Demander un nom d'utilisateur et un mot de passe
            username = input(backgroundColor + "Nom : " + defaultColor).lower()
            password = input(backgroundColor + "mot de passe: " + defaultColor).lower()
            confirmPassword = input(backgroundColor + "Confirmez votre MDP: " + defaultColor).lower()
            #Vérification si le MDP et le nom d'utilisateur font au moins 2 caractères et si les MDP correspondent
            if len(username) < 2 or len(password) < 2 or password != confirmPassword:
                print(errorColor + "Le nom d'utilisateur et le MDP doivent faire au moins 2 caractères et les MDP doivent correspondrent" + backgroundColor)
            else:
                #On défini le nom d'utilisateur et le mdp sur des variable de class
                self.username = username
                self.password = password
                break
        try:
            # ouvrir le fichier de compte
            with open(file="Accounts\\eleves.txt", mode="r", encoding='utf-8') as file:
                #On lit les comptes
                accounts = file.readlines()
                for account in accounts:
                    #Séparer le compte du MDP 
                    account = account.strip().split("|")
                    #Séparer le compte du MDP
                    existingUsername = account[1].split(":")[0]
                    #Vérification si le nom d'utilisateur existe déjà
                    if existingUsername == self.username:
                        print(errorColor + "Le nom d'utilisateur existe déjà" + backgroundColor)
                        self.mainMenu()

            #Si le nom d'utilisateur n'existe pas, sauvegarder le compte
            with open(file="Accounts\\eleves.txt", mode="a", encoding='utf-8') as file:
                file.write(f"{whoRegister}|{username}:{password}\n")

            #Imprimer un message de succès et nettoyer l'écran
            print(correctColor + "Register successful!" + backgroundColor)
            time.sleep(1.5)
            print(Style.CLEAR, end="")

            #Si le compte est un compte prof, ouvrir le mode prof
            if whoCreatedAccount == "PROF":
                self.teacherMode()
            #Si le compte est un compte élève, ouvrir le mode élève
            else:
                self.mainMenu()
        except FileNotFoundError:
            print("Compte introuvable")


    def login(self):
        '''
        Connexion a un compte existant
        '''
        #Demande du nom d'utilisateur et MDP
        username = input(backgroundColor + "Nom: " + defaultColor).lower()
        password = input(backgroundColor + "Mot de Passe: " + defaultColor).lower()
        #définition du nom et du MDP en variable
        self.username = username
        self.password = password

        try:
            #Ouverture du fichier de compte
            with open(file="Accounts\\eleves.txt", mode="r", encoding='utf-8') as file:
                #On lit tous les comptes
                accounts = file.readlines()
        except FileNotFoundError:
            print(backgroundColor + "Compte introuvable")

        for account in accounts:
            # séparation du compte dans 2 rôles séparé nom d'utilisateur et mdp 
            account = account.strip().split("|")
            # définition du rôle sur le premier éléments
            role = account[0]
            # séparation du compte dans 2 rôles séparé nom d'utilisateur et mdp 
            account = account[1].split(":")
            # Check si le nom et le MDP correspondent
            if self.username == account[0] and self.password == account[1]:
                return role


    def teacherMode(self):
        '''
        Print the teacher mode menu
        '''
        # effacer l'ecran
        print(Style.CLEAR, end='')
        print(correctColor + "Login successful" + backgroundColor)
        print(backgroundColor + "*****************************")
        print(Style.BOLD + headerColor + "MODE PROFESSEUR" + Style.END + backgroundColor)
        print("*****************************")
        # - - - - - ACTION FORM - - - - -
        self.ActionForm({
            '1': ('Créer un QCM', lambda: self.createQuiz()),
            '2': ('Créer un compte pour un élève', lambda: self.createStudentAccount()),
            '3': ("Consulter les résultats d'un élève", lambda: self.showStudentResults()),
            '4': ('Main Menu', lambda: (print(Style.CLEAR, end=''), self.mainMenu())),
            'q': ('Quitter', lambda: self.Quit())
            })


    def createQuiz(self):
        '''
        Création d'un nouveau quizz
        '''
        # effacer l'écran
        print(Style.CLEAR, end='')
        # Demander le nom du quiz, nombre de question, nombre de réponse et la durée
        quizQuestions = []
        quizName = input(backgroundColor + "Veuillez entrer le nom du QCM : " + defaultColor)
        quizQuestionsNumber = input(backgroundColor + "Veuillez entrer le nombre de questions du QCM : " + defaultColor)
        quizAnswersNumber = input(backgroundColor + "Veuillez entrer le nombre de réponses par question : " + defaultColor)
        quizDuration = input(backgroundColor + "Veuillez entrer la durée du QCM (en seconds) : " + defaultColor)

        for i in range(int(quizQuestionsNumber)):
            # Demande des questions et réponses
            question = input(backgroundColor + f"Veuillez entrer la question {i+1} : " + defaultColor)
            quizQuestions.append(f"q: {question}")
            for j in range(int(quizQuestionsNumber)):
                answer = input(backgroundColor + f"Veuillez entrer la réponse {j+1} : " + defaultColor)
                quizQuestions.append(f"{j + 1}) {answer}")
                # Si c'est la dernière question, demander la réponse correct
                if j == int(quizAnswersNumber) - 1:
                    quizCorrectAnswer = input(backgroundColor + "Veuillez entrer le numéro de la bonne réponse : " + defaultColor)
                    quizQuestions.append(f"Correct: {quizCorrectAnswer}\n")
        quizQuestions.append(f"Quiz duration: {quizDuration}")

        try:
            # Création du fichier de quiz s'il n'existe pas
            if not os.path.exists(f"QCM\\{quizName}.txt"):
                open(f"QCM\\{quizName}.txt", "w").close()
            # ouverture du fichier du quiz et y écrire les questions et réponses entrer avant
            with open(file=f"QCM\\{quizName}.txt", mode="a", encoding='utf-8') as file:
                for i in range(len(quizQuestions)):
                    file.write(f"{quizQuestions[i]}\n")
            # Afficher un message de succès, effacer l'écran et aller en mode prof 
            print(correctColor + "Le quizz a bien été créé!" + backgroundColor)
            time.sleep(1)
            print(Style.CLEAR, end="")
            self.teacherMode()
        except FileNotFoundError:
            print(errorColor + "Fichier de quizz introuvable" + backgroundColor)


    def createStudentAccount(self):
        '''
        Creation d'un compte eleves en tant que prof
        '''
        print(Style.CLEAR, end='')
        self.register("ELEVE", "PROF")

    
    def showStudentResults(self):
        '''
         Afficher les résultat d'un étudiant
        '''
        print(Style.CLEAR, end='')

        # ------ Selection d'un dossier élève ------
        # creation d'un dictionnaire pour les eleves
        studentFolders = {}
        count = 1

        # Check si un fichier termine avec _QCM si non, afficher un message d'erreur et aller en mode prof
        if len([folder for folder in os.listdir() if folder.endswith("_QCM")]) == 0:
            print(errorColor + "No student folders found" + backgroundColor)
            time.sleep(1.5)
            print(Style.CLEAR, end="")
            self.teacherMode()
        for folder in os.listdir():
            if folder.endswith("_QCM"):
                print(f"{count}) {folder}")
                # Ajouter le dossier au dictionnaire eleve
                studentFolders[str(len(studentFolders) + 1)] = folder
                count += 1


        while True:
            try:
                # Demande de choix d'un quizz
                studentFolderNumber = int(input(backgroundColor + f"Veuillez entrer un numéro valide ({', '.join(studentFolders.keys())}) : " + defaultColor))
                # conversion en string
                studentFolderNumber = str(studentFolderNumber)
                # Check si le choix est valide
                if studentFolderNumber in studentFolders.keys():
                    print("Vous avez choisis", studentFolders[studentFolderNumber])
                    # Set selected quiz 
                    selectedStudentFolder = studentFolders[studentFolderNumber]
                    break
                else:
                    print(errorColor + "Choix invalide" + backgroundColor)
            except ValueError:
                print(errorColor + "Choix invalide" + backgroundColor)
        # ------ Selection d'un fichier eleve ------

        # création d'un dictionnaire pour les fichiers des élèves
        studentFiles = {}
        count2 = 1
        for file in os.listdir(selectedStudentFolder):
            print(f"{count2}) {file}")
            studentFiles[str(count2)] = file
            count2 += 1

        while True:
            try:
                # Demande de choix d'un quizz
                studentFileNumber = int(input(backgroundColor + f"Veuillez entrer un numéro valide ({', '.join(studentFiles.keys())}) : " + defaultColor))
                # conversion en string
                studentFileNumber = str(studentFileNumber)
                # Check si le choix est valide
                if studentFileNumber in studentFiles.keys():
                    print("Vous avez choisis", studentFiles[studentFileNumber])
                    # Set selected quiz
                    selectedStudentFile = studentFiles[studentFileNumber]
                    break
                else:
                    print(errorColor + "Choix invalide" + backgroundColor)
            except ValueError:
                print(errorColor + "Choix invalide" + backgroundColor)

        # ------ Affichage des résultats des élèves ------
        # effacer l'ecran
        print(Style.CLEAR, end='')
        
        # Ouvrir le fichier étudiant et afficher le résultat
        with open(f"{selectedStudentFolder}\\{selectedStudentFile}", "r", encoding='utf-8') as file:
            print(file.read())

        self.ActionForm({
            '1': ("Voulez vous continuer?", lambda: self.showStudentResults()),
            '2': ("Menu Principal", lambda: (print(Style.CLEAR, end=''), self.mainMenu())),
        })

    
    def studentMode(self):
        '''
        afficher le menu élève
        '''
        # effacer l'écran
        print(Style.CLEAR, end='')
        print(correctColor + "Connexion réussie" + backgroundColor)
        print(backgroundColor + "*****************************")
        print(Style.BOLD + headerColor + "MODE ELEVE" + Style.END + backgroundColor)
        print("*****************************")
        self.ActionForm({
            '1': ('Passer un QCM', lambda: self.takeQuiz()),
            "2": ("Main Menu", lambda: (print(Style.CLEAR, end=''), self.mainMenu())),
            'q': ('Quitter', lambda: self.Quit())
            })


    def takeQuiz(self):
        '''
        faire un quiz
        '''
        # effacer l'écran
        print(Style.CLEAR, end='')

        # creation de liste vide pour les question réponse et réponses correcte
        questions = []
        answers = []
        correct_answers = []
        qcmFiles = {}  # Creation d'un dictionnaire pour les quiz qui existent dans un dossier  
        quizDuration = 0
        grade = 0

        # création d'un fichier pour un étudiant
        self.folderName = f"{self.username}_QCM"
        # Check si le fichier existe déjà 
        if not os.path.exists(self.folderName):
            os.mkdir(self.folderName)

        # Check s'il y'a des quiz
        print(backgroundColor + "Liste des QCM disponibles : " + defaultColor)

        # Si l'élève a déjà fait le quiz, retirer le quiz de la liste
        count = 1
        for i, file in enumerate(os.listdir("QCM")):
            if f"{self.username}_{file}" not in os.listdir(self.folderName):
                print(f"{count}) {file}")
                qcmFiles[str(count)] = file.split(".")[0]
                count += 1

        while True:
            try:
                # demande de choix d'un quiz
                qcmNumber = int(input(backgroundColor + f"Veuillez entrer un numéro valide ({', '.join(qcmFiles.keys())}) : " + defaultColor))
                # conversion en string
                qcmNumber = str(qcmNumber)
                # Check si le choix est valide
                if qcmNumber in qcmFiles.keys():
                    print(correctColor + "Vous avez selectionné", qcmFiles[qcmNumber] + defaultColor)
                    # Set selected quiz
                    selectedQCM = qcmFiles[qcmNumber]
                    break
                else:
                    print(errorColor + "Choix invalide" + backgroundColor)
            except ValueError:
                print(errorColor + "Choix invalide" + backgroundColor)
                
        # effacer l'écran
        time.sleep(1)
        print(Style.CLEAR, end='')

        # ------ Lire le fichier quiz ------
        # ouvrir le quiz selectionner
        with open(f'QCM\\{selectedQCM}.txt', "r", encoding='utf-8') as file:
            # lire toutes les lignes
            lines = file.readlines()

        i = 0
        while i < len(lines):
            # check si la ligne commence avec q:
            if lines[i].startswith("q:"):
                # Ajouter les questions dans la liste
                question = lines[i].replace("q:", "").strip()
                questions.append(question)
                i += 1
                answer_choices = []

                # Obtenir les réponses et les ajouter a la liste des réponses, si la ligne ne commence pas avec correct 
                while not lines[i].startswith("Correct:"):
                    answer = lines[i].strip()
                    answer_choices.append(answer)
                    i += 1
                answers.append(answer_choices)
                # Extract correct answer without "Correct:" and add it to correct_answers list 
                correct_answer = lines[i].replace("Correct:", "").strip()
                # conversion en int et ajout dans correct_answers list
                correct_answers.append(int(correct_answer))

            # Check si la ligne commence avec "durée du quiz:" 
            if lines[i].startswith("Quiz duration:"):
                # extraire la durée 
                quizDuration = int(lines[i].replace("Quiz duration:", "").strip())
            i += 1

        # ------ début du timer, afficher les questions ------ 
        # début du décompte
        self.CountDown(quizDuration)
        # début du timer
        stopThread = False
        timerThread = threading.Thread(target=self.Timer, args=(quizDuration,))
        timerThread.start()

        while myTimer > 0:
            for question in range(len(questions)):
                # Print question
                print(questionColor + f"Question: {questions[question]}" + questionColor)
                # Print réponse
                print("\n".join(answers[question]))
                # demander à l'utilisateur la question et la réponse avec try expect
                while True:
                    try:
                        userInput = int(input(backgroundColor + "Entrez votre réponse " + defaultColor))
                        break
                    except ValueError:
                        print(errorColor + "Choix invalide" + backgroundColor)

                # Si la réponse est correct
                if userInput == correct_answers[question]:
                    # si correct ajouter 1 au grade
                    print(correctColor + "Correct!\n" + backgroundColor)
                    grade += 1
                else:
                    # Si incorrecte ; afficher incorrecte
                    print(errorColor + "Incorrect!\n" + backgroundColor)

                # Si le fichier n'existe pas, le créer
                if not os.path.exists(f"{self.folderName}\\{self.username}_{selectedQCM}.txt"):
                    open(f"{self.folderName}\\{self.username}_{selectedQCM}.txt", "w").close()

                # ouvrir le fichier, écrire les question, réponses et les réponse de l'utilisateur
                with open(f"{self.folderName}\\{self.username}_{selectedQCM}.txt", "a", encoding='utf-8') as file:
                    file.write(f"Question: {questions[question]}\n")
                    file.write("Answers:\n")
                    file.write("\n".join(answers[question]) + "\n")
                    file.write(f"Correct Answer: {correct_answers[question]}\n")
                    file.write(f"User Answer: {userInput}\n")
                    file.write("\n")
                
                if myTimer <= 0:
                    break
            #Si toutes les questions sont faites, arreter le timer 
            break

        # Fin du quiz, note de l'élève
        with open(f"{self.folderName}\\{self.username}_{selectedQCM}.txt", "a", encoding='utf-8') as file:
            file.write(f"Student grade: {grade}/{len(questions)}\n")
            file.write("--------------------------------------------------\n")
        
        # effacer l'écran
        time.sleep(1)
        print(Style.CLEAR, end='')
        
        # Print results
        print(correctColor + "Quiz Fini !" + Style.END)
        if grade == len(questions):
            print(correctColor + f"Bravo ! vous avez réussis le teste ({grade}/{len(questions)})") 
        elif grade >= len(questions) / 2:
            print(correctColor + f"Good job! votre note : {grade}/{len(questions)}" + backgroundColor)
        else:
            print(errorColor + f"Dommage,une prochaine fois. Votre note {grade}/{len(questions)}" + Style.END)
        time.sleep(2)
        self.studentMode()

def main():
    print(Style.CLEAR, end='') # effacer l'écran
    user = GestionExamens()
    user.mainMenu()


if __name__ == "__main__":
    main()
