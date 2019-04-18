'''Provides an RSA class for an RSA encryption/decryption application'''

import math
import random
from rsa.rsamath import *
from rsa.encrypter import *
from rsa.decrypter import *


class RSA:
    '''
    Generates a random set of public and private keys for RSA
    encryption from a list of the first 168 prime numbers.
    '''

    def __init__(self):
        self.publicKeys = (0, 0)
        self.privateKeys = (0, 0)

    def setup(self, *args):
        '''
        Generates a random set of public and private keys
        or setup the given key values.
        '''
        if len(args) == 0:
            # primeList lenght is 168 resulting 84 pairs.
            primeList = [x for x in range(2, 1000) if isPrime(x)]

            # Loop through primeList to get p and q.
            for x in range(0, 84):

                # Assures that p and q will be in the first and second
                # halfs of the list, respectively.
                length = len(primeList)
                p_index = random.randrange(0, int(length / 2))
                q_index = random.randrange(int(length / 2), length)

                # Generates a random public key from p and q.
                key = self.generatePublicKey(primeList[p_index],
                                             primeList[q_index])

                isSecure = self.checkSecurity(key)

                # If the key is secure, set public and private keys
                # and break the loop
                if isSecure == True:
                    self.publicKeys = key

                    # Generatesa a random private key from p and q.
                    c = key[1]
                    self.privateKeys = self.generatePrivateKey(c,
                                                               primeList[p_index],
                                                               primeList[q_index])
                    break

                # Remove already used numbers from primeList.
                primeList.remove(primeList[q_index])
                primeList.remove(primeList[p_index])
        else:
            # n = args[0]
            # c = args[1]
            self.publicKeys = (args[0], args[1])
            pq = breakKey(args[0])
            self.privateKeys = self.generatePrivateKey(args[1], pq[0], pq[1])

        return self.publicKeys

    def generatePublicKey(self, p, q):
        '''Generates a random public key from p and q.'''
        coprime = False
        ph = phi(p, q)

        # Look for an integer c that is relatively prime with phi(n)
        # given n = p * q.
        while coprime == False:

            c = random.randrange(2, 1000)

            if math.gcd(ph, c) == 1:
                coprime = True

        return ((p * q), c)

    def generatePrivateKey(self, c, p, q):
        '''Generates a random private key given a public key data.'''
        ph = phi(p, q)
        return ((p * q), modInverse(c, ph))

    def checkSecurity(self, publicKey):
        '''
        Checks if the given public key is secure.

        i.e. gcd(x, n) = 1, where x is the utf-8 value of every
        possible char in the message and n is in the public key.
        '''
        testString = 'abcdefghijklmnopqrstuvwxyz 1234567890'

        for x in range(37):
            if math.gcd(ord(testString[x]), publicKey[0]) != 1:
                return False

            return True

    def encrypt(self, message):
        '''Encrypts the given message'''
        encr = Encrypter(message)
        return encr.encrypt(*self.publicKeys)

    def decrypt(self, message):
        '''Decrypts the given message'''
        decr = Decrypter()
        return decr.decrypt(message, *self.privateKeys)
