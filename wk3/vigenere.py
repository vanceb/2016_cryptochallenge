import argparse
import sys

import frequency
import words

ENCODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEY = {
       'A': None,
       'B': None,
       'C': None,
       'D': None,
       'E': None,
       'F': None,
       'G': None,
       'H': None,
       'I': None,
       'J': None,
       'K': None,
       'L': None,
       'M': None,
       'N': None,
       'O': None,
       'P': None,
       'Q': None,
       'R': None,
       'S': None,
       'T': None,
       'U': None,
       'V': None,
       'W': None,
       'X': None,
       'Y': None,
       'Z': None
       }

def main():
    # Set up the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--infile",
                        help="ciphertext input file")
    parser.add_argument("-o",
                        "--outfile",
                        help="output file")
    parser.add_argument("-t",
                        "--training",
                        help="training file")
    parser.add_argument("-d",
                        "--dictionary",
                        default='dictionary.txt',
                        help="dictionary file")
    parser.add_argument('-n',
                        "--norm",
                        type=int,
                        default=0,
                        help="Normalise frequencies to...  0=don't normalise")
    parser.add_argument('-c',
                        '--caseinsensitive',
                        default=True,
                        action='store_true')

    # Parse the commandline arguments
    args = parser.parse_args()

    outtext = ''

    freqs = frequency.frequency(caseinsensitive=args.caseinsensitive)
    ciphertext = ''

    # Read in the ciphertext`
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                ciphertext += line
        freqs.add(ciphertext)
        cipher_freq = freqs.chars()
    else:
        sys.exit(2)

    # Read in the dictionaryfile
    dictionary = words.wp_dict()
    dictionary.load(dictionaryfile=args.dictionary)

    # Assume that the highest freq is the letter 'e'
    e_char = cipher_freq[0]
    KEY[e_char] = 'e'

    # Try to solve the ciphertext...
    # Create all possibilities, which we wil knock out...
    cipher_chars = {}
    for c in ENCODE_CHARS:
        cipher_chars[c] = ENCODE_CHARS

    for word in ciphertext.split():
        pos_matches = dictionary.find(word)
        if pos_matches:
            word_chars = {}
            for i in range(len(word)):
                if word[i] not in word_chars:
                    word_chars[word[i]] = {}
                for match in pos_matches:
                        word_chars[word[i]][match[i]] = 1
            for c in word_chars:
                if c in ENCODE_CHARS:
                    ok = ''
                    for letter in cipher_chars[c]:
                        if letter in word_chars[c]:
                            ok += letter
                    cipher_chars[c] = ok

    # Where we have solved a particular cypher letter let's add it to the Key
    for c in cipher_chars:
        if len(cipher_chars[c]) == 1:
            KEY[c] = cipher_chars[c]

    # Have a second round of elimination
    # If the letter is in the key then let's remove it as a possibile
    solved_letters = ''
    for cc in KEY:
        if KEY[cc]:
            solved_letters += KEY[cc]
    for c in cipher_chars:
        if len(cipher_chars[c]) > 1:
            ok = ''
            for d in cipher_chars[c]:
                if d not in solved_letters:
                    ok += d
            cipher_chars[c] = ok

    # Convert the ciphertext into the plaintext (or mix)
    for c in ciphertext:
        if c in ENCODE_CHARS:
            if KEY[c]:
                outtext += KEY[c].lower()
            else:
                outtext += c
        else:
            outtext += c

    outtext += "\nCipher Freqs: " + str(cipher_freq)
    outtext += "\nKey: "
    for c in ENCODE_CHARS:
        outtext += c + ": " + str(KEY[c]) + ", "
    outtext += "\nSolve:\n"
    for c in cipher_chars:
        outtext += c + ": " + str(cipher_chars[c]) + "\n"

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


if __name__ == '__main__':
    main()
