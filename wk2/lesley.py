import argparse
import sys

import frequency

ENCODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEY = {'O': 'I', 'Z': 'T', 'C': 'W', 'K': 'E', 'N': 'H', 'X': 'R', 'G': 'A', 'U': 'O', 'Y': 'S', 'J': 'D', 'T': 'N', 'B': 'V', 'S': 'M', 'R': 'L', 'L': 'F', 'E': 'Y', 'I': 'C', 'A': 'U', 'Q': 'K', 'V': 'P', 'H': 'B', 'M': 'G', 'D': 'X', 'P': 'J', 'W': 'Q'}

def main():
    # Set up the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--infile",
                        help="input file")
    parser.add_argument("-o",
                        "--outfile",
                        help="output file")
    parser.add_argument("-t",
                        "--training",
                        help="training file")
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

    intext = ''
    outtext = ''

    training = frequency.frequency(caseinsensitive=args.caseinsensitive)
    ciphertext = frequency.frequency(caseinsensitive=args.caseinsensitive)

    if args.training is not None:
        with open(args.training, 'r') as f:
            for line in f:
                intext = intext + line
        training.add(intext)

    intext = ''
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                intext = intext + line
        ciphertext.add(intext)
    else:
        sys.exit(2)

    train_freq = training.chars()
    cipher_freq = ciphertext.chars()

    for c in intext:
        if c in KEY:
            outtext += KEY[c].lower()
        else:
            outtext += c

    outtext += "\nKey: " + str(KEY)

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


if __name__ == '__main__':
    main()
