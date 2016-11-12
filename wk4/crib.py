import argparse
import re

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

    # Search for cribwords in text using wordcode only
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

    # Search for cribwords in text using both codeword patterns and
    # wordcodes.  Allows search across partially decoded ciphertext
    # with CIPHERTEXT as uppercase and plaintext as lowercase
    # Exact matches against the plaintext parts and any character match
    # against the uppercase CIPHERTEXT
    def search2(self, text):
        hits = {}
        frequent_hits = {}
        for i in range(len(text)):
            for crib in self.cribwords:
                testword = text[i:i+len(crib)]
                test_pattern = words.codematch(testword).lower()
                test_matcher = re.compile(test_pattern)
                if test_matcher.fullmatch(crib):
                    if words.wordcode(testword) == words.wordcode(crib):
                        if crib in hits:
                            if testword in hits[crib]:
                                # We have hit this sequence already
                                if crib in frequent_hits:
                                    if testword in frequent_hits[crib]:
                                        frequent_hits[crib][testword] += 1
                                    else:
                                        frequent_hits[crib][testword] = 2
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
                        required=True,
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
    frequent_hits, hits = crib.search2(ciphertext)

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


def help():
    print('key, freq, history, crib, quit')


def main2():
    # Set up the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--infile",
                        required=True,
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
    parser.add_argument("-r",
                        "--reverse",
                        action="store_true",
                        help="Reverse the ciphertext before decryption")
    parser.add_argument("-s",
                        "--stripciphertext",
                        action="store_true",
                        help="should we strip the ciphertext of spaces and"
                             "punctuation before we start to attempt decode")
    parser.add_argument("-t",
                        "--cribthreshold",
                        default=0.1,
                        help="Thresholds for us to use the cribwords",
                        type=float)

    # Parse the commandline arguments
    args = parser.parse_args()

    outtext = ''
    ciphertext = ''

    # Read in the ciphertext`
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                ciphertext += line

    # Reverse the ciphertext if wanted
    if args.reverse:
        ciphertext = ciphertext[::-1]

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
    #c, n = freqlist[0]
    #k.set(c, 'e', 'Frequency')
    #e = c
    #c, n = freqlist[1]
    #k.set(c, 't', "Frequency")
    #t = c
    # Now we know 't' and 'e', try to find the h from 'the'
    #c, n = freq.h_spotter(t, e, ciphertext)
    #k.set(c, 'h', 'h spotter')

    # Use the cribs to try and get a start on the cracking
    crib = Crib()
    crib.load(args.crib)
    frequent_hits, hits = crib.search2(ciphertext)

    for cribword in frequent_hits:
        for match in frequent_hits[cribword]:
            score = frequent_hits[cribword][match] / len(hits[cribword])
            if score > args.cribthreshold:
                k.set_string(match, cribword, "Cribword: " + cribword)

    # get the partially decrypted ciphertext
    print(k.decipher(ciphertext))

    # put the loop in a try block so that if we hit an Exception
    # we will save the state of the key and ciphertext...
    try:
        # Start an interactive loops
        while True:
            cmd = input("\n:> ")
            # Check to see whether we entered an integer
            try:
                # If so then lets use it to
                # go back in time...
                i = int(cmd)
                k.history = i
            except:
                if len(cmd) == 1:
                    if cmd.upper() in ENCODE_CHARS:
                        p = input("Plaintext :> ")
                        k.set(cmd, p, 'User')
                    elif cmd == '?':
                        help()
                elif cmd == 'key':
                    print('\n' + str(k.key) + '\n')
                elif cmd == 'freq':
                    print(str(freqlist))
                elif cmd == 'quit':
                    break
                elif cmd == 'history':
                    print(k.history)
                elif cmd == 'crib':
                    frequent_hits, hits = crib.search2(k.decipher(ciphertext))
                    print('\n' + str(hits))
                    print('\n' + str(frequent_hits))
                elif cmd == 'help':
                    help()
            print('\n' + k.decipher(ciphertext))
    finally:

        outtext = ''
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
    main2()
