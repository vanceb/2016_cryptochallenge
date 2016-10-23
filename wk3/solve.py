import words


class Substitution:

    def __init__(self, key=None, encode_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        self.d = words.wp_dict()
        self.d.load()
        self.encode_chars = encode_chars

        # Setup the key
        if key:
            # We have been given a key...
            self.key = key
        else:
            # Prepare to solve for the key
            self.key = {}
            for c in self.encode_chars:
                self.key[c] = None

    def solve(self, ciphertext):
        # Try to solve the ciphertext...

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
