import operator
import argparse


class frequency:
    def __init__(self):
        self.freq = {}

    def add_key(self, key):
        if key in self.freq:
            self.freq[key] += 1
        else:
            self.freq[key] = 1

    def freq_dict(self):
        return self.freq

    def add(self, text):
        for c in text:
            self.add_key(c)

    def freq_list(self, norm_to=50, sort='freq'):
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
            norm.append((c, f * norm_to // max_freq))
        return norm

    def plot_freq(self):
        fl = self.freq_list()
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

    # Parse the commandline arguments
    args = parser.parse_args()

    intext = ''
    outtext = ''

    freq = frequency()

    print("Mode: " + args.mode)
    if args.infile is not None:
        with open(args.infile, 'r') as f:
            for line in f:
                intext = intext + line
        freq.add(intext)
    if args.outfile is not None:
        print("Outfile: " + args.outfile)
    if args.mode == "char":
        outtext = str(freq.freq_list())
    elif args.mode == "hist":
        outtext = freq.plot_freq()

    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            f.write(outtext)
    else:
        print(outtext)


if __name__ == '__main__':
    main()
