import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


intervals = float(1) #Spacing between each line of the displayed grid 
#intervals = float(getRealGrid())
fig,ax=plt.subplots()
#ax.set_xticklabels([]) 
#ax.set_yticklabels([])

locx = plticker.MultipleLocator(base=1)
locy = plticker.MultipleLocator(base=1)

ax.xaxis.set_major_locator(locx)
ax.yaxis.set_major_locator(locy)

plt.gca().xaxis.grid(False)
ax.grid(b= False, which='both', axis='both', linestyle='-',zorder =10)


x = np.linspace(-5,5,1000)
y = (x**2) 
#x = a_two*x*b_two
plt.plot(x,y, 'r', color = '0')

x = np.linspace(-5,5,1000)
y = (x**2)+ 1.26
#x = a_two*x*b_two
plt.plot(x,y, 'r', color = '0')

plt.show()