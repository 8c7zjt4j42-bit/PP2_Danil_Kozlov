class Circle:
    def __init__(self, r):
        self.r = r

    def area(self):
        pi = 3.14159
        return pi * self.r * self.r

r = int(input().strip())
c = Circle(r)
print(f"{c.area():.2f}")
