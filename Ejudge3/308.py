class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return None
        self.balance -= amount
        return self.balance

b, w = map(int, input().split())
acc = Account("owner", b)

res = acc.withdraw(w)
if res is None:
    print("Insufficient Funds")
else:
    print(res)
