class Animal():
    def __init__(self, nom):
        self.nom = nom


class Chien(Animal):
    def aboyer(self):
        print(F"{dog.nom} est un chien qui aboie")

dog = Chien("Doggo")

class Chat(Animal):
    def miauler(self):
        print(F"{cat.nom} est un chat qui miaule")

cat = Chat("Felix")

dog.aboyer()
cat.miauler()