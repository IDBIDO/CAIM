# esto
# Prueba de push
import enchant
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def getFrequency (line):
    frequency = line[0];
    for i in range(1, len(line)):
        if line[i] != ',':
            frequency = frequency + line[i]
        else:
            break;
    return int(frequency)

def getWold (line):
    word = ""
    i = 0;
    while i < len(line):
        if (line[i] == ','):
            break;
        i = i +1;
    i += 2;
    while i < len(line) -1:
        word = word + line[i];
        i = i + 1;
    return word

def isWord(word):
    dot = False
    number = False
    badChars = False
    for letter in word:
        if letter == '.':
            dot = True
            break
        if letter >= '0' and letter <= '9':
            number = True
            break
        if not((letter >= "a" and letter <= "z") or letter == 'æ' or letter == 'þ' or letter == 'ð'):
            badChars = True
            break
    if dot or number or badChars:
        return False
    else:
        return True

news = open ("arviv_abs.txt")
lineas = news.readlines()
f = open('info_arviv_abs.txt', 'w', encoding='utf-8')
total = len(lineas) - 2

#rango = 1
array = []
words = []
d = enchant.Dict("en_US")
for l in range (0, total):
    freq = getFrequency(lineas[l])
    w = getWold(lineas[l])
    if d.check(w) and isWord(w):
        #f.write(w)
        #f.write('\n')
        words.append(w)
        array.append(freq)
        


stop_words = set(stopwords.words('english'))
print(stop_words)
res = array[::-1]
res_word = words[::-1]

menor10 = 0
stopWordNum = 0
for l in range(0, len(array)):
    if res[l] > 1:
        if True:
            f.write(str(res[l]))
            f.write(' ')
            f.write(res_word[l])
            f.write('\n')
        else:
            stopWordNum += 1
    else:
        menor10 += 1
print('frecuencia menor 10 ' + str(menor10))

print('stop word ' + str(stopWordNum))
print(len(array)- menor10 - stopWordNum);
f.close