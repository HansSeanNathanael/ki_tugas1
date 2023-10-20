import numpy as np
from scipy.stats import entropy

# Hardcoded plaintext and corresponding ciphertexts for various algorithms
plaintext = "3519082204010001"
ciphertexts = {
    "AESCBC": "v6GVMPOWUT9Sy5uA7ar8Z1lDcJwhNpDlUXUFBKGrsZ70UOw0BJIhGxpIbFN6g1g9",
    # ... [other cipher texts]
}

def calc_freq(text):
    """
    Calculate the frequency of each character in a given text.

    Args:
    - text (str): The input string.

    Returns:
    - prob_array (np.array): An array of probabilities corresponding to the frequency of each character.
    """
    
    # Initialize a dictionary to store the frequency of each character
    freq_dict = {}
    for char in text:
        freq_dict[char] = freq_dict.get(char, 0) + 1  # Update the count of each character

    # Convert the dictionary values to a numpy array
    freq_array = np.array(list(freq_dict.values()), dtype=float)
    
    # Normalize the frequencies to compute probabilities
    prob_array = freq_array / np.sum(freq_array)
    
    return prob_array

# Compute entropy of the plaintext using the Shannon entropy formula
H_plain = entropy(calc_freq(plaintext), base=2)
L_plain = len(plaintext)

# Display the entropy and length of the plaintext
print(f"The entropy of the plaintext is {H_plain:.2f} bits, with the length of string being {L_plain} characters.")

# Compute and display the entropy for each ciphertext in the dictionary
for algorithm, ciphertext in ciphertexts.items():
    H_cipher = entropy(calc_freq(ciphertext), base=2)
    L_cipher = len(ciphertext)
    print(f"The entropy of the ciphertext for {algorithm} is {H_cipher:.2f} bits, with the length of the string being {L_cipher} characters.")
