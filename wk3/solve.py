import words


class Substitution:

    def __init__(self, key=None, encode_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        self.d = words.wp_dict()
        self.d.load()
        self.encode_chars = encode_chars
        self.__ciphertext=''

        # Setup the key
        if key:
            # We have been given a key...
            self.key = key
        else:
            # Prepare to solve for the key
            self.key = {}
            for c in self.encode_chars:
                self.key[c] = None

    def solve(self):
        # Try to solve the ciphertext...
        ciphertext = self.ciphertext

        # Create all possibile solutions, which we wil knock out...
        self.cipher_chars = {}
        for c in self.encode_chars:
            if self.key[c] is None:
                self.cipher_chars[c] = self.encode_chars
            else:
                self.cipher_chars[c] = self.key[c]

        # Go through each word in the ciphertext
        for word in ciphertext.split():
            # Get matches from the pattern dictionary
            pos_matches = self.d.find(word)
            # Check to see whether we have any hits
            if pos_matches:
                # create a variable to hold the possibilities for each
                # ciphertext character
                word_chars = {}
                # Loop over each character in the ciphertext word
                for i in range(len(word)):
                    # If we have not seen the character in the word yet
                    # then initialise
                    if word[i] not in word_chars:
                        word_chars[word[i]] = {}
                    # Loop around each potential match
                    for match in pos_matches:
                        # mark the possible matches for the ciphertext
                        # character
                        word_chars[word[i]][match[i]] = 1
                # Loop over each of the ciphertext word characters again
                for c in word_chars:
                    # Check that it is a character we are looking to decode
                    if c in self.encode_chars:
                        # initialise a variable to hold the still-good
                        # characters
                        ok = ''
                        # Loop over all remaining possible solution characters
                        # for this ciphertext character
                        for letter in self.cipher_chars[c]:
                            if letter in word_chars[c]:
                                # if it is still a possibility then keep it
                                ok += letter
                        # Set the remaining possibilities for the
                        # ciphertext character
                        self.cipher_chars[c] = ok

        # Where we have solved a particular cypher letter let's add
        # it to the Key
        for c in self.cipher_chars:
            if len(self.cipher_chars[c]) == 1:
                self.key[c] = self.cipher_chars[c]

        # Have a second round of elimination
        # If the letter is in the key then let's remove it as a possible
        solved_letters = ''
        for cc in self.key:
            if self.key[cc]:
                solved_letters += self.key[cc]
        for c in self.cipher_chars:
            if len(self.cipher_chars[c]) > 1:
                ok = ''
                for d in self.cipher_chars[c]:
                    if d not in solved_letters:
                        ok += d
                self.cipher_chars[c] = ok

        # Convert the ciphertext into the plaintext (or mix)
        outtext = ''
        for c in ciphertext:
            if c in self.encode_chars:
                if self.key[c]:
                    outtext += self.key[c].lower()
                else:
                    outtext += c
            else:
                outtext += c
        return outtext


    def solve2(self):
        # Try to solve the ciphertext...

        # Create all possibile solutions, which we will knock out...
        self.reset_cipher_chars()

        # Go through each word in the (safer)ciphertext
        # Using the plaintext as the input provides any partial solution
        # to be reused
        safertext = self.__safertext(self.plaintext)
        # Loop through each word
        for word in safertext.split():
            word = word.strip()
            # Get matches from the pattern dictionary
            pos_matches = self.d.find(word)
            print(word + ": " + str(pos_matches))
            # Check to see whether we have any hits
            if pos_matches:
                # create a variable to hold the possibilities for each
                # ciphertext character
                word_chars = {}
                # Loop over each character in the ciphertext word
                for i in range(len(word)):
                    # If we have not seen the character in the word yet
                    # then initialise
                    if word[i] not in word_chars:
                        word_chars[word[i]] = {}
                    # Loop around each potential match
                    for match in pos_matches:
                        # mark the possible matches for the ciphertext
                        # character
                        word_chars[word[i]][match[i]] = 1
                # Loop over each of the ciphertext word characters again
                for c in word_chars:
                    # Check that it is a character we are looking to decode
                    if c in self.encode_chars:
                        # initialise a variable to hold the still-good
                        # characters
                        ok = ''
                        # Loop over all remaining possible solution characters
                        # for this ciphertext character
                        for letter in self.cipher_chars[c]:
                            if letter in word_chars[c]:
                                # if it is still a possibility then keep it
                                ok += letter
                        # Set the remaining possibilities for the
                        # ciphertext character
                        self.cipher_chars[c] = ok
            else:
                print("Unable to find a match for pattern: " + word)

        # Where we have solved a particular cypher letter let's add
        # it to the Key
        for c in self.cipher_chars:
            if len(self.cipher_chars[c]) == 1:
                self.key[c] = self.cipher_chars[c]

        # Have a second round of elimination
        # If the letter is in the key then let's remove it as a possible
        solved_letters = ''
        for cc in self.key:
            if self.key[cc]:
                solved_letters += self.key[cc]
        for c in self.cipher_chars:
            if len(self.cipher_chars[c]) > 1:
                ok = ''
                for d in self.cipher_chars[c]:
                    if d not in solved_letters:
                        ok += d
                self.cipher_chars[c] = ok
        return self.plaintext

    # Solve3 tries a word by word solution rahter than a whole solution
    # From testing this seems to get a few characters wrong...
    # This is dictionary dependent...  dynamix vs dynamic
    def solve3(self, most_matches=10, reverse=False):
        #self.reset_cipher_chars()
        safertext = self.__safertext(self.plaintext)
        words = safertext.split()
        if reverse:
            words = reversed(words)
        for word in words:
            # Convert as much to plaintext as possible
            matchword = ''
            for c in word:
                if self.key[c]:
                    matchword += self.key[c].lower()
                else:
                    matchword += c.upper()
            solutions = self.d.find(matchword)
            if solutions:
                if len(solutions) <= most_matches:
                    for i in range(len(matchword)):
                        ok = ''
                        # go through the possibilities we have for the solution
                        for match in solutions:
                            if matchword[i].isupper():
                                if match[i] in self.cipher_chars[matchword[i]]:
                                    ok += match[i]
                        self.cipher_chars[matchword[i]] = ok
        # Check to see whether we have solved any cipher characters
        # Store them in the key if we have
            for c in self.cipher_chars:
                if len(self.cipher_chars[c]) == 1:
                    if self.key[c]:
                        if self.key[c] != self.cipher_chars[c][0]:
                            raise Exception("Solved for 2 different keys"
                                            " for the same cipher character")
                    #self.key[c] = self.cipher_chars[c][0]
                    try:
                        self.add_key(c,self.cipher_chars[c][0])
                    except:
                        print("Problem writing: Cipherchar: " + c +
                              " Plainchar: " + self.cipher_chars[c])
        return self.plaintext


    def add_key(self, cipherchar, plainchar):
        if self.key[cipherchar] is None:
            for c in self.key:
                if self.key[c] == plainchar:
                    if c != cipherchar:
                        print("Duplicate")
                        raise Exception("Plaintext character already found")
            self.key[cipherchar] = plainchar
        else:
            if self.key[cipherchar] != plainchar:
                print("Overwrite")
                raise Exception("Tried to overwrite a previously allocated key")

    def reset(self):
        # Prepare to solve for the key
        self.key = {}
        for c in self.encode_chars:
            self.key[c] = None
        self.reset_cipher_chars()

    def reset_cipher_chars(self):
        # Create all possibile solutions, which we wil knock out...
        self.cipher_chars = {}
        for c in self.encode_chars:
            if self.key[c] is None:
                self.cipher_chars[c] = self.encode_chars
            else:
                self.cipher_chars[c] = self.key[c]

    @property
    def ciphertext(self):
        return self.__ciphertext

    @ciphertext.setter
    def ciphertext(self, text):
        self.__ciphertext = text
        # reset the keys
        self.reset()

    def __safertext(self, text):
        safertext = ''
        for c in text:
            if c in self.encode_chars or c in ' \t\n':
                safertext += c
        return safertext

    @property
    def plaintext(self):
        # Convert the ciphertext into the plaintext (or mix)
        outtext = ''
        for c in self.ciphertext:
            if c in self.encode_chars:
                if self.key[c]:
                    outtext += self.key[c].lower()
                else:
                    outtext += c.upper()
            else:
                outtext += c.upper()
        return outtext
