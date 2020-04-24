import matplotlib.pyplot as plt
import numpy as np

with open("data.csv") as f:
  data = f.read().split('\n')
  
x =  np.array([float(d.split(',')[0]) for d in data[1:]])
y1 = np.array([float(d.split(',')[1]) for d in data[1:]])
y2 = np.array([float(d.split(',')[2]) for d in data[1:]])


plt.subplot(2,1,1)
plt.grid(which='both', lw=.5)
plt.title("Czas zbieractwa od ilości wysłanych pików")
plt.plot(x,y1, label="lvl 1")
plt.plot(x,y2, label="lvl 3")
plt.legend()
plt.minorticks_on()

plt.subplot(2,1,2)
plt.grid()
plt.title("Zysk na minute od ilości wysłanych pików")
plt.plot(x, x*25*0.1/y1, lw=3,linestyle="dashed", label="lvl 1")
plt.plot(x, x*25*0.5/y2, lw=2,linestyle="dotted", label="lvl 3")
plt.plot(x, x*25*0.5/y2 - x*25*0.1/y1, lw=2,linestyle=":", label="diff 3-1")
plt.legend()

plt.tight_layout()

plt.show()
