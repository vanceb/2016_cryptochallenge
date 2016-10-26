import argparse
import words


class Wordsolve:

    def __init__(self,
                 encodechars='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                 dictionary="dictionary.txt"):
        # Decide which characters in the ciphertext we are interested in
        self.encodechars = encodechars.upper()
        # Reset the ciphertext
        self.__ciphertext = ''
        # Load the pattern matching dictionary
        self.dictionary = words.wp_dict()
        self.dictionary.load(dictionary=dictionary)
        self.reset()

    @property
    def ciphertext(self):
        return self.__ciphertext

    @ciphertext.setter
    def ciphertext(self, text):
        # Make sure that the ciphertext is uppercase
        self.__ciphertext = text.upper()
        # Reset the key amd key possibilities
        self.reset()

    def __safertext(self):
        safertext = ''
        for c in self.plaintext:
            if c in " \n\t":
                # Deal with whitespace first
                safertext += " "
            elif c.upper() in self.encodechars:
                # Only include characters that we are trying to solve
                # i.e. remove punctuation etc
                safertext += c
        return safertext

    @property
    def plaintext(self):
        text = ''
        for c in self.__ciphertext:
            # Check that we are trying to solve for the character
            if c in self.key:
                # if the key is not None then we have a solution for it
                if self.key[c]:
                    # So replace the ciphertext character with the solution
                    text += self.key[c].lower()
                else:
                    # just put in the ciphertext
                    text += c.upper()
            else:
                # Just put in the character
                text += c
        return text

    def reset(self):
        # Set up our key, ready for solving
        self.key = {}
        # Set up the possible key matches.
        # Initially every cipher character coule be ever plaintext character
        self.poss_keys = {}

        # Initialise
        for c in self.encodechars:
            self.key[c] = None
            self.poss_keys[c] = self.encodechars.lower()

    def solve(self, max_loops=3, max_matches=1, reverse=False):
        loops = 0
        solved = False
        while loops < max_loops and not solved:
            loops += 1
            # Split the safertext into words and reverse the order if desired
            words = self.__safertext().split()
            if reverse:
                words = reversed(words)
            # Loop over each word
            for word in words:
                # Look for potential matches
                matches = self.dictionary.find(word)
                # If the number of matches for this word is less we want
                if matches:
                    if len(matches) <= max_matches:
                        # Loop over each characters
                        for i in range(len(word)):
                            ok = ''
                            # If the character is uppercase...
                            if word[i].isupper():
                                # then this is a cipher character so...
                                # Loop over each potential match
                                for match in matches:
                                    if match[i].lower() in self.poss_keys[word[i]]:
                                        # add a possible solution character
                                        # to ok
                                        if match[i].lower() not in ok:
                                            ok += match[i].lower()
                                # Put the possible solutions back into the
                                # possible keys
                                self.poss_keys[word[i]] = ok
                for c in self.poss_keys:
                    if len(self.poss_keys[c]) == 1:
                        self.key[c] = self.poss_keys[c][0]

                # Check to see whether we have solved all keys
                solved = True
                for c in self.key:
                    if self.key[c] is None:
                        solved = False


def main():
    # Set up the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--infile",
                        help="ciphertext input file")
    parser.add_argument("-o",
                        "--outfile",
                        help="output file")
    parser.add_argument("-d",
                        "--dictionary",
                        default='dictionary.txt',
                        help="dictionary file")

    # Parse the commandline arguments
    args = parser.parse_args()

    outtext = ''
    ciphertext = ''

    # Read in the ciphertext`
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                ciphertext += line

    w = Wordsolve(dictionary=args.dictionary)
    w.ciphertext = ciphertext
    w.solve()
    outtext += w.plaintext + "\n"
    outtext += str(w.key) + "\n"
    outtext += str(w.poss_keys) + "\n"

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)

if __name__ == '__main__':
    main()
