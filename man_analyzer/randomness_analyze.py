import numpy as np
from scipy.stats import norm

# Run test counter for strings
def count_runs(s):
    runs = 1  # start with 1 to account for the first character
    for i in range(1, len(s)):
        if s[i] != s[i-1]:
            runs += 1
    return runs

# Run test script for strings
def runs_test(s):
    n = len(s)
    unique_chars = set(s)
    if len(unique_chars) != 2:
        raise ValueError("The input string must contain exactly 2 unique characters for the runs test.")
    
    char1, char2 = unique_chars
    n1 = s.count(char1)
    n2 = n - n1

    R = count_runs(s)
    R_exp = 2.0 * n1 * n2 / n + 1
    R_var = (2.0 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))

    z = (R - R_exp) / np.sqrt(R_var)

    # Using two-sided z-test
    return z, 2 * (1 - norm.cdf(abs(z)))

# Data
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

# Tests
for algorithm, ciphertext in ciphertexts.items():
    try:
        z, p = runs_test(ciphertext)
        print(f"Runs test for {algorithm}:")
        print(f"Z-statistic: {z}")
        print(f"P-value: {p}")
        print()
    except ValueError as e:
        print(f"Error for {algorithm}: {e}")
