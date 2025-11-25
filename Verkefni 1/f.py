def f(s, m1=1, m2=2, k1=10, k2=5, c1=10, c2=1):
    coe1 = m1*m2
    coe2 = c2*(m1+m2*(c1+c2))
    coe3 = m1*k2+m2*(k1+k2)+c1*c2
    coe4 = c1*k2+c2*k1
    coe5 = k1*k2
    return coe1*(s**4) + coe2*(s**3) + coe3*(s**2) + coe4*(s) + coe5