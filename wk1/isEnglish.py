# detectEnglish.py

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VALID = LETTERS + LETTERS.lower() + ' \t\n\r'


def loadDictionary():
    dictionaryFile = open("dictionary.txt")
    englishWords = {}
    with dictionaryFile:
        for word in dictionaryFile.read().split('\n'):
            englishWords[word] = None
    return englishWords

ENGLISH_WORDS = loadDictionary()


def removeInvalid(message):
    validOnly = []
    for symbol in message:
        if symbol in VALID:
            validOnly.append(symbol)
    return ''.join(validOnly)


def getEnglishCount(message):
    message = message.upper()
    message = removeInvalid(message)
    possibleWords = message.split()

    if possibleWords == []:
        return 0.0

    matches = 0
    for word in possibleWords:
        if word in ENGLISH_WORDS:
            matches += 1
    return float(matches)/len(possibleWords)


def isEnglish(message, wordPercentage=20, letterPercentage=85):
    wordMatch = getEnglishCount(message) * 100 >= wordPercentage
    numLetters = len(removeInvalid(message))
    messageValidPercentage = float(numLetters)/len(message) * 100
    lettersMatch = messageValidPercentage >= letterPercentage
    return wordMatch and lettersMatch
