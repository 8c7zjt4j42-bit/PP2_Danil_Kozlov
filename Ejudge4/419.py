import math
import sys

eps = 1e-12

def dist(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)

R = float(sys.stdin.readline())
x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

OA = math.hypot(x1, y1)
OB = math.hypot(x2, y2)
AB = dist(x1, y1, x2, y2)


dx = x2 - x1
dy = y2 - y1
den = dx*dx + dy*dy

if den < eps:
    ans = 0.0
else:
    
    t = -(x1*dx + y1*dy) / den
    if t <= 0.0:
        dmin = OA
    elif t >= 1.0:
        dmin = OB
    else:
        
        dmin = abs(x1*dy - y1*dx) / math.sqrt(den)

    if dmin >= R - 1e-12:
        ans = AB
    else:
        
        ta = math.sqrt(max(0.0, OA*OA - R*R))
        tb = math.sqrt(max(0.0, OB*OB - R*R))

        
        cos_phi = (x1*x2 + y1*y2) / (OA*OB)
        cos_phi = max(-1.0, min(1.0, cos_phi))
        phi = math.acos(cos_phi)

    
        alpha = math.acos(R / OA)
        beta  = math.acos(R / OB)

       
        arc1 = R * abs(phi - alpha - beta)
        arc2 = R * (2*math.pi - abs(phi - alpha - beta))
        arc = min(arc1, arc2)

        ans = ta + tb + arc

print(f"{ans:.10f}")