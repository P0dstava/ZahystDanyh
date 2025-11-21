import string
from collections import Counter

# English frequencies (uppercase assumed, sum = 100%)
english_freq = {
    'A': 8.08, 'B': 1.67, 'C': 3.18, 'D': 3.99, 'E': 12.56, 'F': 2.17,
    'G': 1.80, 'H': 5.27, 'I': 7.24, 'J': 0.14, 'K': 0.63, 'L': 4.04,
    'M': 2.60, 'N': 7.38, 'O': 7.47, 'P': 1.91, 'Q': 0.09, 'R': 6.42,
    'S': 6.59, 'T': 9.15, 'U': 2.79, 'V': 1.00, 'W': 1.89, 'X': 0.21,
    'Y': 1.65, 'Z': 0.07
}

def shift_char(c, shift):
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - base - shift) % 26 + base)
    return c

def decode_with_shift(text, shift):
    return ''.join(shift_char(c, shift) for c in text)

def chi_squared_stat(text):
    # Count only letters
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters)
    if total == 0:
        return float('inf')
    observed = Counter(letters)
    chi2 = 0
    for letter, exp_freq in english_freq.items():
        observed_count = observed.get(letter, 0)
        expected_count = total * (exp_freq / 100)
        chi2 += (observed_count - expected_count) ** 2 / (expected_count + 1e-9)
    return chi2

def auto_decode(text):
    best_shift = min(range(26), key=lambda s: chi_squared_stat(decode_with_shift(text, s)))
    return decode_with_shift(text, best_shift)

# Example usage
ciphertext = input().rstrip("\n")
print(auto_decode(ciphertext))
