import argparse

import words
import frequency
import key

ENCODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Crib:

    def __init__(self):
        self.cribwords = []

    def load(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                self.cribwords.append(line.strip())

    def search(self, text):
        hits = {}
        frequent_hits = {}
        for i in range(len(text)):
            for crib in self.cribwords:
                testword = text[i:i+len(crib)]
                cribcode = words.wordcode(crib)
                testcode = words.wordcode(testword)
                if cribcode == testcode:
                    if crib in hits:
                        if testword in hits[crib]:
                            # We have hit this sequence already
                            if crib in frequent_hits:
                                if testword in frequent_hits[crib]:
                                    frequent_hits[crib][testword] += 1
                                else:
                                    frequent_hits[crib] = {testword: 2}
                            else:
                                frequent_hits[crib] = {testword: 2}
                        hits[crib].append(testword)
                    else:
                        hits[crib] = [testword]
        return frequent_hits, hits


def stripciphertext(ciphertext):
    outtext = ''
    for c in ciphertext:
        if c in ENCODE_CHARS:
            outtext += c
    return outtext


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
    parser.add_argument("-c",
                        "--crib",
                        default='cribwords.txt',
                        help="cribwords file")
    parser.add_argument("-s",
                        "--stripciphertext",
                        action="store_true",
                        help="should we strip the ciphertext of spaces and"
                             "punctuation before we start to attempt decode")

    # Parse the commandline arguments
    args = parser.parse_args()

    outtext = ''
    ciphertext = ''

    # Read in the ciphertext`
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                ciphertext += line

    # Strip if requested
    if args.stripciphertext:
        ciphertext = stripciphertext(ciphertext)

    # Initialise the key
    k = key.Key()

    # Do the frequency analysis
    freq = frequency.frequency()
    freq.add(ciphertext)
    freqlist = freq.freq_list()
    print(str(freqlist))

    # Assume e is the most frequent and t is the second most frequent letters
    c, n = freqlist[0]
    k.set(c, 'e', 'Frequency')
    e = c
    c, n = freqlist[1]
    k.set(c, 't', "Frequency")
    t = c
    # Now we know 't' and 'e', try to find the h from 'the'
    c, n = freq.h_spotter(t, e, ciphertext)
    k.set(c, 'h', 'h spotter')

    # get the partially decrypted ciphertext
    pd = k.decipher(ciphertext)

    # Use the cribs to try and get a start on the cracking
    crib = Crib()
    crib.load(args.crib)
    frequent_hits, hits = crib.search(ciphertext)

    for cribword in frequent_hits:
        for match in frequent_hits[cribword]:
            score = frequent_hits[cribword][match] / len(hits[cribword])
            if score > 0.1:
                k.set_string(match, cribword, "Cribword: " + cribword)

    outtext += str(hits) + '\n'
    outtext += str(frequent_hits) + '\n'
    for cribword in frequent_hits:
        outtext += cribword + '\n'
        for match in frequent_hits[cribword]:
            score = frequent_hits[cribword][match]/len(hits[cribword])
            outtext += '\t' + match + ":\t " + str(score) + '\n'
    outtext += '\n\n' + k.decipher(ciphertext) + '\n\n'
    outtext += '\n' + str(k.key) + '\n'
    outtext += '\n' + str(k.history) + '\n'

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


if __name__ == '__main__':
    main()
