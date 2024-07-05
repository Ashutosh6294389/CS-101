import random

# Function to perform the Miller-Rabin primality test
def is_probable_prime(n, k=100):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d where d is odd
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Miller-Rabin test
    def miller_rabin_test(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False
    
    # Repeat k times for accuracy
    for _ in range(k):
        a = random.randint(2, n - 1)
        if not miller_rabin_test(a):
            return False
    
    return True

# Function to generate a random n-digit probable prime number
def generate_random_prime(n):
    lower_bound = 10**(n-1)
    upper_bound = 10**n - 1
    
    while True:
        num = random.randint(lower_bound, upper_bound)
        if is_probable_prime(num):
            return num

# Main function to handle user input and generate the prime number
def main():
    n = int(input("Enter the number of digits for the random prime number: "))
    random_prime = generate_random_prime(n)
    print(f"Random {n}-digit probable prime number: {random_prime}")

if __name__ == "__main__":
    main()
