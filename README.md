# Outline:

- The RSA Algorithm is a form of assymetric or public key encryption and is one of the most commonly used encryption techniques.
- The working of the system is rather simple:
    - Depending on the bitsize (k) of the message to send, choose two prime numbers - p and q such that the product of the 2 primes, n (p*q) follows the condition k≤n.
    - Choose another integer e such that 1≤e<phi(n) where phi(n) is Euler's Totient Function that measures the number of integers between 1 and n-1 that are coprime with n, i.e have a greatest common divisor (gcd) of 1. Since p and q are primes, phi(n) is (p-1)*(q-1). The integer e is chosen such that it lies between the range and is coprime with phi(n).
    - Your public key is (e,n).
    - Calculate the modular inverse, d, of e with respect to phi(n) where modular inverse is a number that is multiplied with e to give remainder 1 with mod(phi(n)). This can be calculated with the Extended Euclid algorithm.
    - Your private key is (d,n)
    - To encrypt a message using the public key, convert the message an integer and then your ciphered text c is m^e mod(n).
    - Deciphering the ciphered text can then be completed by c^d mod(n).
    - Here is a comprehensive look at the [proof and working of the RSA algorithm.](https://www.di-mgt.com.au/rsa_alg.html)
- The RSA algorithm works since there is no known algorithm that can factorise an integer in polynomial time, much less an integer with close to 610 digits, therefore given n, it becomes almost impossible to find p and q. Thus finding the totient function and by extension the private keys is almost impossible, given that the algorithm is implemented correctly.
- Hence the RSA doesn't rely on something complex that we are able to do rather something simple that we are unable to do.
- A detailed description of the working of my implementation lies below.

# Purpose:

- As part of the Discrete Math for CS specialisation that I am currently completing, the RSA Algorithm was the final portion of our number theory course. The final project of the course made us implement simple RSA cracking techniques in case of faulty implementation and also made us implement the mechanism of the RSA given the public and private keys. I thoroughly enjoyed the modular arithmetic and RSA challenges and so I wanted to go one step further and implement the RSA entirely from scratch, from generating the primes to calculating all the modular arithmetic , handling string and integer conversion with padding as necessary and much more in order to create a safe encryption strategy.
- The build proved to be extremely engaging and somewhat challenging but wholly rewarding especially when I had to generate prime numbers with close to 310 digits each.
- All in all, the project was an apt introduction into the world of cybersecurity and cryptography and I'm looking forward to more such projects in the future!

# Description:

- First, let us begin with the generate_primes program.
    - The working principle of the program is the Miller Rabin primality test, a probabilistic test which determines whether a number is prime or not.
    - A wonderful resource that I used for this program is this [article.](https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb)
    - We start by generating random bits of a specific length as per our requirement - if the size of the message is k bits, we want to generate 2 primes, both of size k//2 bits.
    - We set the least significant and most significant bit, i.e make them 1 so that this value adheres to our length requirement. I also set the bit second from the left as this ensured that n which is p*q  spans the full bit length.
    - Using the Miller Rabin primality test, we then check to see if the number generated is prime; to do this, for our number n, we convert n-1 to the form (2^s)*r.
    - Then for any random base, a between 2 and n-1, we check if a^r = 1 (mod n) or a^((2^j)r) = -1 where j is some number such that 0 ≤ j ≤ s-1. If any of these are satisfied for any a, the number n is considered strongly pseudo prime w.r.t to base a.
    - This process is repeated some number of times (here 128) where a is randomly generated.
    - If the tests are satisfied 128 times, the number is considered prime and the probability of the test being incorrect being 4^-x where x is the number of tests.
    - If any of the tests return false, a new number is generated and the process is repeated.
    - All of this is neatly packed in a class GenPrimes, an object of which is created in the rsa_implementation program once the generate_primes program is imported.
- Now we look at the rsa_implementation program.
    - There are some helper functions that I first must explain:
        - convert_to_int(text) and convert_to_str(n) are used to pack and unpack the string and integer value respectively. The former works by adding the ascii value of the character and then using a base of 256 i.e multiplying by 256 in order to convert the string into an integer. The latter obtains the original text in reverse order by taking the number mod 256, obtaining the ascii value and then replacing the number with the number//256.
        - euclid_gcd(a,b) returns the greatest common divisor of a and b and it recursively calls itself replacing a by b and b by a%b until b is 0 at which point it returns a.
        - extended_euclid(a,b) returns the gcd of a,b and 2 integers x,y where ax + by = gcd(a,b). This is used to calculate the modular inverse of e as when you take the gcd of phi(n) and e, you get phi(n)*x + e*d = 1 where d is the modular inverse of e.
        - fast_modular_exponentiation(b,e,m) returns the result of the operation b^e mod m. This function works by converting the exponent e into either a power of 2 or a sum of powers of 2. E.g an exponent of 55 is: 2^5 + 2^4 + 2^2 + 2^1 + 2^0 while 64, being a power of 2 is just 2^6. You then iterate over k times where k≤the largest power of 2 that composes e. If e is a power of 2, you can simply square b and take the modulus at each step, reducing the number of iterations from e to log2(e). If it isn't a power of 2, you do the same thing but multiple only the set positions of 2.
    - After the values are initialised, the choose_primes function is called which creates an object of the GenPrimes class from the generate_primes program. This generates p,q such that the absolute value of p-q > 1,000,000 such that nobody can iterate around the square root of n to find p and q. It also checks whether e is coprime to phi(n). e is already set to 65537, an industry standard as this is a sum of only 2 powers of 2; 2^16 + 2^0 and is a prime number. If any of the conditions are not met, the primes are regenerated. d is also calculated such that it is the modular inverse of e.
    - The driver function accepts a user inputted string, and if the string is short, it is padded with random lower and uppercase letters until it is 255 characters long (1 character less as a contingency should the chosen primes cause n to be shorter). The padded message is then displayed.
    - The message is converted to a number and is encrypted using the modular formula above and the ciphered number and text are both displayed.
    - The text is then decrypted using the private key as calculated above and the original padded message is displayed. The decrypted number and text are both displayed.
    - By consistently displaying the values at each step of the process, the user can better visualise how the RSA Algorithm works, even though the usual purpose of the RSA Algorithm is to cipher and share a key in case of symmetric cryptography owing to the computational load, by using the RSA Algorithm to encrypt and display plaintext displays how secure a well implemented RSA Algorithm is.
