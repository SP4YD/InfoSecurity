S_BOX = [
    (12, 4, 6, 2, 10, 1, 8, 5, 11, 14, 9, 7, 3, 15, 13, 0),
    (8, 2, 5, 12, 9, 6, 10, 1, 4, 13, 15, 14, 3, 7, 0, 11),
    (7, 10, 0, 12, 2, 8, 13, 6, 1, 15, 4, 9, 11, 3, 14, 5),
    (10, 9, 0, 7, 2, 12, 4, 6, 1, 8, 13, 15, 3, 11, 5, 14),
    (15, 3, 8, 12, 0, 6, 9, 5, 2, 10, 1, 14, 7, 11, 4, 13),
    (9, 15, 7, 4, 11, 10, 5, 3, 14, 8, 0, 12, 13, 2, 1, 6),
    (3, 12, 13, 1, 2, 8, 9, 15, 6, 14, 5, 4, 11, 7, 0, 10),
    (14, 11, 4, 3, 1, 5, 10, 9, 7, 0, 13, 8, 2, 15, 6, 12),
]

def padding_data(data):
    pad_len = 8 - len(data) % 8
    return data + bytes([pad_len] * pad_len)

def unpadding_data(data):
    pad_len = data[-1]
    return data[:-pad_len]

def generate_subkeys(key):
    return [(key >> (32 * i)) & 0xFFFFFFFF for i in range(8)]

def round_function(part, key):
    temp = part ^ key
    output = 0

    for i in range(8):
        nibble = (temp >> (4 * i)) & 0xF
        output |= (S_BOX[i][nibble] << (4 * i))

    return ((output >> 11) | (output << (32 - 11))) & 0xFFFFFFFF

def encrypt_block(plaintext, subkeys):
    left = plaintext >> 32
    right = plaintext & 0xFFFFFFFF

    for i in range(24):
        tmp = right
        right = left ^ round_function(right, subkeys[i % 8])
        left = tmp

    for i in range(8):
        tmp = right
        right = left ^ round_function(right, subkeys[7 - i])
        left = tmp

    return (left << 32) | right

def decrypt_block(ciphertext, subkeys):
    left = ciphertext >> 32
    right = ciphertext & 0xFFFFFFFF

    for i in range(8):
        tmp = left
        left = right ^ round_function(left, subkeys[i])
        right = tmp

    for i in range(24):
        tmp = left
        left = right ^ round_function(left, subkeys[(7 - i) % 8])
        right = tmp

    return (left << 32) | right

def encrypt(data, subkeys):
    data = padding_data(data)
    blocks = [data[i:i+8] for i in range(0, len(data), 8)]
    encrypted_data = b''

    for block in blocks:
        block_int = int.from_bytes(block, 'big')
        encrypted_block = encrypt_block(block_int, subkeys)
        encrypted_data += encrypted_block.to_bytes(8, 'big')

    return encrypted_data

def decrypt(data, subkeys):
    blocks = [data[i:i+8] for i in range(0, len(data), 8)]
    decrypted_data = b''

    for block in blocks:
        block_int = int.from_bytes(block, 'big')
        decrypted_block = decrypt_block(block_int, subkeys)
        decrypted_data += decrypted_block.to_bytes(8, 'big')

    return unpadding_data(decrypted_data)

############################################################

key = 0x1234567890ABCDEF1234567890ABCDEF9876543210FEDCBA9876543210FEDCBA
subkeys = generate_subkeys(key)

input_file = "input.txt"
encrypted_file = "encrypted.txt"
decrypted_file = "decrypted.txt"

with open(input_file, 'rb') as f:
    data = f.read()
    print("input:", data)

with open(encrypted_file, 'wb') as f:
    encrypted_data = encrypt(data, subkeys)
    f.write(encrypted_data)
    print("encrypted:", encrypted_data)

with open(decrypted_file, 'wb') as f:
    decrypted_data = decrypt(encrypted_data, subkeys)
    f.write(decrypted_data)
    print("decrypted:", decrypted_data)
