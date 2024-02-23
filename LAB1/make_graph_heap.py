from traceback import print_last
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def getFrequency (line):
    frequency = line[0];
    for i in range(1, len(line)):
        if line[i] != ' ':
            frequency = frequency + line[i]
        else:
            break
    return int(frequency)

def heapLaw (n, k , b):
    return k*n**b

xvalues = []    # num words
yvalues = []     # num diff words


for i in range(1, 15):
    name = 'info_novels' + str(i) + '.txt'
    text = open(name)
    lineas = text.readlines()

    total = len(lineas)
    difWords = 0
    nWords = 0
    for l in range (0, total):
            nWords += getFrequency(lineas[l])
            difWords += 1
    xvalues.append(nWords)
    yvalues.append(difWords)
    print("Número total de palabras ", nWords, "------Número de palabras diferentes ", difWords)


popt, pcov = curve_fit(heapLaw, xvalues, yvalues)

print(popt)

plt.plot(xvalues, heapLaw(xvalues, *popt), 'g--', label='fit-with-bounds')

plt.plot(xvalues, yvalues)
#plt.yscale('log')
plt.ylabel('different words')
plt.xlabel('words')
#plt.xscale('log')
plt.show()
