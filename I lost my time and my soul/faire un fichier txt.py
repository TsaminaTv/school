import os
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "animaux.txt")

with open(file_path, "w") as file:
    file.write("Cheval\nMouton\nSinge\nTigre\n")

with open(file_path, "a") as file:
    file.write("Les animaux de la forêt")
    