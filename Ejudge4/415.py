from datetime import datetime, timedelta, timezone
import math

def parse(line: str) -> datetime:
    date, utc = line.split()
    sign = 1 if utc[3] == '+' else -1
    h, m = map(int, utc[4:].split(':'))
    tz = timezone(sign * timedelta(hours=h, minutes=m))
    return datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=tz)

birth = parse(input().strip())
now = parse(input().strip())

m, d = birth.month, birth.day

def birthday_in_year(year: int) -> datetime:
    
    try:
        return datetime(year, m, d, tzinfo=birth.tzinfo)
    except ValueError:
        return datetime(year, 2, 28, tzinfo=birth.tzinfo)

now_utc = now.astimezone(timezone.utc)

year = now.year
while True:
    bd = birthday_in_year(year)
    bd_utc = bd.astimezone(timezone.utc)
    if bd_utc >= now_utc:   
        break
    year += 1

delta = (bd_utc - now_utc).total_seconds()

if delta == 0:
    print(0)
else:
    print(math.ceil(delta / 86400))