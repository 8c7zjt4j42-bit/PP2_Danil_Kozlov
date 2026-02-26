import math

R = float(input().strip())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1


seg_len = math.hypot(dx, dy)
if seg_len == 0.0:
   
    print(f"{0.0:.10f}")
    raise SystemExit


a = dx*dx + dy*dy
b = 2.0 * (x1*dx + y1*dy)
c = x1*x1 + y1*y1 - R*R


inside1 = (x1*x1 + y1*y1) <= R*R + 1e-12
inside2 = (x2*x2 + y2*y2) <= R*R + 1e-12
if inside1 and inside2:
    print(f"{seg_len:.10f}")
    raise SystemExit

disc = b*b - 4.0*a*c


if disc < 0.0:
    
    print(f"{0.0:.10f}")
    raise SystemExit

sqrt_disc = math.sqrt(max(0.0, disc))
t1 = (-b - sqrt_disc) / (2.0*a)
t2 = (-b + sqrt_disc) / (2.0*a)
if t1 > t2:
    t1, t2 = t2, t1


L = max(0.0, t1)
Rr = min(1.0, t2)

length_inside = 0.0
if Rr > L:
    length_inside = (Rr - L) * seg_len
else:
    
    mid = 0.5
    xm = x1 + mid*dx
    ym = y1 + mid*dy
    if (xm*xm + ym*ym) <= R*R + 1e-12:
        length_inside = seg_len

print(f"{length_inside:.10f}")