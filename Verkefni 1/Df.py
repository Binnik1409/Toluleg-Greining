def Df(s, m1=1, m2=2, k1=10, k2=5, c1=10, c2=1):
    f3 = 4*m1*m2*(s**3)
    f2 = 3*c2*(m1+m2*(c1+c2))*(s**2)
    f1 = 2*(m1*k2+m2*(k1+k2)+c1*c2)*(s**1)
    f0 = c1*k2+c2*k1
    return f3 + f2 + f1 + f0