import math as m

def mjaaa(start, m1=1, m2=1, l1=2, l2=2, g=9.81):
    x1 = start[0]
    x2 = start[1]
    y1 = start[2]
    y2 = start[3]
    delta = y1-x1
    a = m2*l1*(x2**2)*m.sin(delta)*m.cos(delta)
    b = m2*g*m.sin(y1)*m.cos(delta)
    c = m2*l2*(y2**2)*m.sin(delta)
    d = (m1+m2)*g*m.sin(x1)
    e = (m1+m2)*l1
    f = m2*l1*(m.cos(delta)**2)
    func1 = (a+b+c-d)/(e-f)
    i = m2*l2*(y2**2)*m.sin(delta)*m.cos(delta)
    j = (m1+m2)*(g*m.sin(x1)*m.cos(delta)-l1*(x2**2)*m.sin(delta)-g*m.sin(y1))
    k = (m1+m2)*l2
    l = m2*l2*(m.cos(delta)**2)
    func2 = (-i+j)/(k-l)
    return [x2, func1, y2, func2]

    