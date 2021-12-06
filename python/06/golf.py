import sys
from functools import cache
d=[int(l) for l in sys.stdin.read().split(",")]
g=cache(lambda t,d:1+sum(g(8,e-1) for e in range(d-t,0,-7)))
s=lambda n:print(sum([g(t,n) for t in d]))
s(80)
s(256)
