with open('animaux.txt', 'r') as f:
    liste = f.readlines()
    liste.sort(key=len)

print(f"Le mot le plus court est: {liste[0]}")
print(f"Le mot le plus long est: {liste[-1]}")