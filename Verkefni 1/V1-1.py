# Fyrst þurfum við að skilgreina a, b og fallið

punktar = [[-9.45, -9.4], [-1.4, -1.3]]

f = lambda s: 2*s**4 + 23*s**3 + 45*s**2 + 60*s + 50
target_E = (1*10**(-10))        # target_E er markmiðsskekkjan

for i in punktar:

    print(i)

    a = i[0]
    b = i[1]
    
    # Því næst þurfum við að skilgreina breyturnar fyrir helmingunaraðferðina

    n = 0                           # n er fjöldi ítrekana
    E = (b-a)/(2**n)                # E er skekkjan

    # Þá þurfum við að skilgreina while lykkjuna.
    # While lykkjan heldur áfram þar til skekkjan er minni en eða jafnt og markmiðsskekkjan.

    while E >= target_E:
        c = (a+b)/2                 # c er miðpunktur a og b
    
        if f(c) == 0:               # Ef fallgildið í c er 0, þá er c rótin
            break   
    
        if f(a)*f(c) < 0:           # Ef fallgildin í a og c hafa mismunandi formerki, þá er rótin á milli a og c
            b = c
        else:                       # Annars er rótin á milli c og b
            a = c
    
        n = n+1                     # Hækka fjölda ítrekana
        E = (b-a)/(2**n)            # Uppfæra skekkjuna

    print(c)                        # Prenta rótina
