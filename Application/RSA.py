# %%
import random
import math
from typing import List
import sys
sys.setrecursionlimit(1500)

# %%
def convert_to_num(char: str) -> int:
    if char.isdigit():
        return int(char)
    elif char.isalpha():
        return ord(char.lower()) - 87
    else:
        return 36

def convert_to_char(num: int) -> str:
    if 0 <= num <= 9:
        return str(num)
    elif 10 <= num <= 35:
        return chr(num + 87)
    else:
        return ' '

def encode_message(msg: str) -> int:
    # Convert any extra characters to spaces
    msg = ''.join([c if c.isalnum() else ' ' for c in msg])

    # Pad the message with spaces to make sure it's divisible by 5
    msg += ' ' * (5 - len(msg) % 5) * (len(msg) % 5 != 0)

    # Split the message into groups of 5 characters
    groups = [msg[i:i+5] for i in range(0, len(msg), 5)]

    # Convert each group into a number using the specified formula
    nums = []
    for group in groups:
        num = 0
        for i, c in enumerate(group):
            num += convert_to_num(c) * (37 ** (4-i))
        nums.append(num)
    # Combine the numbers into a single integer by concatenating digits
    result = int(''.join([str(n) for n in nums]))
    return result

def decode_message(num: int) -> str:
    num_str = str(num).zfill((len(str(num)) + 7) // 8 * 8)

    # split into 8-character chunks and convert back to integers
    groups = [int(num_str[i:i+8]) for i in range(0, len(num_str), 8)]

    # Convert each group back into a string of 5 characters using mod and div
    msg = ''
    for group in groups:
        group_str = ''
        for i in range(5):
            c = convert_to_char(group // (37 ** (4-i))) 
            group_str += c
            group %= 37 ** (4-i)
        msg += group_str.rstrip()

    return msg

# %%
def extended_euclidean_algorithm(a: int, b: int) -> tuple:
    if b == 0:
        return (1, 0, a)
    else:
        x, y, gcd = extended_euclidean_algorithm(b, a % b)
        return (y, x - (a // b) * y, gcd)

# %%
def generate_keypair(p: int, q: int) -> tuple:
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e such that e and phi(n) are coprime.
    # In practice, e is usually a small prime number, such as 65537.
    e = 7
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    # Use the extended Euclidean algorithm to compute the private key.
    # d is the multiplicative inverse of e modulo phi(n).
    # That is, d * e = 1 (mod phi(n)).
    x, y, gcd = extended_euclidean_algorithm(e, phi)
    d = x % phi
    
    # Return the public and private keys as a tuple.
    public_key = (e, n)
    private_key = (d, n)
    return (public_key, private_key)

# %%
def encrypt(public_key: tuple, message: int) -> int:
    e, n = public_key
    return pow(message, e, n)

def decrypt(private_key: tuple, encrypted_message: int) -> int:
    d, n = private_key
    return pow(encrypted_message, d, n)

# %%
import sympy
def generate_prime(bit_length):
    while True:
        p = sympy.randprime(2**(bit_length-1), 2**bit_length - 1)
        return p

def generate_two_distinct_primes():
    while True:
        p = generate_prime(1024)
        q = generate_prime(1024)
        if p != q:
            return p, q
        

# %%
def Encrypt(message: str, public_key: tuple) -> int:
    encoded_message = encode_message(message)
    encrypted_message = encrypt(public_key, encoded_message)
    return encrypted_message

def Decrypt(encrypted_message: int, private_key: tuple) -> str:
    decoded_message = decrypt(private_key, encrypted_message)
    message = decode_message(decoded_message)
    return message
