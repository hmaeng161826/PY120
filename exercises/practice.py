class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def introduce(self):
        print(f'Hi, I am a {self.name} the {self.species}!')

class Owner:
    def __init__(self, name, pet):
        self.name = name
        self.pet = pet

    def introduce(self):
        print(f"I'm {self.name}, and this is my pet:")
        self.pet.introduce()

fluffy = Pet("Fluffy", "dog")
alice = Owner("Alice", fluffy)

alice.introduce()
