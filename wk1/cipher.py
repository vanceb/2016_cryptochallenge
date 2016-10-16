import sys
import argparse

import isEnglish


def main():
    # Set up the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",
                        choices=["encrypt", "decrypt", "crack", "jamelia"],
                        help="Mode for the program")
    parser.add_argument("-k",
                        "--key",
                        type=int,
                        help="Provide an integer as a key")
    parser.add_argument("-i",
                        "--infile",
                        help="input file")
    parser.add_argument("-o",
                        "--outfile",
                        help="output file")
    parser.add_argument("-r",
                        "--reversed",
                        action="store_true",
                        help="reverse the input text")
    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="More verbose output")


    # Parse the commandline arguments
    args = parser.parse_args()

    intext = ''
    outtext = ''

    print("Mode: " + args.mode)
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                intext = intext + line
        if args.reversed:
            intext = intext[::-1]

    if args.outfile is not None:
        print("Outfile: " + args.outfile)
    if args.key is None:
        if args.mode in ["encrypt", "decrypt"]:
            print("You must supply a key if you choose encrypt or decrypt "
                  "modes")
            sys.exit(2)
        print("Key: " + str(args.key))

    if args.verbose:
        verbose = True
    else:
        verbose = False

    if args.mode == "encrypt":
        outtext = encrypt(args.key, intext)
    elif args.mode == "decrypt":
        outtext = decrypt(args.key, intext)
    elif args.mode == "jamelia":
        possibilities = crack_jamelia(intext, verbose)
        if len(possibilities) > 0:
            for key in possibilities:
                print()
                print("Key: " + str(key))
                print(possibilities[key])
        else:
            print("Unable to crack...")
    else:
        possibilities = crack(intext, verbose)
        if len(possibilities) > 0:
            for key in possibilities:
                print()
                print("Key: " + str(key))
                print(possibilities[key])
        else:
            print("Unable to crack...")

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


# Caesar cipher
codeset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
r_codeset = codeset[::-1]


def caesar(key, text):
    outtext = ''
    for c in text.upper():
        if c in codeset:
            pos = codeset.index(c)
            outtext = outtext + codeset[(pos + key) % len(codeset)]
        else:
            outtext = outtext + c
    return outtext


def jamelia(key, text):
    outtext = ''
    lettersonly = ''
    for c in text.upper():
        if c in letters:
            pos = codeset.index(c)
            lettersonly = lettersonly + codeset[(pos + key) % len(codeset)]
    # reverse the letters
    lettersonly = lettersonly[::-1]
    i = 0
    for c in text.upper():
        if c in letters:
            outtext = outtext + lettersonly[i]
            i = i + 1
        else:
            outtext = outtext + c
    return outtext


def crack_jamelia(text, verbose=False):
    possibilities = {}
    for i in range(len(codeset)):
        outtext = jamelia(i, text)
        if verbose:
            print()
            print(i)
            print(outtext)

        if isEnglish.isEnglish(outtext):
            possibilities[i] = outtext
    return possibilities


# Dummy encrypt
def encrypt(key, text):
    return caesar(key, text)


# Dummy decrypt
def decrypt(key, text):
    return caesar((len(codeset) - key) % len(codeset), text)


# Dummy crack
def crack(text, verbose=False):
    possibilities = {}
    for i in range(len(codeset)):
        outtext = decrypt(i, text)
        if verbose:
            print()
            print(i)
            print(outtext)

        if isEnglish.isEnglish(outtext):
            possibilities[i] = outtext
    return possibilities


if __name__ == '__main__':
    main()
