import time


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


appHeaderColor = Style.DARKCYAN
backgroundColor = Style.CYAN
headerColor = Style.RED
questionColor = Style.BLUE
correctColor = Style.GREEN
errorColor = Style.RED
goodbyeColor = Style.YELLOW

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

class Professeur:
    def __init__(self, nom):
        self.nom = nom

    def creer_qcm(self):
        numero_qcm = int(input("Numéro du QCM : "))
        nombre_questions = int(input("Nombre de questions : "))
        duree = int(input("Durée du QCM en minutes : "))

        qcm = QCM(numero_qcm, nombre_questions, duree)

        for i in range(nombre_questions):
            question = input(f"Question {i + 1} : ")
            reponses = []
            for j in range(4):
                reponse = input(f"Réponse {j + 1} : ")
                reponses.append(reponse)
            reponse_correcte = int(input("Numéro de la réponse correcte : "))
            qcm.ajouter_question(question, reponses, reponse_correcte)

        qcm.enregistrer_qcm()
    
class GestionExamens:
    def __init__(self):
        self.username = ""
        self.password = ""


    def mainMenu(self):
        print(Style.BOLD + appHeaderColor + "\nAPPLICATION DE GESTION DE QCM" + Style.END)
        print(Style.CYAN + "*****************************")
        print(Style.BOLD + headerColor + "MENU PRINCIPAL" + Style.END)
        print(backgroundColor + "*****************************")
        print("1. Mode PROFESSEUR")
        print("2. Mode ELEVE")
        print("q. Quitter")

        while True:
            try:    
                userInput = input("Entrez votre choix (1/2/q)\n[Ou entrez 'q' pour quitter] : " + Style.WHITE)

                if userInput == "1":
                    self.checkAccount("PROF")
                elif userInput == "2":
                    self.checkAccount("ELEVE")
                elif userInput == "q":
                    print(goodbyeColor + "Au revoir!" + Style)
                    exit()
                else:
                    print(errorColor + "\nChoix invalide\n" + backgroundColor)
                    time.sleep(1)
                    self.mainMenu()
            except ValueError:
                print("ERROR choix invalide")


    def checkAccount(self, user):
        answer = input(backgroundColor + "Do you have an account? (y/n) : " + Style.WHITE)
        while True:
            if answer == "y":
                if user == "PROF" and self.login() == "PROF":
                    self.teacherMode()
                elif user == "ELEVE" and self.login() == "ELEVE":
                    self.studentMode()
                else:
                    print(Fore.MAGENTA + "You dont have permission to access this mode\n" + backgroundColor)
                    time.sleep(1)
                    self.mainMenu()
                break
            elif answer == "n":
                self.register(user)
                break
            else:
                answer = input(errorColor + "Please enter a valid answer (y/n) : " + Style.WHITE)


    def register(self, whoRegister):
        username = input(backgroundColor + "Username: " + Style.WHITE).lower()
        password = input(backgroundColor + "Password: " + Style.WHITE).lower()
        confirm_password = input(backgroundColor + "Confirm password: " + Style.WHITE).lower()
        if password == confirm_password:
            self.username = username
            self.password = password
        else:
            print(Fore.MAGENTA + "Passwords do not match\n" + Style)
            time.sleep(1)
            self.mainMenu()

        try:
            with open(file="accounts.txt", mode="r") as file:
                accounts = file.readlines()
                for account in accounts:
                    account = account.strip().split("|")
                    existingUsername = account[1].split(":")[0]
                    if existingUsername == self.username:
                        print(errorColor + "Username already exists" + backgroundColor)
                        time.sleep(1)
                        self.mainMenu()

            with open(file="accounts.txt", mode="a") as file:
                file.write(f"{whoRegister}|{username}:{password}\n")
            print(correctColor + "Registered successfully!" + backgroundColor)
            time.sleep(1)
            self.mainMenu()
        except FileNotFoundError:
            print("No accounts file found")


    def login(self):
        username = input(backgroundColor + "Username: " + Style.WHITE).lower()
        password = input(backgroundColor + "Password: " + Style.WHITE).lower()
        self.username = username
        self.password = password

        try:
            with open(file="accounts.txt", mode="r") as file:
                accounts = file.readlines()
        except FileNotFoundError:
            print(backgroundColor + "No accounts file found")

        for account in accounts:
            account = account.strip().split("|")
            role = account[0]
            account = account[1].split(":")
            if self.username == account[0] and self.password == account[1]:
                print(correctColor + "Login successful" + backgroundColor)
                return role


    def teacherMode(self):   
        while True:
            try:
                print("*****************************")
                print(Style.BOLD + headerColor + "MODE PROFESSEUR" + Style.END + backgroundColor)
                print("*****************************")
                print("1. Créer un QCM")
                print("2. Créer un compt pour un élève")
                print("3. Consulter les résultats d'un élève")
                print("q. Quitter le mode PROFESSEUR")
                userInput = input("Entrez votre choix (1/2/3/4/q)\n[Ou entrez 'q' pour quitter] : " + Style.WHITE)

                if userInput == "1":
                   mode_professeur()
                elif userInput == "2":
                    print(backgroundColor + "\nCréer un compte pour un élève\n")
                    # self.createStudentAccount()
                elif userInput == "3":
                    print(backgroundColor + "\nConsulter les résultats d'un élève\n")
                    # self.showStudentResults()
                elif userInput == "q":
                    print(errorColor + "Quitter le mode PROFESSEUR\n")
                    time.sleep(1)
                    self.mainMenu()
                    
                else:
                    print(errorColor + "\nChoix invalide\n" + backgroundColor)
                    time.sleep(1)
                    self.mainMenu()
            except ValueError:
                print("ERROR choix invalide")

    
    def studentMode(self):
        while True:
            try:
                print("*****************************")
                print(Style.BOLD + headerColor + "MODE ELEVE" + Style.END + backgroundColor)
                print("*****************************")
                print("1. Passer un QCM")
                print("q. Quitter le mode ELEVE")
                userInput = input("Entrez votre choix (1/q)\n[Ou entrez 'q' pour quitter] : " + Style.WHITE)

                if userInput == "1":
                    print(backgroundColor + "Passer un QCM\n")
                    self.takeQuiz()
                elif userInput == "q":
                    print(errorColor + "Quitter le mode ELEVE\n" + backgroundColor)
                    time.sleep(1)
                    self.mainMenu()
                else:
                    print(errorColor + "\nChoix invalide\n" + backgroundColor)
                    time.sleep(1)
                    self.mainMenu()
            except ValueError:
                print("Choix invalide")
        
    
    def takeQuiz(self):
        with open('qcm.txt', "r") as file:
            lines = file.readlines()

        questions = []
        answers = []
        correct_answers = []

        i = 0
        while i < len(lines):
            if lines[i].startswith("q:"):
                question = lines[i].replace("q:", "").strip()
                questions.append(question)
                i += 1
                answer_choices = []
                while not lines[i].startswith("Correct:"):
                    answer = lines[i].strip()
                    answer_choices.append(answer)
                    i += 1
                answers.append(answer_choices)
                correct_answer = lines[i].replace("Correct:", "").strip()
                correct_answers.append(int(correct_answer))
            i += 1

        for question in range(len(questions)):
            print(questionColor + f"Question: {questions[question]}" + questionColor)
            print("\n".join(answers[question]))
            print()
            # print(f"Correct Answer: {correct_answers[question]}" + Style)

            userInput = int(input(backgroundColor + "Enter your answer: " + Style.WHITE))
            if userInput == correct_answers[question]:
                print(correctColor + "Correct!\n" + backgroundColor)
            else:
                print(errorColor + "Incorrect!\n" + backgroundColor)

            with open(f"{self.username}_results.txt", "a") as file:
                file.write(f"Question: {questions[question]}\n")
                file.write("Answers:\n")
                file.write("\n".join(answers[question]) + "\n")
                file.write(f"Correct Answer: {correct_answers[question]}\n")
                file.write(f"User Answer: {userInput}\n")
                file.write("\n")


def main():
    user = GestionExamens()
    user.mainMenu()


if __name__ == "__main__":
    main()