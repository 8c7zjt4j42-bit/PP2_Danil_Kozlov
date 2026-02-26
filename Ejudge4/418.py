import sys

x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())


y2r = -y2


dy = y2r - y1

if abs(dy) < 1e-15:
    
    if abs(y1) < 1e-15:
        
        xr = x1
    else:
        
        xr = x1
else:
    t = (0.0 - y1) / dy
    xr = x1 + t * (x2 - x1)

print(f"{xr:.10f} {0.0:.10f}")