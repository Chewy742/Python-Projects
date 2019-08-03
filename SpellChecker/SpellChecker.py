import csv

##Project involves a spell checker that reads and writes to a Dictionary.csv file, while updating the number of times a word has been suggested

#Returns a list of lists of the dictionary file
def getDictionaryList():
    f = open("dictionary.csv", "r")
    csv_f = csv.reader(f)
    myDictionaryList = [];
    for row in csv_f:
        myDictionaryList.append(row)

    myDictionaryList.pop(0) ## Removes the csv file column names
    f.close()
    return myDictionaryList

#Checks word to be true or returns a list of suggestions
def check_word(word):
    checkWord = word.lower()
    if isWord(checkWord):
        return True
    ##if we haven't found it, let's build possibilties, and then return the good suggestions
    ##I chose to do this here, instead of the actual functions themselves
    else:
        suggestionsList = getSuggestions(getPossibilities(checkWord))
        return suggestionsList

def getSuggestions(possibilities): ##handles possibilities into concrete suggestions, checking if those are words and handling unique cases such as a split word 
    suggestionsList = []
    possibilitiesList = possibilities
    for possibility in possibilitiesList:
        if isWord(possibility):
            suggestionsList.append(possibility)
        else:  # for corrections 4, spaced words
            for i in range(len(possibility)):
                if possibility[i] == " ":
                    word1 = possibility[:i]
                    word2 = possibility[i + 1:]
                    if isWord(word1) and isWord(word2):
                        suggestionsList.append(word1)
                        suggestionsList.append(word2)
    return suggestionsList

def isWord(word): ##JUST CHECKS IF ITS A WORD, NO SUGGESTIONS LIST

    checkWord = word.lower()  ##converts to lowercase
    done = False
    myDictionary = getDictionaryList()
    for row in myDictionary: ##Checks if the dictionary has the word
        if row[0] == checkWord:
            done = True
            return True
    return False


def getPossibilities(word): ##accumulates all possibilities
##All possibilities- each of the 5 possibility programs
    possibilities = []
    transposed = getTransposed(word)  # transposed words
    for element in transposed:
        possibilities.append(element)
    insertions = getInsertions(word)
    for element in insertions:
        possibilities.append(element)
    deletions = getDeletions(word)
    for element in deletions:
        possibilities.append(element)
    spaced = getSpaced(word)
    for element in spaced:
        possibilities.append(element)
    userSuggestions = isUserSuggestion(word)
    for element in userSuggestions:
        possibilities.append(element)

    return possibilities

def getTransposed(word): #If you transposed two letters accidentally
    result = []

    for i in range(0, len(word) - 1):
        l = word[:i]
        c1 = word[i]
        c2 = word[i + 1]
        r = word[i + 2:]
        n = l + c2 + c1 + r ##switches the order of the two letters at index i
        result.append(n)

    return result

def getInsertions(word): #If you forgot a letter
    result = []
    alphabet = []
    ##Create a list of the alphabet characters to insert
    for letter in range(97,123):
        alphabet.append(chr(letter))
    for i in range(0, len(word)+1):
        for character in alphabet:
            insertion = character
            start = word[:i]
            end = word[i:]
            newWord = start + insertion + end
            result. append(newWord)

    return result

def getDeletions(word): #If you inserted a random letter
    result = []

    for i in range (0, len(word)):
        start = word[:i]
        end = word[i+1:]
        newWord = start + end
        result.append(newWord)

    return result

def getSpaced(word): #If your word is spaced our

    result = []

    for i in range(0, len(word)):
        start = word[:i]
        end = word[i:]
        result.append(start + " " + end)

    return result

def isUserSuggestion(word):
    result = []
    dictionary = getDictionaryList()
    ##Row 5 is previous mispelled words, that have been associated with a correct spelling
    for row in dictionary:
        if (row[5] == word):
            result.append(row[0])

    return result

def update_corrections(old_word, new_word):
    new = new_word.lower()
    old = old_word.lower()
    if isWord(new): ##increment the number of times selected
        incrementCSVFile(old,new)
    else: ##create a new line in the dictionary
        addLine(old, new)

def incrementCSVFile(old, new): ##writes back to dictionary

    wordList = getDictionaryList()
    rewriteList = []
    firstLine = ["Word,","Relative_Frequency,","User_Created,","Times_Selected,","Frequency","Mispellings"] ##just rewriting the file
    rewriteList.append(firstLine)
    for line in wordList:
        if (line[0] == new):
            count = int(line[3])
            count += 1
            newCount = str(count)
            newLine = [line[0], line[1], line[2], newCount, line[4], line[5]] ##line with new count
            rewriteList.append(newLine)
        else:
            rewriteList.append(line)
    f = open("dictionary.csv", "w")
    writer = csv.writer(f)
    writer.writerows(rewriteList)
    f.close()

def addLine(old, new): ##adding a single entry in the dictionary, user added
    f = open("dictionary.csv", "a")
    csvwriter = csv.writer(f)
    csvwriter.writerow([new,"","","1","1",old])
    f.close()


if __name__ == "__main__":

    done = False
    while not done:
        w = input("Please enter a word (enter -1 to end: ")
        if w == "-1":
            print("Exiting.")
            break
            done = True

        c = check_word(w)

        if c == True:
            print("The word is correctly spelled.")
        else:
            print("Suggested corrections are: ", c)
            f = input("Enter one of the words or your own correction: ")
            r = update_corrections(w, f)



