import solve

ciphertext = ''
with open('WK2_CIPHERTEXT2.txt', 'r') as f:
    for line in f:
        ciphertext += line

vigenere = solve.Substitution()
vigenere.ciphertext = ciphertext
#vigenere.solve()
#vigenere.solve3(most_matches=3)
vigenere.solve3(most_matches=1, reverse=True)

print(vigenere.plaintext + "\n")
print(str(vigenere.key) + "\n")
