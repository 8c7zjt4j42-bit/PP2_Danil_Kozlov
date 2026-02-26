from datetime import datetime, timedelta, timezone

def parse(s):
    date, utc = s.split()
    sign = 1 if utc[3] == '+' else -1
    h, m = map(int, utc[4:].split(':'))
    offset = timezone(sign * timedelta(hours=h, minutes=m))
    return datetime.fromisoformat(date).replace(tzinfo=offset)

a = parse(input())
b = parse(input())

diff = abs((a.astimezone(timezone.utc) - b.astimezone(timezone.utc)).total_seconds())
print(int(diff // 86400))