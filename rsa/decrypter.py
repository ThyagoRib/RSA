'''RSA decrypter for an RSA application.'''


class Decrypter:
    '''
    Decrypts a given message using the RSA standard algorithm.
    '''

    def __init__(self):
        pass

    def decrypt(self, message, *key):
        '''
        Applies the RSA decryption algorithm then returns
        the decoded message.
        '''
        # Maps the given encrypted string into a list.
        encrypted = list(map(str, message.split()))
        encrypted = self.toInt(encrypted)

        outString = ''

        # Applies the RSA decryption algorithm to the list
        # and adds the result to the output string.
        for x in encrypted:
            outString += str(chr(x**key[1] % key[0]))

        '''testing the result'''
        # print(outString)

        return outString

    def toInt(self, stringList):
        '''
        Decodes the encrypted message from a char string list
        to a int list.
        '''
        intList = []

        for x in stringList:
            string = ''
            for y in range(len(x)):
                # -50 to reverse the char range from ('b','k')
                #to ('0', '9')
                string += chr(ord(x[y]) - 50)
            intList.append(int(string))

        return intList
