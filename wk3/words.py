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
    return code

class wc_dict
