class Person:
  species = "Human" 

  def __init__(self, name):
    self.name = name 

p1 = Person("Emil")
p2 = Person("Tobias")

print(p1.name)
print(p2.name)
print(p1.species)
print(p2.species)