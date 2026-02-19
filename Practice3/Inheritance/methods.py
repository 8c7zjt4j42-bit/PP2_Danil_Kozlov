class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, university):
        super().__init__(name)
        self.university = university

    def introduce(self):
        print("Hi, my name is", self.name, "and I study at", self.university)

s = Student("Danil", "KBTU")
s.introduce()