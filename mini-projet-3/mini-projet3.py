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

        # le timer commence
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
            elif answer == "n":
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
            username = input(backgroundColor + "Username: " + defaultColor).lower()
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
            with open(file="Accounts\\accounts.txt", mode="r", encoding='utf-8') as file:
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
            with open(file="Accounts\\accounts.txt", mode="a", encoding='utf-8') as file:
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
        username = input(backgroundColor + "Username: " + defaultColor).lower()
        password = input(backgroundColor + "Password: " + defaultColor).lower()
        #définition du nom et du MDP en variable
        self.username = username
        self.password = password

        try:
            #Ouverture du fichier de compte
            with open(file="Accounts\\accounts.txt", mode="r", encoding='utf-8') as file:
                #On lit tous les comptes
                accounts = file.readlines()
        except FileNotFoundError:
            print(backgroundColor + "Compte introuvable")

        for account in accounts:
            # Split the account into role and username:password
            account = account.strip().split("|")
            # Set the role to the first element of the account
            role = account[0]
            # Split the username:password into username and password
            account = account[1].split(":")
            # Check if the username and password match
            if self.username == account[0] and self.password == account[1]:
                return role


    def teacherMode(self):
        '''
        Print the teacher mode menu
        '''
        # Clear the screen
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
        Create a new quiz
        '''
        # Clear the screen
        print(Style.CLEAR, end='')
        # Ask for the quiz name, number of questions, number of answers and quiz duration
        quizQuestions = []
        quizName = input(backgroundColor + "Veuillez entrer le nom du QCM : " + defaultColor)
        quizQuestionsNumber = input(backgroundColor + "Veuillez entrer le nombre de questions du QCM : " + defaultColor)
        quizAnswersNumber = input(backgroundColor + "Veuillez entrer le nombre de réponses par question : " + defaultColor)
        quizDuration = input(backgroundColor + "Veuillez entrer la durée du QCM (en seconds) : " + defaultColor)

        for i in range(int(quizQuestionsNumber)):
            # Ask for the question and the answers
            question = input(backgroundColor + f"Veuillez entrer la question {i+1} : " + defaultColor)
            quizQuestions.append(f"q: {question}")
            for j in range(int(quizQuestionsNumber)):
                answer = input(backgroundColor + f"Veuillez entrer la réponse {j+1} : " + defaultColor)
                quizQuestions.append(f"{j + 1}) {answer}")
                # If it's the last answer, ask for the correct answer because thats how the format is
                if j == int(quizAnswersNumber) - 1:
                    quizCorrectAnswer = input(backgroundColor + "Veuillez entrer le numéro de la bonne réponse : " + defaultColor)
                    quizQuestions.append(f"Correct: {quizCorrectAnswer}\n")
        quizQuestions.append(f"Quiz duration: {quizDuration}")

        try:
            # Create the quiz file if it doesn't exist
            if not os.path.exists(f"QCM\\{quizName}.txt"):
                open(f"QCM\\{quizName}.txt", "w").close()
            # Open the quiz file and write the questions and answers that were entered before
            with open(file=f"QCM\\{quizName}.txt", mode="a", encoding='utf-8') as file:
                for i in range(len(quizQuestions)):
                    file.write(f"{quizQuestions[i]}\n")
            # Print a success message and clear the screen clear the screen and redirect to teacher mode
            print(correctColor + "Quiz created successfully!" + backgroundColor)
            time.sleep(1)
            print(Style.CLEAR, end="")
            self.teacherMode()
        except FileNotFoundError:
            print(errorColor + "No quizzes file found" + backgroundColor)


    def createStudentAccount(self):
        '''
        Create a new student account as a teacher
        '''
        print(Style.CLEAR, end='')
        self.register("ELEVE", "PROF")

    
    def showStudentResults(self):
        '''
        Show the results of a student
        '''
        print(Style.CLEAR, end='')

        # ------ SELECT STUDENT FOLDER ------
        # Create a dictionary for the student folders
        studentFolders = {}
        count = 1

        # Check if a folder that ends with _QCM exists, if no folders that end with _QCM exist, print an error message and redirect to the teacher mode
        if len([folder for folder in os.listdir() if folder.endswith("_QCM")]) == 0:
            print(errorColor + "No student folders found" + backgroundColor)
            time.sleep(1.5)
            print(Style.CLEAR, end="")
            self.teacherMode()
        for folder in os.listdir():
            if folder.endswith("_QCM"):
                print(f"{count}) {folder}")
                # Add the folder to the students dictionary
                studentFolders[str(len(studentFolders) + 1)] = folder
                count += 1

        while True:
            try:
                # Ask user to choose a quiz
                studentFolderNumber = int(input(backgroundColor + f"Veuillez entrer un numéro valide ({', '.join(studentFolders.keys())}) : " + defaultColor))
                # Convert to string
                studentFolderNumber = str(studentFolderNumber)
                # Check if choice is valid
                if studentFolderNumber in studentFolders.keys():
                    print("You selected", studentFolders[studentFolderNumber])
                    # Set selected quiz
                    selectedStudentFolder = studentFolders[studentFolderNumber]
                    break
                else:
                    print(errorColor + "Invalid choice" + backgroundColor)
            except ValueError:
                print(errorColor + "Invalid choice" + backgroundColor)

        # ------ SELECT STUDENT FILE ------
        # Create a dictionary for the student files
        studentFiles = {}
        count2 = 1
        for file in os.listdir(selectedStudentFolder):
            print(f"{count2}) {file}")
            studentFiles[str(count2)] = file
            count2 += 1

        while True:
            try:
                # Ask user to choose a quiz
                studentFileNumber = int(input(backgroundColor + f"Veuillez entrer un numéro valide ({', '.join(studentFiles.keys())}) : " + defaultColor))
                # Convert to string
                studentFileNumber = str(studentFileNumber)
                # Check if choice is valid
                if studentFileNumber in studentFiles.keys():
                    print("You selected", studentFiles[studentFileNumber])
                    # Set selected quiz
                    selectedStudentFile = studentFiles[studentFileNumber]
                    break
                else:
                    print(errorColor + "Invalid choice" + backgroundColor)
            except ValueError:
                print(errorColor + "Invalid choice" + backgroundColor)

        # ------ SHOW STUDENT RESULTS ------
        # Clear the screen
        print(Style.CLEAR, end='')
        
        # Open the student file and print the results
        with open(f"{selectedStudentFolder}\\{selectedStudentFile}", "r", encoding='utf-8') as file:
            print(file.read())

        self.ActionForm({
            '1': ("Do you want to continue?", lambda: self.showStudentResults()),
            '2': ("Main Menu", lambda: (print(Style.CLEAR, end=''), self.mainMenu())),
        })

    
    def studentMode(self):
        '''
        Print the student mode menu
        '''
        # Clear the screen
        print(Style.CLEAR, end='')
        print(correctColor + "Login successful" + backgroundColor)
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
        Take a quiz
        '''
        # Clear the screen
        print(Style.CLEAR, end='')

        # Create empty lists for questions, answers and correct answers
        questions = []
        answers = []
        correct_answers = []
        qcmFiles = {}  # Create a dictionary for the quizzes that exist in a folder
        quizDuration = 0
        grade = 0

        # Create folder for student
        self.folderName = f"{self.username}_QCM"
        # Check if folder exists
        if not os.path.exists(self.folderName):
            os.mkdir(self.folderName)

        # Check if there are any quizzes
        print(backgroundColor + "Liste des QCM disponibles : " + defaultColor)

        # Check if the user has already done the quiz, if yes, remove it from their quizzes list
        count = 1
        for i, file in enumerate(os.listdir("QCM")):
            if f"{self.username}_{file}" not in os.listdir(self.folderName):
                print(f"{count}) {file}")
                qcmFiles[str(count)] = file.split(".")[0]
                count += 1

        while True:
            try:
                # Ask user to choose a quiz
                qcmNumber = int(input(backgroundColor + f"Veuillez entrer un numéro valide ({', '.join(qcmFiles.keys())}) : " + defaultColor))
                # Convert to string
                qcmNumber = str(qcmNumber)
                # Check if choice is valid
                if qcmNumber in qcmFiles.keys():
                    print(correctColor + "You selected", qcmFiles[qcmNumber] + defaultColor)
                    # Set selected quiz
                    selectedQCM = qcmFiles[qcmNumber]
                    break
                else:
                    print(errorColor + "Invalid choice" + backgroundColor)
            except ValueError:
                print(errorColor + "Invalid choice" + backgroundColor)
                
        # Clear the screen
        time.sleep(1)
        print(Style.CLEAR, end='')

        # ------ READ QUIZ FILE ------
        # Open selected quiz
        with open(f'QCM\\{selectedQCM}.txt', "r", encoding='utf-8') as file:
            # Read all lines
            lines = file.readlines()

        i = 0
        while i < len(lines):
            # Check if line starts with q:
            if lines[i].startswith("q:"):
                # Get question and add it to questions list
                question = lines[i].replace("q:", "").strip()
                questions.append(question)
                i += 1
                answer_choices = []

                # Get answers and add them to answers list if the line doesn't start with Correct:
                while not lines[i].startswith("Correct:"):
                    answer = lines[i].strip()
                    answer_choices.append(answer)
                    i += 1
                answers.append(answer_choices)
                # Extract correct answer without "Correct:" and add it to correct_answers list
                correct_answer = lines[i].replace("Correct:", "").strip()
                # Convert to int and add to correct_answers list
                correct_answers.append(int(correct_answer))

            # Check if line starts with "Quiz duration:"
            if lines[i].startswith("Quiz duration:"):
                # Extract the duration value
                quizDuration = int(lines[i].replace("Quiz duration:", "").strip())
            i += 1

        # ------ START TIMER, SHOW QUIZ QUESTIONS AND WRITE ANSWERS TO STUDENT FILE ------
        # Start the countdown
        self.CountDown(quizDuration)
        # Start the timer
        stopThread = False
        timerThread = threading.Thread(target=self.Timer, args=(quizDuration,))
        timerThread.start()

        while myTimer > 0:
            for question in range(len(questions)):
                # Print question
                print(questionColor + f"Question: {questions[question]}" + questionColor)
                # Print answers
                print("\n".join(answers[question]))
                # Ask user the question answer with try except
                while True:
                    try:
                        userInput = int(input(backgroundColor + "Enter your answer: " + defaultColor))
                        break
                    except ValueError:
                        print(errorColor + "Invalid choice" + backgroundColor)

                # Check if answer is correct
                if userInput == correct_answers[question]:
                    # If correct, add 1 to grade
                    print(correctColor + "Correct!\n" + backgroundColor)
                    grade += 1
                else:
                    # If incorrect, print correct answer
                    print(errorColor + "Incorrect!\n" + backgroundColor)

                # If file doesn't exist, create it
                if not os.path.exists(f"{self.folderName}\\{self.username}_{selectedQCM}.txt"):
                    open(f"{self.folderName}\\{self.username}_{selectedQCM}.txt", "w").close()

                # Open file and write the questions, answers, correct answer and user answer
                with open(f"{self.folderName}\\{self.username}_{selectedQCM}.txt", "a", encoding='utf-8') as file:
                    file.write(f"Question: {questions[question]}\n")
                    file.write("Answers:\n")
                    file.write("\n".join(answers[question]) + "\n")
                    file.write(f"Correct Answer: {correct_answers[question]}\n")
                    file.write(f"User Answer: {userInput}\n")
                    file.write("\n")
                
                if myTimer <= 0:
                    break
            # If done with all questions stop the timer thread and break
            break

        # End of quiz, grade the student
        with open(f"{self.folderName}\\{self.username}_{selectedQCM}.txt", "a", encoding='utf-8') as file:
            file.write(f"Student grade: {grade}/{len(questions)}\n")
            file.write("--------------------------------------------------\n")
        
        # Clear the screen
        time.sleep(1)
        print(Style.CLEAR, end='')
        
        # Print results
        print(correctColor + "Quiz completed!" + Style.END)
        if grade == len(questions):
            print(correctColor + f"Congratulations! You aced the test! ({grade}/{len(questions)})")
        elif grade >= len(questions) / 2:
            print(correctColor + f"Good job! You got {grade}/{len(questions)}" + backgroundColor)
        else:
            print(errorColor + f"SOOO BAAAAAD HAHAHA. You got {grade}/{len(questions)}" + Style.END)
        time.sleep(2)
        self.studentMode()

def main():
    print(Style.CLEAR, end='') # Clear the screen
    user = GestionExamens()
    user.mainMenu()


if __name__ == "__main__":
    main()
