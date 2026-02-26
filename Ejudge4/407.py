class Reverse:
    def __init__(self, s):
        self.s = s
        self.i = len(s)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i == 0:
            raise StopIteration
        self.i -= 1
        return self.s[self.i]

s = input()
print("".join(Reverse(s)))