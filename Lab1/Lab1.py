import sys

# Read input
operation = input().strip()  # "ENCODE" or "DECODE"
pseudo_random_number = int(input().strip())
rotors = [input().strip() for _ in range(3)]
message = input().strip()

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shift_char(c, shift):
    """Shift character c by shift positions in the alphabet."""
    idx = (alphabet.index(c) + shift) % 26
    return alphabet[idx]

def unshift_char(c, shift):
    """Reverse shift of character c."""
    idx = (alphabet.index(c) - shift) % 26
    return alphabet[idx]

def encode(message, rotors, start_shift):
    result = []
    shift = start_shift
    for ch in message:
        # Step 1: Caesar shift
        shifted = shift_char(ch, shift)

        # Step 2: Pass through rotors in order
        for rotor in rotors:
            shifted = rotor[alphabet.index(shifted)]

        result.append(shifted)

        # Increase shift for next letter
        shift += 1
    return "".join(result)

def decode(message, rotors, start_shift):
    result = []
    shift = start_shift
    for ch in message:
        # Step 1: Pass backwards through rotors
        shifted = ch
        for rotor in reversed(rotors):
            shifted = alphabet[rotor.index(shifted)]

        # Step 2: Undo Caesar shift
        shifted = unshift_char(shifted, shift)

        result.append(shifted)

        # Increase shift for next letter
        shift += 1
    return "".join(result)

# Perform the required operation
if operation == "ENCODE":
    print(encode(message, rotors, pseudo_random_number))
else:  # DECODE
    print(decode(message, rotors, pseudo_random_number))

