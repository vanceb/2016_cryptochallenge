import re


def wordcode(word):
    words = word.split(" ")
    if len(words) > 1:
        raise Exception("Too many words passed in")
    word = words[0].strip()
    code = []
    letters_seen = {}
    next_letter = 1
    for c in word:
        if c not in letters_seen:
            letters_seen[c] = next_letter
            next_letter += 1
        code.append(letters_seen[c])
    return tuple(code)


class word_pattern:
    def __init__(self):
        self.words = []
        self.wc = None

    def add(self, word):
        word = word.upper()
        code = wordcode(word)
        # Check to see that the word we are adding has the same code as others
        if self.wc is None:
            self.wc = code
        elif self.wc != code:
            raise Exception("Error, attempt to mix word codes")
        self.words.append(word)

    def find(self, pattern):
        pattern = pattern.upper()
        regex = re.compile(pattern)
        hits = []
        for word in self.words:
            hit = regex.match(word)
            if hit:
                hits.append(hit.group(0))
        return hits

    # Generate a regex pattern where uppercase characters can match anything
    # lowercase characters are taken as literal characters
    def codematch(self, code):
        pattern = ''
        for c in code:
            if c.isupper():
                pattern += '.'
            else:
                pattern += c.upper()
        return pattern


class wp_dict:
    def __init__(self):
        self.wordcodes = {}

    def add(self, word):
        code = wordcode(word.upper())
        if code not in self.wordcodes:
            wc = word_pattern()
            self.wordcodes[code] = wc
        self.wordcodes[code].add(word)

    # Finds potentially matching words for a code.
    # Upper case characters are allowed to match anything.
    # lower case characters are taken as literals and must match exactly
    # e.g. 'CEllO' would match 'hello'
    # This allows us to replace code characters with lower case once
    # we have identified a match
    def find(self, code):
        wc = wordcode(code)
        if wc in self.wordcodes:
            pattern = self.wordcodes[wc].codematch(code)
            hits = self.wordcodes[wc].find(pattern)
            codehits = []
            for hit in hits:
                hitcode = wordcode(hit)
                if hitcode == wc:
                    codehits.append(hit)
            return codehits
        else:
            return None

    def load(self, dictionary='dictionary.txt'):
        with open(dictionary, 'r') as f:
            for line in f:
                for word in line.split():
                    self.add(word.strip())


def main():
    print("This is a library, do not call directly")

if __name__ == '__main__':
    main()
