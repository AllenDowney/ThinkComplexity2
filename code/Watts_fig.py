from pylab import *

t = []
for line in file('watts.out'):
    data = [float(x) for x in line.split()]
    t.append(data)

P, L, C = zip(*t)

L = [x/L[0] for x in L]
C = [x/C[0] for x in C]

semilogx(P, L, 'bo-')
hold('on')
semilogx(P, C, 'rs-')
show()
