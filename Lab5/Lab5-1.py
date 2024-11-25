def lcg(start_val, a, b, m, n):
    numbers = []
    x = start_val
    for _ in range(n):
        x = (a * x + b) % m
        numbers.append(x)
    return numbers


def encrypt(text, key):
    result = []
    for i, char in enumerate(text):
        encrypted_char = chr((ord(char) ^ (key[i] % 256)))
        result.append(encrypted_char)
    encrypted_text = ""
    for char in result:
        encrypted_text += char
    return encrypted_text

#############################################

text = input("Текст для шифрования: ")

start_val = 52525
a = 77777
b = 50777
n = len(text)
m = 2**n
        
key = lcg(start_val, a, b, m, n)

encrypted_text = encrypt(text, key)
print("Зашифрованный текст: ", encrypted_text)

decrypted_text = encrypt(encrypted_text, key)
print("Расшифрованный текст: ", decrypted_text)
