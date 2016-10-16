import operator
import sys
import argparse


disallowed_chars = ' '


def char_freq(text, sort='freq', ignore=disallowed_chars):
    freq = {}
    for c in text.upper():
        if c not in ignore:
            if c in freq:
                freq[c] = freq[c] + 1
            else:
                freq[c] = 1
    return norm_freq(freq, sort=sort)


def plot_freq(freq):
    max_freq = 0
    for c, f in freq:
        if f > max_freq:
            max_freq = f
    for i in range(max_freq, 0, -1):
        line = ''
        for c, f in freq:
            if f >= i:
                line = line + c
            else:
                line = line + ' '
        print(line)


def norm_freq(freq, norm_to=20, sort="freq"):
    max_freq = 0

    for c in freq:
        if freq[c] > max_freq:
            max_freq = freq[c]

    if sort == "freq":
        # Sort by the frequency
        sorted_list = sorted(freq.items(),
                             key=operator.itemgetter(1),
                             reverse=True)
    else:
        # Sort by the character
        sorted_list = sorted(freq.items(),
                             key=operator.itemgetter(0),
                             reverse=True)

    norm = []
    for c, f in sorted_list:
        norm.append((c, f * norm_to // max_freq))
    return norm


def main():
    # Set up the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",
                        choices=["char", "hist"],
                        help="Mode for the program")
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
    if args.mode == "char":
        outtext = str(char_freq(intext))
    elif args.mode == "hist":
        outtext = plot_freq(char_freq(intext))

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


if __name__ == '__main__':
    main()
