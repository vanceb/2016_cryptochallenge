import operator
import argparse

ENCODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class frequency:
    def __init__(self, caseinsensitive=True):
        self.caseinsensitive = caseinsensitive
        self.freq = {}

    def add_key(self, key):
        if self.caseinsensitive:
            key = key.upper()
        if key in ENCODE_CHARS:
            if key in self.freq:
                self.freq[key] += 1
            else:
                self.freq[key] = 1

    def freq_dict(self):
        return self.freq

    def add(self, text):
        for c in text:
            self.add_key(c)

    def freq_list(self, norm_to=50, caseinsensitive=True, sort='freq'):
        max_freq = 0

        for c in self.freq:
            if self.freq[c] > max_freq:
                max_freq = self.freq[c]

        if sort == 'freq':
            # Sort by the frequency
            sorted_list = sorted(self.freq.items(),
                                 key=operator.itemgetter(1),
                                 reverse=True)
        else:
            # Sort by the character
            sorted_list = sorted(self.freq.items(),
                                 key=operator.itemgetter(0),
                                 reverse=True)

        norm = []
        for c, f in sorted_list:
            if norm_to == 0:
                norm.append((c, f))
            else:
                norm.append((c, f * norm_to // max_freq))
        return norm

    def chars(self):
        characters = []
        freqs = self.freq_list()
        for c, f in freqs:
            characters.append(c)
        return characters

    def h_spotter(self, t, e, text):
        length = len(text)
        h = {}
        for i in range(length):
            if i < length - 2:
                if text[i] == t and text[i+2] == e:
                    poss_h = text[i+1]
                    if poss_h in h:
                        h[poss_h] += 1
                    else:
                        h[poss_h] = 1
        sorted_list = sorted(h.items(),
                             key=operator.itemgetter(1),
                             reverse=True)
        return sorted_list[0]

    def plot_freq(self, norm_to=50):
        fl = self.freq_list(norm_to=norm_to)
        outtext = ''
        max_freq = 0
        for c, f in fl:
            if f > max_freq:
                max_freq = f
        for i in range(max_freq, 0, -1):
            line = ''
            for c, f in fl:
                if f >= i:
                    line = line + c
                else:
                    line = line + ' '
            outtext += line + '\n'
        return outtext


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
    parser.add_argument('-n',
                        "--norm",
                        type=int,
                        default=0,
                        help="Normalise frequencies to...  0 = don't normalise")
    parser.add_argument('-c',
                        '--caseinsensitive',
                        default=True,
                        action='store_true')

    # Parse the commandline arguments
    args = parser.parse_args()

    intext = ''
    outtext = ''

    freq = frequency(caseinsensitive = args.caseinsensitive)

    print("Mode: " + args.mode)
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                intext = intext + line
        freq.add(intext)
    if args.outfile is not None:
        print("Outfile: " + args.outfile)
    if args.mode == "char":
        outtext = str(freq.freq_list(norm_to=args.norm))
    elif args.mode == "hist":
        outtext = freq.plot_freq(norm_to=args.norm)

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


if __name__ == '__main__':
    main()
