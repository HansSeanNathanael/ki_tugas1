import numpy as np
from scipy.stats import norm
import base64

# Run test counter
def count_runs(x):
    return np.sum(np.abs(np.diff(x)) == 1) + 1

# Run test script
def runs_test(x):
    n = len(x)
    n1 = np.sum(x)
    n2 = n - n1

    tau = 2.0 / np.sqrt(n)
    R = count_runs(x)
    R_exp = 2.0 * n1 * n2 / n + 1
    R_var = (2.0 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))

    z = (R - R_exp) / np.sqrt(R_var)

    # Menggunakan two-sided z-test
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
    # Ciphertext to binary
    binary_ciphertext = [int(b) for byte in base64.b64decode(ciphertext) for b in f"{byte:08b}"]

    # Test
    z, p = runs_test(binary_ciphertext)

    print(f"Runs test for {algorithm}:")
    print(f"Z-statistic: {z}")
    print(f"P-value: {p}")
    print()
