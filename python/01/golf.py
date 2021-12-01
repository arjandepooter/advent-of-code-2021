import sys
p=print
d=[int(l) for l in sys.stdin.readlines() if l.strip()]
s=lambda l,n:len([0 for (a,b) in zip(l,l[n:]) if b>a])
p(s(d,1))
p(s(d,3))