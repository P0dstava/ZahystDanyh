def encode(text: str) -> str:
    bits = ""
    for ch in text:
        # Convert to 8-bit binary
        binary = format(ord(ch), "08b")
        # Triple each bit
        for b in binary:
            bits += b * 3
    return bits


def decode(bits: str) -> str:
    corrected_bits = ""
    
    # Step 1: group into triplets
    for i in range(0, len(bits), 3):
        triplet = bits[i:i+3]
        # Step 2: majority vote (0 if more 0s, 1 if more 1s)
        corrected_bits += "1" if triplet.count("1") > triplet.count("0") else "0"
    
    # Step 3: regroup into 8-bit binary chunks
    text = ""
    for i in range(0, len(corrected_bits), 8):
        byte = corrected_bits[i:i+8]
        text += chr(int(byte, 2))  # binary → decimal → ASCII
    
    return text