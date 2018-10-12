import numpy as np
import matplotlib.pyplot as plt
nb_instance = 10
a = np.zeros(nb_instance)
x = []
for i in range (0, nb_instance):
    x.append(i)

for i in range (0, 10000):
    s = np.random.poisson(2)
    a[s%nb_instance] += 1
    print(s)
a = a*1.0/10000
plt.bar(x, a)
plt.show()