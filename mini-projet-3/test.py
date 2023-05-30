import time
import threading


def timer():
    global myTimer

    myTimer = 10

    for i in range(10):
        myTimer -= 1
        time.sleep(1)

    print("\nTime's up! Enter your last answer: ")


timerThread = threading.Thread(target=timer)
timerThread.start()

questions = ["What is the capital of France?", "What is the capital of Germany?", "What is the capital of Italy?"]
answers = [["1. Paris", "2. Rome", "3. Berlin"], ["1. Berlin", "2. Paris", "3. Rome"], ["1. Rome", "2. Berlin", "3. Paris"]]
grade = 0

while myTimer > 0:
    for question in range(len(questions)):
        # Print question
        print(f"Question: {questions[question]}")
        # Print answers
        print("\n".join(answers[question]))
        # Ask user the question answer with try except
        while True:
            try:
                userInput = int(input("Enter your answer: "))
                break
            except ValueError:
                print("Invalid choice")

        # Check if answer is correct
        if userInput == 1:
            # If correct, add 1 to grade
            print("Correct!\n")
            grade += 1
        else:
            # If incorrect, print correct answer
            print("Incorrect!\n")
        
        if myTimer <= 0:
            break
    
# Print final grade
print(f"Your final grade is {grade}/{len(questions)}")