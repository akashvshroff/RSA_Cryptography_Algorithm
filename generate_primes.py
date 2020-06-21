from random import getrandbits, randrange


class GenPrimes:
    def __init__(self, length=1024, tests=128):
        self.p = 4  # prime candidate - start with a non-prime
        self.length = length  # length of prime in bits
        self.tests = tests

    def is_prime(self, n):
        """
        Checks if a number is prime based on the Miller-Rabin Primality Test.
        """
        if n in [2, 3]:
            return True
        if n <= 1 or not n % 2:  # Even or less than 0
            return False
        s = 0
        r = n - 1
        while not r & 1:  # get n-1 in the form (2^s)*r
            s += 1
            r //= 2
        """
        For the Miller-Rabin test, if a^r = 1 (mod n) or a^((2^j)r) = -1 (mod n)
        for some j where 0 ≤ j ≤ s-1 where a is a random number between 2,n-1 then the
        number is thought to strongly pseudo prime (w.r.t to base a).
        """
        for test in range(self.tests):  # do self.tests num of tests
            a = randrange(2, n-1)
            x = pow(a, r, n)
            if x != 1 and x != n-1:
                j = 1
                """
                Note: for any number n; n -1 (mod n) = -1 therefore if x which is a^((2^j)r) is n - 1,
                the whole equation is congruent to -1 and we can break out of the while loop and move to the
                next test.
                """
                while j < s and x != n-1:  # for j < s-1
                    x = pow(x, 2, n)
                    if x == 1:
                        return False
                    j += 1
                if x != n - 1:
                    return False
        return True

    def generate_prime_candidate(self):
        """
        Generates a possible prime number of self.length bits, sets the last bit
        to ensure that the number is odd and sets the first 2 bits to ensure that the random
        bits adhere to the length as decided.
        """
        self.p = getrandbits(self.length)
        mask = (1 << self.length-1) | (1 << self.length-2) | 1
        self.p |= mask

    def generate_prime(self):
        """
        Get a prime candidate, if not prime, then repeat the process, return number if prime.
        """
        while not self.is_prime(self.p):
            self.generate_prime_candidate()
        prime = self.p
        self.p = 4
        return prime


# prime_generator = GenPrimes()
# x = prime_generator.generate_prime()
# y = prime_generator.generate_prime()
# print(x)
# print(y)
