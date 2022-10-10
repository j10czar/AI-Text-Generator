from asyncore import read
from cgitb import text
from curses.ascii import isdigit
import random
from tracemalloc import start
import re

def unique(w):
    uniqueWords = []
    for word in w:
        if word not in uniqueWords:
            uniqueWords.append(word)

    return uniqueWords

def filterWord(word):
    newWord = ''


    for w in word:
        if w!='(' and w!=')' and w!='.' and w!='*' and w!='“' and w!='”' and w!=',' and w!=':' and w!=';' and w!='"' and w!='-':
            newWord += w
    return newWord.lower().strip()

def filter(words):

    filtered = []
    for word in words:
        word.replace('\u200b','')
        if word != '' and word != '-':
            filtered.append(filterWord(word))

    return filtered

textInput = 'bee.txt'


file = open(textInput,'r')
inputText = filter(re.split(' |\n', file.read()))
sortedText = unique(inputText)
sortedText.sort()

print('generating an array of unique words')
print(sortedText)