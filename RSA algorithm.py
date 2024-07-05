import random
import math

def is_prime(n, k=5):
    """ Miller-Rabin primality test """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    def check_composite(a, d, n, s):
        """ Check if n is composite using witness a """
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    # Write n as 2^r * d + 1 with d odd (n-1 = 2^r * d)
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        if check_composite(a, d, n, s):
            return False
    return True

def generate_prime(bits):
    """ Generate a prime number of 'bits' length """
    while True:
        candidate = random.getrandbits(bits)
        if candidate % 2 != 0 and is_prime(candidate):
            return candidate

def gcd_extended(a, b):
    """ Extended Euclidean Algorithm to find gcd and coefficients x, y such that ax + by = gcd(a, b) """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    """ Find d such that (d * e) % phi = 1 using Extended Euclidean Algorithm """
    gcd, x, _ = gcd_extended(e, phi)
    if gcd == 1:
        return x % phi
    return None

def generate_rsa_keys(bits):
    """ Generate RSA public and private keys """
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = random.randrange(2, phi)
    while math.gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # Compute d as modular multiplicative inverse of e modulo phi
    d = mod_inverse(e, phi)

    # Public key (e, n), Private key (d, n)
    return (e, n), (d, n)

def rsa_encrypt(message, public_key):
    """ Encrypt message using RSA """
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher

def rsa_decrypt(cipher, private_key):
    """ Decrypt cipher using RSA """
    d, n = private_key
    message = ''.join([chr(pow(char, d, n)) for char in cipher])
    return message

# Example usage:
if __name__ == "__main__":
    bits = 1024
    public_key, private_key = generate_rsa_keys(bits)
    message = "Hello, RSA!"

    print("Original message:", message)

    encrypted_message = rsa_encrypt(message, public_key)
    print("Encrypted message:", encrypted_message)

    decrypted_message = rsa_decrypt(encrypted_message, private_key)
    print("Decrypted message:", decrypted_message)
