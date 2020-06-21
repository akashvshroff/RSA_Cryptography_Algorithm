from generate_primes import *
import string
import random
import time


class RsaEncryption:
    def __init__(self, length_message=2048):
        self.message = ''
        self.message_int = 0
        self.ciphered_int = 0
        self.cipher_text = ''
        self.deciphered_int = 0
        self.decrypted = ''
        self.length_primes = length_message//2
        self.n, self.p, self.q, self.d, self.e, self.phi = 0, 0, 0, 0, 65537, 0
        self.prime_generator = GenPrimes(length=self.length_primes)
        self.pad = string.ascii_lowercase + string.ascii_uppercase
        self.choose_primes()
        self.driver()

    def convert_to_int(self, text):
        res = 0
        for i in range(len(text)):
            res = res * 256 + ord(text[i])
        return res

    def convert_to_str(self, n):
        res = ""
        while n > 0:
            res += chr(n % 256)
            n //= 256
        return res[::-1]

    def fast_mod_exponent(self, b, e, m):
        """
        Represents exponent - e as a power of 2 or sum of self.fast_mod_exponenters of 2.
        """
        e_bin = bin(e)[2:]
        if e_bin.count('1') == 1:  # Power of 2
            k = int(math.log2(e))
            c = b % m
            for i in range(0, k):
                c = (c * c) % m
            return c
        else:
            set_pos = []
            for i, l in enumerate(e_bin):
                if l == '1':
                    set_pos.append(len(e_bin)-i-1)
            max_set = max(set_pos)
            c = b % m
            prod = []
            for i in range(max_set+1):
                if i in set_pos:
                    prod.append(c)
                c = (c*c) % m
            product = 1
            for x in prod:
                product = (product * x) % m
            return product

    def euclid_gcd(self, a, b):
        return self.euclid_gcd(b, a % b) if b > 0 else a

    def extended_euclid(self, a, b):
        if b == 0:
            return a, 1, 0
        gcd, p, q = self.extended_euclid(b, a % b)
        x = q
        y = p - (a//b)*q
        return gcd, x, y

    def choose_primes(self):
        while True:
            p, q = self.prime_generator.generate_prime(), self.prime_generator.generate_prime()
            phi = (p-1)*(q-1)
            if not abs(p-q) <= 1000000 and self.euclid_gcd(phi, self.e) == 1:
                break
        self.p, self.q, self.phi, self.n = p, q, phi, p*q
        gcd, x, y = self.extended_euclid(self.phi, self.e)
        self.d = y
        assert((self.e*self.d) % self.phi == 1)

    def check_message(self, message):
        if len(message) > 255:
            return False
        else:
            message += '*'
            to_pad = 255 - len(message)
            padding = ''.join(random.choices(self.pad, k=to_pad))
            self.message = message + padding
            return True

    def encrypt_message(self):
        self.message_int = self.convert_to_int(self.message)
        self.ciphered_int = self.fast_mod_exponent(self.message_int, self.e, self.n)
        self.cipher_text = self.convert_to_str(self.ciphered_int)

    def decrypt_message(self):
        encrypted_int = self.convert_to_int(self.cipher_text)
        self.deciphered_int = self.fast_mod_exponent(encrypted_int, self.d, self.n)
        self.decrypted = self.convert_to_str(self.deciphered_int)

    def driver(self):
        print("Welcome to a visualisation of RSA Encryption.")
        print("-"*15)
        print("Public Key: (e = {},n = {})".format(self.e, self.n))
        while True:
            print("Please enter message to be encrypted: (MAX 255 CHARS)\n")
            message = input()
            #message = 'Hi there this is my name.'
            if not self.check_message(message):
                print("Message is too long. Please re-enter.")
                continue
            else:
                break
        print("Padded message:\n{}".format(self.message))
        self.encrypt_message()
        time.sleep(0.3)
        print("-"*15)
        print("ENCRYPTED:\n")
        print("Encrypted num:\n\n{}".format(self.ciphered_int))
        print("Encrypted text: \n\n{}".format(self.cipher_text))
        print('\n')
        time.sleep(0.3)
        print("-"*15)
        print("Now decrypting, assuming you only send the ciphered text.")
        print("-"*15)
        time.sleep(0.5)
        self.decrypt_message()
        print("DECRYPTED:\n")
        print("Decrypted num:\n\n{}".format(self.deciphered_int))
        print("Decrpyted message:\n\n{}".format(self.decrypted))
        print("-"*15)


def main():
    obj = RsaEncryption()


if __name__ == '__main__':
    main()
