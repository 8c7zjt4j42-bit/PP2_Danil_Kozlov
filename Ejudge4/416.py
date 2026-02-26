from datetime import datetime, timedelta, timezone

def parse(s):
    date, time, utc = s.split()
    sign = 1 if utc[3] == '+' else -1
    h, m = map(int, utc[4:].split(':'))
    offset = timezone(sign * timedelta(hours=h, minutes=m))
    return datetime.fromisoformat(date + "T" + time).replace(tzinfo=offset)

start = parse(input())
end = parse(input())

sec = int((end.astimezone(timezone.utc) - start.astimezone(timezone.utc)).total_seconds())
print(sec)