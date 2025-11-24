def newton(x0,tol, f, Df):
    oldx=x0+2*tol
    x=x0
    errors = []
    while abs(oldx-x)>tol:
        oldx=x
        x=x-f(x)/Df(x)
<<<<<<< HEAD
    return [x, abs(oldx-x)]
=======
        errors.append(abs(oldx-x))
    return(x, errors)
>>>>>>> 7bd944cdadb6f16a46da25169db458a0aa1ba788

