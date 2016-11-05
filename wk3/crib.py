import argparse

import words

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

    # Parse the commandline arguments
    args = parser.parse_args()

    outtext = ''
    ciphertext = ''

    # Read in the ciphertext`
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                ciphertext += line

    crib = Crib()
    crib.load(args.crib)
    frequent_hits, hits = crib.search(stripciphertext(ciphertext))
    outtext += str(hits) + '\n'
    outtext += str(frequent_hits) + '\n'
    for cribword in frequent_hits:
        outtext += cribword + '\n'
        for match in frequent_hits[cribword]:
            score = frequent_hits[cribword][match]/len(hits[cribword])
            outtext += '\t' + match + ":\t " + str(score) + '\n'

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


if __name__ == '__main__':
    main()
