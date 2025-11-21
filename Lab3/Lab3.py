def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)

def xor_bytes(*args):
    result = bytearray(args[0])  # start with the first
    for b in args[1:]:
        for i in range(len(result)):
            result[i] ^= b[i]
    return bytes(result)

# Read inputs
m1 = hex_to_bytes(input().strip())
m2 = hex_to_bytes(input().strip())
m3 = hex_to_bytes(input().strip())

# XOR them all together
plain = xor_bytes(m1, m2, m3)

# Convert to ASCII text
print(plain.decode("ascii"))
