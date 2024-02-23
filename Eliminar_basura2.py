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

news = open ("news_alpha.txt")
lineas = news.readlines()
f = open('info.txt', 'w', encoding='utf-8')
total = len(lineas) - 2

#rango = 1
for l in range (0, total):
    freq = getFrequency(lineas[l])
    w = getWold(lineas[l])

    if isWord(w):
        #f.write(rango)
        #f.write(', ')
        f.write(str(freq))
        f.write(', ')
        f.write(w)
        f.write('\n')
        #rango += 1

f.close
