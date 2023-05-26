class Parent():
    def __init__(self, nom):
        self.nom = nom


class Enfant1(Parent):
    def heritage(self):
        print(F"{enfant1.nom} a reçu {heritage * 0.75} €")

class Enfant2(Parent):
    def heritage(self):
        print(F"{enfant2.nom} a reçu {heritage * 0.25} €")

        


heritage = 50000
enfant1 = Enfant1("Ryad")
enfant2 = Enfant2("Sefa")
enfant1.heritage()
enfant2.heritage()