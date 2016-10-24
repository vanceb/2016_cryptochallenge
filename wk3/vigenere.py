import argparse
import sys

import frequency
import solve

ENCODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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

    # Create a substitution cipher solver
    vigenere = solve.Substitution()
    # Make an initial solution
    #outtext = vigenere.solve(ciphertext)
    vigenere.ciphertext = ciphertext
    outtext = vigenere.solve2()
    # Now we have a better idea of the likely words let's have a second go
    #outtext = vigenere.solve(outtext)
    outtext = vigenere.solve2()

    outtext += "\nCipher Freqs: " + str(cipher_freq)
    outtext += "\nKey: "
    outtext += str(vigenere.key)
    outtext += "\nSolve:\n"
    for c in vigenere.cipher_chars:
        outtext += c + ": " + str(vigenere.cipher_chars[c]) + "\n"
    outtext += "\n"
    vigenere.solve3()

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


if __name__ == '__main__':
    main()
