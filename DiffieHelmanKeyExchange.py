import random

def mod_exp(base, exp, modulus):
    """ Efficiently computes (base ** exp) % modulus using exponentiation by squaring """
    result = 1
    while exp > 0:
        if exp % 2 == 1:  # If exp is odd, multiply base with result
            result = (result * base) % modulus
        base = (base * base) % modulus  # Square the base
        exp //= 2  # Divide exponent by 2
    return result

def generate_prime(bits):
    """ Generates a random prime number of 'bits' length """
    while True:
        candidate = random.getrandbits(bits)
        if candidate % 2 != 0 and is_prime(candidate):
            return candidate

def is_prime(n, trials=5):
    """ Miller-Rabin primality test to check if n is likely prime """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Write n as 2^r * d + 1 with d odd (n-1 = 2^r * d)
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    def check_composite(a, d, n, r):
        """ Check if a^d % n == 1 or a^(d*2^j) % n == n-1 for some j in [0, r-1] """
        x = mod_exp(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                return False
        return True

    for _ in range(trials):
        a = random.randrange(2, n - 1)
        if check_composite(a, d, n, r):
            return False
    return True

def generate_dh_parameters():
    """ Generates parameters p (prime) and g (primitive root modulo p) for Diffie-Hellman """
    bits = 128  # Adjust bits as needed for security
    p = generate_prime(bits)
    
    # Find a generator g of the multiplicative group modulo p
    g = 2
    while mod_exp(g, (p - 1) // 2, p) == 1 or mod_exp(g, (p - 1) // 3, p) == 1:
        g += 1
    
    return p, g

def diffie_hellman_key_exchange():
    """ Performs Diffie-Hellman key exchange """
    p, g = generate_dh_parameters()
    print(f"Generated parameters: p = {p}, g = {g}")

    # Alice's side
    a_private = random.randint(2, p - 2)
    A = mod_exp(g, a_private, p)

    # Bob's side
    b_private = random.randint(2, p - 2)
    B = mod_exp(g, b_private, p)

    # Shared secret computation
    secret_key_A = mod_exp(B, a_private, p)
    secret_key_B = mod_exp(A, b_private, p)

    # Both should have the same shared secret
    assert secret_key_A == secret_key_B

    print(f"Alice's secret key: {secret_key_A}")
    print(f"Bob's secret key: {secret_key_B}")

# Example usage:
diffie_hellman_key_exchange()
