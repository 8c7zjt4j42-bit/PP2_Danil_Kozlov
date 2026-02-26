from datetime import datetime

d1 = datetime(2024,1,1,0,0,0)
d2 = datetime(2024,1,2,0,0,0)

print((d2-d1).total_seconds())