from scipy.stats import entropy
import numpy as np

# Your hardcoded plaintext and ciphertext
plaintext = "3519082204010001"
ciphertexts = {
    "AESCBC": "v6GVMPOWUT9Sy5uA7ar8Z1lDcJwhNpDlUXUFBKGrsZ70UOw0BJIhGxpIbFN6g1g9",
    "AESCFB": "wstgjEW5WK2Hzofd27hgroNDWYSyddiFCTMoq1wbfLUg3vOms5Ts0F2QqnNOtadZ",
    "AESOFB": "wstgjEW5WK2g2d1wwCyOQnjyWbTn7GfZ8gLv9bQ1PqgMb7JJK9DNOJy0GnaYYjcN",
    "AESCTR": "smZFS2U9G4Cjc7Vb10wEKg==",
    "DESCBC": "8BEwmkw+tRLTYSvyBGDrc7U1YbfGzXbcfCT9JU69eBQ=",
    "DESCFB": "nouE3JSGuc1aPH6T1+Yw03z3EaDAWAjAAj/uA4L4jwA=",
    "DESOFB": "niVw4b3o54kg1FYVBbYed7c0rMTg76F1BZmbzCoFkrU=",
    "DESCTR": "hhGDIUo/eoCcAA9Z99mUJQ==",
    "CR4": "JQn7wIFOBU0ZtjHlipcZCQ=="
}

# Function to calculate frequency of characters
def calc_freq(text):
    # Initialize a dictionary to hold character frequencies
    freq_dict = {}
    for char in text:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1

    # Convert the dictionary values to a numpy array
    freq_array = np.array(list(freq_dict.values()), dtype=float)
    
    # Normalize the frequencies to get probabilities
    prob_array = freq_array / np.sum(freq_array)
    
    return prob_array

H_plain = entropy(calc_freq(plaintext), base=2)
L_plain = len(plaintext)


print(f"The entropy of the ciphertext is {H_plain} bits, with the lenght of string is {L_plain}")

# Calculate the entropy for each ciphertext in the dictionary
for algorithm, ciphertext in ciphertexts.items():
    H_cipher = entropy(calc_freq(ciphertext), base=2)
    L_cipher = len(ciphertext)
    print(f"The entropy of the ciphertext for {algorithm} is {H_cipher} bits, with the length of the string is {L_cipher}")
