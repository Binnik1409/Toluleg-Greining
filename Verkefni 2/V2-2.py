import functions as f
import numpy as np

import matplotlib.pyplot as plt

w = 2*np.pi/24 #Gögn úr dæmi

t = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23] #Gögn úr dæmi
b = [12.0, 14.0, 13.9, 12.3, 11.7, 8.9, 6.3, 6.5, 6.1, 5.8, 6.6, 9.3] #Gögn úr dæmi
a = np.matrix([[np.cos(w*x), np.sin(w*x), 1] for x in t]) #Fylkið A skv. aðverð minnstu kvarðata
aT = np.transpose(a) #Transpose af A
aTa = np.dot(aT,a) #Transpose af A margfaldað við A
aTaI = np.linalg.inv(aTa) #Adnhverfa af margefeldi Transpose A og A
x = np.dot(np.dot(aTaI, aT), b) #Andhverfan margfaldað við transpose A og b skv. setningu gefur x

print("A:", x[0,0])
print("B:", x[0,1])
print("C:", x[0,2])


# plt.plot(t,b,'o')
# plt.plot(t,[f.qE0(i,x[0,0],x[0,1],x[0,2]) for i in t])
# plt.show() #It's beautiful