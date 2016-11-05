class Key:
    def __init__(self, encodechars='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        self.__decode = {}
        self.__possibles = {}
        self.encodechars = encodechars.upper()
        self.key = {}

    def set(self, cipherchar, plainchar, conflict_exception=True):
        cipherchar = cipherchar.upper()
        plainchar = plainchar.lower()
        if self.__decode[cipherchar] is not None \
                and conflict_exception is True:
            if self.__decode[cipherchar] != plainchar:
                raise Exception("Tried to set existing key to a new value")
        else:
            self.__decode[cipherchar] = plainchar
            self.__possibles[cipherchar] = plainchar
            # Remove plaintext char from all other possible ciphertext
            # characters
            for c in self.__possibles:
                if c != cipherchar:
                    self.eliminate(c, plainchar)

    def set_string(self, ciphertext, plaintext):
        if len(ciphertext) != len(plaintext):
            raise Exception("ciphertext and plaintext are different lengths")
        for i in range(len(ciphertext)):
            self.set(ciphertext[i], plaintext[i])

    def eliminate(self, cipherchar, plainchar):
        cipherchar = cipherchar.upper()
        plainchar = plainchar.lower()
        self.__possibles[cipherchar] = \
            self.__possibles[cipherchar].replace(plainchar, '')
        if len(self.__possibles[cipherchar]) == 1:
            # we have elimiated all other possibilities so make the
            # remaining character equal to the key
            self.set(cipherchar, self.__possibles[cipherchar][0])

    def decipher(self, ciphertext):
        plaintext = ''
        for c in ciphertext:
            if c in self.encodechars:
                if self.__decode[c] is not None:
                    plaintext += self.__decode[c]
                else:
                    plaintext += c
            else:
                plaintext += c
        return plaintext

    @property
    def key(self):
        return self.__decode

    @key.setter
    def key(self, newkey):
        for c in self.encodechars:
            self.__decode[c] = None
            self.__possibles[c] = self.encodechars.lower()
        for k in newkey:
            self.set(k, newkey[k])

    @property
    def possible_keys(self):
        return self.__possibles
