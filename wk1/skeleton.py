import sys
import argparse


def main():
    # Set up the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",
                        choices=["encrypt", "decrypt", "crack"],
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

    # Parse the commandline arguments
    args = parser.parse_args()

    intext = ''
    outtext = ''

    print("Mode: " + args.mode)
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                intext = intext + line
    if args.outfile is not None:
        print("Outfile: " + args.outfile)
    if args.key is None:
        if args.mode in ["encrypt", "decrypt"]:
            print("You must supply a key if you choose encrypt or decrypt "
                  "modes")
            sys.exit(2)
        print("Key: " + str(args.key))

    if args.mode == "encrypt":
        outtext = encrypt(args.key, intext)
    elif args.mode == "decrypt":
        outtext = decrypt(args.key, intext)
    else:
        outtext = crack(intext)

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


# Dummy encrypt
def encrypt(key, text):
    print("Encrypt: " + str(key) + " " + text)
    return text


# Dummy decrypt
def decrypt(key, text):
    print("Decrypt: " + str(key) + " " + text)
    return text


# Dummy crack
def crack(text):
    print("Crack: " + text)
    return text


if __name__ == '__main__':
    main()
