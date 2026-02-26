import sys

class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)
        self.gpa = gpa

    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa:.1f}")



data = sys.stdin.read().strip().split()

name = data[0]
gpa = float(data[1])

student = Student(name, gpa)
student.display()