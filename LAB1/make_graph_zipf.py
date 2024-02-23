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


def zipFunction(rank, a, b, c):
	return c/((rank+b)**a)

def heapsFunction(n, k, b):
    return k*n**b
news = open ("info_arxiv_abs.txt")
lineas = news.readlines()
f = open('test.txt', 'w', encoding='utf-8')
total = len(lineas)

array = []
count = 0
for l in range (0, total):
    #if (getFrequency(lineas[l]) > 1000):
    #if count < 500:
        array.append( getFrequency(lineas[l]) )
        count += 1




xList = [(x+1) for x in range(len(array))]
popt, pcov = curve_fit(zipFunction, xList, array, bounds=([0.7, -100000.0, -100000.0],[1.8, 100000.0, 1000000.0]))

print(popt)

plt.plot(xList, zipFunction(xList, *popt), 'g--', label='fit-with-bounds')

plt.plot(array)
plt.yscale('log')
plt.ylabel('frecuency')
plt.xlabel('rank')
plt.xscale('log')
plt.show()


