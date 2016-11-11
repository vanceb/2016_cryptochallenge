import argparse

ENCODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


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
    parser.add_argument("-m",
                        "--modulus",
                        type=int,
                        help="Modulus key - pick every xth bit",
                        )

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

    outtext = ''
    for i in range(len(ciphertext)):
        j = (i * args.modulus) % len(ciphertext)
        outtext += ciphertext[j]

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)

if __name__ == '__main__':
    main()
