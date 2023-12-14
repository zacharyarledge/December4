from timeit import default_timer as timer
import sys
#function for hash code
def hc(word):
    n = len(word)
    i = 0
    hashCode = 0
    while (n > 0): #given formula
        hashCode += ord(word[i])*(a**(n-1))
        n -= 1
        i += 1
    return hashCode

#compression function for indexing in hash
def h(word):
    compression = hc(word) % tableSize
    while(hashTable[compression] != ""):
        if hashTable[compression] == word: #returns if hash table already has word (no duplicates)
            return
        elif compression == 28: #loops around array
            compression = 0
        else:
            compression += 1
    hashTable[compression] = word

#checks hash table for word and adds to dictionary if exists
def check(word):
    compression = hc(word) % tableSize
    originalCompression = compression
    #updates word count if match found in first position
    if (hashTable[compression] == word):
        updateDict(word)
        return
    #handles wrap around array
    if compression != 28:
        compression += 1
    else:
        compression = 0
    #checks against the rest of the keywords and returns if it is not a keyword
    while(hashTable[compression] != word):
        if (compression == originalCompression):
            return
        if compression == 28:
            compression = 0
        else:
            compression += 1
    updateDict(word)

#adds to the count(value) of the word (key)
def updateDict(word):
    myDict[word] = myDict[word] + 1

if len(sys.argv) != 3:
    raise ValueError('Please provide two file names.')

initialText = sys.argv[1]
speechText = sys.argv[2]
print("\nThe hash table will be built from:", initialText)
print("\nThe hash table will be compared to:", speechText)

start = timer()

#creates list of initial words for hash table
f = open(initialText, "r")
initialList = []
for text in f:
    text = text.lower()
    text = text.strip(".,\n''")
    text = text.split()
    initialList.extend(text)

f.close()

#variables given for hash table
tableSize = 29
hashTable = [""]*tableSize
a = 31

#send list of words to hash table and creates dictionary with the key words (keys) set to 0 (value)
myDict = {}
for text in initialList:
    myDict[text] = 0
    h(text)

#creates list of speech words to check against hash table
f = open(speechText, "r")
linesRead = 0
wordsInSpeech = []
for text in f:
    if (text != '\n'): #counts non-blank lines
        linesRead += 1
    text = text.lower()
    text = text.strip(".,\n''")
    text = text.split()
    wordsInSpeech.extend(text)

f.close()
wordsRead = len(wordsInSpeech)

#checks all words from MLKSpeech to the keywords
for text in wordsInSpeech:
    check(text)

#display in format
print("**********************")
print("***** Statistics *****")
print("**********************")
print("Total lines read: {0}".format(linesRead))
print("Total words read: {0}".format(wordsRead))
print("\nBreakdown by keyword:")
for i in range(len(hashTable)):
    if hashTable[i] != "":
        print("{0} : {1}".format(myDict[hashTable[i]], hashTable[i]))
end = timer()
print("Total Time of Program: {:.8f} milliseconds".format(end-start))
