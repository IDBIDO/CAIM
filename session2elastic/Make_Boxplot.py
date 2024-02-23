import matplotlib.pyplot as plt
import numpy as np
array = []

results = open ("test.txt")
lineas = results.readlines()
total = len(lineas)
#print(lineas)
for value in lineas:
    array.append(float(value))

plt.boxplot(array)
plt.show()