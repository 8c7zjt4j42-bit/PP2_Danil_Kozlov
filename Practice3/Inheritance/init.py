class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

d = Dog("Rex", "Shepherd")
print(d.name)
print(d.breed)