'''RSA encrypter for an RSA application.'''


class Encrypter:
    '''
    Encrypts a given message using the RSA standard algorithm.
    '''

    def __init__(self, message):
        self.ordList = []
        self.preCode(message)

    def preCode(self, message):
        '''Precodes the message into utf-8 decimal value.'''
        for x in message:
            charOrd = ord(x)
            self.ordList.append(charOrd)

    def encrypt(self, *key):
        '''
        Applies the RSA encryption algorithm then returns
        the final encoded string.
        '''
        encrypted = []

        # Loop through the numerical message and applies
        # the RSA encryption algorithm.
        for x in self.ordList:
            encrypted.append(str(x**key[1] % key[0]))

        outString = self.toString(encrypted)

        # testing the results
        # print(encrypted)
        # print(outString)

        return outString

    def toString(self, encryptedList):
        '''
        Encodes the numerical RSA encryption list into a
        char string.
        '''
        string = ''

        for x in encryptedList:
            for y in range(len(x)):
                # + 50 to keep char range from 'b' to 'k'
                if y < len(x) - 1:
                    string += chr(ord(x[y]) + 50)
                else:
                    string += chr(ord(x[y]) + 50) + " "

        return string
