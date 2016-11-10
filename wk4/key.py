class Key:
    def __init__(self, encodechars='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        self.__decode = {}
        self.__possibles = {}
        self.__history = []
        self.__key_history = []
        self.encodechars = encodechars.upper()
        self.key = {}
        self.__history_pointer = 0
        self.__history = [("", "", "Initialisation")]
        self.__key_history = [(self.__decode, self.__possibles)]

    def set(self, cipherchar, plainchar, reason, conflict_exception=True):
        # if we are not at the head of the history list
        # and we are setting something, we need to delete
        # all current future steps and start a new branch here
        if self.__history_pointer + 1 < len(self.__history):
            self.__history = self.__history[:self.__history_pointer + 1]
            self.__key_history = \
                self.__key_history[:self.__history_pointer + 1]
            self.__decode, self.__possibles = \
                self.__key_history[self.__history_pointer]
        # convert cipherchar and plainchar into appropriate case
        cipherchar = cipherchar.upper()
        plainchar = plainchar.lower()
        # Check to ensure we are not overwriting a key we already set
        if self.__decode[cipherchar] is not None \
                and conflict_exception is True:
            if self.__decode[cipherchar] != plainchar:
                raise Exception("Tried to set existing key to a new value")
        else:
            # Get on with setting the character
            self.__decode[cipherchar] = plainchar
            self.__possibles[cipherchar] = plainchar
            # Remove plaintext char from all other possible ciphertext
            # characters
            for c in self.__possibles:
                if c != cipherchar:
                    self.eliminate(c, plainchar)
            # Update history
            self.__update_history(cipherchar, plainchar, reason)

    def __update_history(self, cipherchar, plainchar, reason):
        self.__history.append((cipherchar, plainchar, reason))
        # get copies of the current state using the dict() function
        self.__key_history.append((dict(self.__decode), dict(self.__possibles)))
        self.__history_pointer += 1

    def set_string(self, ciphertext, plaintext, reason):
        if len(ciphertext) != len(plaintext):
            raise Exception("ciphertext and plaintext are different lengths")
        for i in range(len(ciphertext)):
            self.set(ciphertext[i], plaintext[i], reason)

    def eliminate(self, cipherchar, plainchar):
        cipherchar = cipherchar.upper()
        plainchar = plainchar.lower()
        self.__possibles[cipherchar] = \
            self.__possibles[cipherchar].replace(plainchar, '')
        if len(self.__possibles[cipherchar]) == 1:
            # we have elimiated all other possibilities so make the
            # remaining character equal to the key
            self.set(cipherchar, self.__possibles[cipherchar][0], "Elimination")

    def decipher(self, ciphertext):
        plaintext = ''
        # deciper at appropriate point in our history
        key, poss = self.__key_history[self.__history_pointer]
        for c in ciphertext:
            if c in self.encodechars:
                if key[c] is not None:
                    plaintext += self.key[c]
                else:
                    plaintext += c
            else:
                plaintext += c
        return plaintext

    @property
    def key(self):
        key, poss = self.__key_history[self.__history_pointer]
        return key

    @key.setter
    def key(self, newkey):
        # Reset the key
        for c in self.encodechars:
            self.__decode[c] = None
            self.__possibles[c] = self.encodechars.lower()
            self.history = 0
        # copy in the new values
        for k in newkey:
            self.set(k, newkey[k])

    @property
    def possible_keys(self):
        key, poss = self.__key_history[self.__history_pointer]
        return poss

    @property
    def history(self):
        outtext = ""
        for i in range(len(self.__history)):
            # Mark our current position
            if i == self.__history_pointer:
                outtext += "**"
            outtext += str(i) + "\n\n"
            outtext += str(self.__history[i]) + "\n\n"
            outtext += str(self.__key_history[i]) + "\n\n\n"
        return outtext

    @history.setter
    def history(self, index):
        if index < 0:
            # Move history relative
            if self.__history_pointer + index < 0:
                raise Exception("Attempt to move history back beyond 0")
            else:
                self.__history_pointer = self.__history_pointer + index
        else:
            if index > len(self.__history):
                raise Exception("Attempt to move beyond max future")
            else:
                self.__history_pointer = index
