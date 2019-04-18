'''Provides a set of basic functions for an RSA application.'''

import math


def isPrime(number):
    '''Check if a given number is a prime number.'''
    for x in range(2, int(math.sqrt(number)) + 1):
        if number % x == 0:
            return False

    return True


def phi(p, q):
    '''
    Returns Euler's totient function [phi(n)]
    given p and q, with n = p * q.
    '''
    return (p - 1) * (q - 1)


def modInverse(c, ph):
    '''
    Returns a modular inverse from c and ph
    using the Extend Euclid Algorithm.

    Method code from:
    https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
    '''
    ph_aux = ph
    y = 0
    x = 1

    while c > 1:

        q = c // ph

        t = ph

        ph = c % ph
        c = t
        t = y

        y = x - q * y
        x = t

    if x < 0:
        x += ph_aux

    return x


def breakKey(n):
    '''
    Returns p and q, from a given n, needed to generate a private key.

    OBS: This method only exists because n is relatively low
         and is used when the user provides the public key.
    '''
    primeList = [x for x in range(2, 1000) if isPrime(x)]

    # Assume x = p and look for q, since n = p * q
    for x in range(len(primeList)):
        q = n / primeList[x]
        for y in range(x + 1, len(primeList)):
            if primeList[y] == q:
                return [primeList[x], primeList[y]]
