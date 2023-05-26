import os
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "ex3.txt")

y =  0
with open(file_path, 'r', encoding="UTF-8") as f:
    liste = f.readlines()
for x in liste:
    print(x)
    y += 1
    print(f"il y'a {y} lignes")
print(f"Il y'a {y} lignes au total")
    