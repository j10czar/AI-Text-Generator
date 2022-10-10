from asyncore import read
from cgitb import text
import random
from tracemalloc import start
import re
import os



#change these before running
#modify project dir in order for the program to read in text files
wordTree = {}
blockedWords = []
fillerWords = []
# project_dir = r'C:\Users\jasea\VSCodeRepos\Basic-AI-Text-Generator'
project_dir = os.path.dirname(os.path.realpath(__file__))

#adds words into word tree from w 
def populateTree(w):
    for word in w:
        wordTree[word] = []             


#returns an arry of all unique words
def unique(w):
    uniqueWords = []
    for word in w:
        if word not in uniqueWords:
            uniqueWords.append(word)

    return uniqueWords

#makes words easier to process
def filterWord(word):
    newWord = ''


    for w in word:
        if w!= '¶' and w!='(' and w!=')' and w!='.' and w!='*' and w!='“' and w!='”' and w!=',' and w!=':' and w!=';' and w!='"' and w!='-':
            newWord += w
    return newWord.lower().strip()     




#filters the words to not be a single charater
def filter(words):

    filtered = []
    for word in words:
        word.replace('\u200b','')
        if word != '' and word != '-' and word not in blockedWords and not word.isdigit():
            filtered.append(filterWord(word))

    return filtered        

#returns an array of possible words that follow a word in a given text
def matchWords(word, wordList):
    matchedWords = []
    occurrences = []

    for index, elem in enumerate(wordList):
        if elem == word:
            occurrences.append(index)
     

    for i in occurrences:
        if i >= len(wordList)-2:
            i = len(wordList)-3

        matchedWords.append(wordList[i+1])

    return matchedWords    



#populates tree with occurrences array
def populateWords(wordList, wordTree):
    for key in wordTree:
        wordTree[key] = matchWords(key, wordList)


#runs the simulatoin
def runSimulation(wordTree,sortedWords,wordNum):
    output = ''
    if wordNum == 'sentence':
        sentenceNum = random.randint(10,18)
        text = ''
        lastWord = ''
        startIndex = random.randint(0, len(sortedWords)-2)

        lastWord=sortedWords[startIndex]
        text+=lastWord[0:1].upper() + lastWord[1:len(lastWord)] +' '

        for i in range(0,sentenceNum):
            arr = wordTree[lastWord]
            lastWord = arr[random.randint(0, len(arr)-1)]
            if i==sentenceNum-1:
                text+= lastWord 
            else:
                text+= lastWord + ' '
        print(text+'.')        
    else:
        while(wordNum>=5):
            sentenceNum = random.randint(10,18)
            text = ''
            lastWord = ''
            startIndex = random.randint(0,len(sortedWords)-2)

            lastWord=sortedWords[startIndex]
            text+=lastWord[0:1].upper() + lastWord[1:len(lastWord)] +' '

            for i in range(0,sentenceNum):
                arr = wordTree[lastWord]
                lastWord = arr[random.randint(0, len(arr)-1)]
                if i==sentenceNum-1:
                    text+= lastWord
                else:
                    text+= lastWord + ' '
            output+=text+'. '
            wordNum -= sentenceNum
        print(output)
#intro sequence
print('-----------')
print("Basic AI Text Generator")
print("By Jason Tenzcar")
print('-----------')
print("What file would you like to generate text from?")
print("")
print("")


#reads in all folders in project dir
folder_dir = os.listdir(os.path.expanduser(project_dir))

txt_files = []

for file in folder_dir:
    if file[len(file)-4:] == '.txt':
        txt_files.append(file)

print_num = 1
for file in txt_files:
    print(str(print_num)+'- '+file)
    print_num+=1

print("")
print("")    
#takes and processes user input
while(True):
    user_choice = input('Type the file number to generate text or type multiple file numbers seperated by "/" for hybrid generation.')
    print("")
    if user_choice.isdigit() and int(user_choice)-1<=len(txt_files):
        #opens text file(s) for reading and puts them into a useable string
        textInput = txt_files[int(user_choice)-1]
        print('generating word tree from '+str(textInput)+'...')
        file = open(textInput,'r')
        inputText = filter(re.split(' |\n', file.read())) 
        break
    elif len(user_choice.split('/'))>1:
        choices = user_choice.split('/')
        print('You are now on hybrid mode...')
        print('generating word tree from: ')
        inputText = []
        for choice in choices:
            if choice.isdigit and int(choice)<len(txt_files)+1:
                print(choice+"- "+txt_files[int(choice)-1])
                openedText = open(txt_files[int(choice)-1],'r')
                inputText += filter(re.split(' |\n', openedText.read()))  
        break
    else:
        print('invalid input')        
#opens text file(s) for reading and puts them into a useable string



sortedText = unique(inputText)
sortedText.sort()



#populates wordTree with corresponding words
print('populating tree with unique words...')
populateTree(sortedText)
populateWords(inputText, wordTree)
print('tree has been populated with '+str(len(sortedText))+' unique words')





running = True
while(running):
    userInput = input('Press enter to generate sentence or type number of words you want in generation.')
    if userInput == '':
        print('__________________')
        runSimulation(wordTree,sortedText,'sentence')
        print('__________________')
    elif userInput == 'e':
        running = False

    else:
        if userInput.isdigit():
            print('__________________')
            runSimulation(wordTree,sortedText,int(userInput)-1)
            print('__________________')
        else:
            print('please type a number or "e" to exit')