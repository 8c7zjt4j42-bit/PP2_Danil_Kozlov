class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, university):
        super().__init__(name)
        self.university = university

s = Student("Danil", "KBTU")
print(s.name, "studies at", s.university)