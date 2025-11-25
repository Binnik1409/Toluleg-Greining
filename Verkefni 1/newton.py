def newton(x0,tol, f, Df, errors = False):
    oldx=x0+2*tol
    x=x0
    if errors:
        errors = []
        while abs(oldx-x)>tol:
            oldx=x
            x=x-f(x)/Df(x)
            errors.append(abs(oldx-x))
        return x, errors
    else:
        while abs(oldx-x)>tol:
            oldx=x
            x=x-f(x)/Df(x)
        return x
