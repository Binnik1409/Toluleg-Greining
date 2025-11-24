# Fyrst skilgreinum við leitarbilin og fallið

punktar = [[-9.45, -9.4], [-1.4, -1.3]]

f = lambda s: 2*s**4 + 23*s**3 + 45*s**2 + 60*s + 50
f_ = lambda s: 8*s**3 + 69*s**2 + 90*s + 60

target_E = (1*10**(-10))        # target_E er markmiðsskekkjan

villur = []

#====================
# Helmingunaraðferð!
#====================
for i in punktar:

    a = i[0]
    b = i[1]
    
    # Því næst þurfum við að skilgreina breyturnar fyrir helmingunaraðferðina

    n = 0                           # n er fjöldi ítrekana
    E = (b-a)/(2**n)                # E er skekkjan

    # Þá þurfum við að skilgreina while lykkjuna.
    # While lykkjan heldur áfram þar til skekkjan er minni en eða jafnt og markmiðsskekkjan.

    v = [E]

    while E > target_E:

        c = (a+b)/2                 # c er miðpunktur a og b
    
        if f(c) == 0:               # Ef fallgildið í c er 0, þá er c rótin
            break   
    
        if f(a)*f(c) < 0:           # Ef fallgildin í a og c hafa mismunandi formerki, þá er rótin á milli a og c
            b = c
        else:                       # Annars er rótin á milli c og b
            a = c
    
        n = n+1                     # Hækka fjölda ítrekana
        E = (b-a)/(2**n)            # Uppfæra skekkjuna
        
        v.append(E)

    villur.append(v)

#================
# Newton-Raphson
#================
for i in punktar:
    a = i[0]
    b = a - f(a)/f_(a)
    E = abs(b-a)
    
    v = [E]
    j = 0
    while E > target_E:
        b = a - f(a)/f_(a)
        E = abs(b-a)
        v.append(E)
        a = b

        j = j+1
        if j == 20:
            break

    villur.append(v)

#================
# Villur í töflu
#================

print("|  Ítrekun  |  Helmingunar, rót 1  |  Helmingunar, rót 2  |  Newton-Raphson, rót 1  |  Newton-Raphson, rót 2  |")
print("---------------------------------------------------------------------------------------------------------------")
for i in range(len(villur[0])):
    print(i, end="  |  ")
    for j in range(len(villur)):
        try:
            print(villur[j][i], end="  |  ")
        except:
            print("", end="  |  ")
    print()