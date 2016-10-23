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
    def __init__(self, caseinsensitive=True):
        self.words = []
        self.wc = None
        self.caseinsensitive = caseinsensitive

    def add(self, word):
        if self.caseinsensitive:
            word = word.upper()
        code = wordcode(word)
        # Check to see that the word we are adding has the same code as others
        if self.wc is None:
            self.wc = code
        elif self.wc != code:
            raise Exception("Error, attempt to mix word codes")
        self.words.append(word)

    def find(self, pattern):
        if self.caseinsensitive:
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
                pattern += c
        return pattern


class wp_dict:
    def __init__(self, caseinsensitive=True):
        self.wordcodes = {}
        self.caseinsensitive = caseinsensitive

    def add(self, word):
        if self.caseinsensitive:
            word = word.upper()
        code = wordcode(word)
        if code not in self.wordcodes:
            wc = word_pattern(caseinsensitive=self.caseinsensitive)
            self.wordcodes[code] = wc
        self.wordcodes[code].add(word)

    # Finds potentially matching words for a code.
    # Upper case characters are allowed to match anything.
    # lower case characters are taken as literals and must match exactly
    # e.g. 'CEllO' would match 'hello'
    # This allows us to replace code characters with lower case once
    # we have identified a match
    def find(self, code):
        if self.caseinsensitive:
            wc = wordcode(code.upper())
        else:
            wc = wordcode(code)
        if wc in self.wordcodes:
            pattern = self.wordcodes[wc].codematch(code)
            hits = self.wordcodes[wc].find(pattern)
            codehits = []
            # We want upper and lower chase character in the code
            # to be treated as different characters for this part
            # of the matching process, so get a new code that
            # is case sensitive
            wc = wordcode(code)
            for hit in hits:
                hitcode = wordcode(hit)
                if hitcode == wc:
                    codehits.append(hit)
            return codehits
        else:
            return None

    def load(self, dictionaryfile='dictionary.txt'):
        with open(dictionaryfile, 'r') as f:
            for line in f:
                for word in line.split():
                    self.add(word.strip())


def main():
    print("This is a library, do not call directly")

if __name__ == '__main__':
    main()
