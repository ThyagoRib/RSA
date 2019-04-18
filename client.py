'''Provides a Client class to handle users login in an RSA module.'''

import os
from rsa.decrypter import *
from rsa.encrypter import *
from rsa.rsa import *


class Client:
    '''Handles all user methods and the data base file.'''

    def __init__(self):
        '''Initiate Client and clients.txt, case it doesn't exist'''
        self.userList = []
        self.userPassword = []
        self.clientPublicKey = (0, 0)
        self.clientPrivateKey = (0, 0)
        self.userDecrypter = Decrypter()

        # Creates the clients.txt file if it doesn't exist.
        f = open("clients.txt", "a")
        f.close()
        # Tries to load existent users
        self.loadUsers()

    def loadUsers(self):
        '''
        Reads the clients.txt and loads the users list.

        Do nothing if clients.txt is empty.
        '''
        clientKeys = []

        # Check if file is empty.
        if os.stat("clients.txt").st_size != 0:
            with open("clients.txt", "r") as f:
                # Read the Client keys line.
                clientKeys = f.readline().split()
                # Set Client's public and private keys from clients.txt.
                self.clientPublicKey = (int(clientKeys[0]),
                                        int(clientKeys[1]))
                self.clientPrivateKey = (int(clientKeys[2]),
                                         int(clientKeys[3]))
                # Loop through remaining lines to load users list
                # and their respective passwords.
                for x, line in enumerate(f):
                    if x % 2 == 0:
                        self.userList.append(self.decryptUser(line.strip()))
                    else:
                        self.userPassword.append(
                            self.decryptUser(line.strip()))

        # Testing method results
        # print(self.userList)
        # print(self.userPassword)

    def decryptUser(self, user):
        '''Uses the Client private key to decrypt the users data'''
        return self.userDecrypter.decrypt(user, *self.clientPrivateKey)

    def encryptUsers(self):
        '''Encrypt and save the users data'''
        encryptedUsers = []
        encryptedPasswords = []
        ind = 0
        # Get a new random set of public and private keys
        # and replaces the current ones.
        self.setKeys()

        # Encrypt users one by one
        for x in self.userList:
            enc = Encrypter(x)
            encryptedUsers.append(enc.encrypt(*self.clientPublicKey))

        # Encrypt passwords one by one
        for x in self.userPassword:
            enc = Encrypter(x)
            encryptedPasswords.append(enc.encrypt(*self.clientPublicKey))

        # Write data to clients.txt
        with open("clients.txt", "w") as f:
            # Write public and private keys
            f.write(str(self.clientPublicKey[0]) + ' '
                    + str(self.clientPublicKey[1]) + ' '
                    + str(self.clientPrivateKey[0]) + ' '
                    + str(self.clientPrivateKey[1]) + '\n')
            # Write encrypted user and his password
            for x in encryptedUsers:
                f.write(x + '\n')
                f.write(encryptedPasswords[ind] + '\n')
                ind += 1

    def setKeys(self):
        '''
        Replaces current Client's public and private keys
        with a new random set.
        '''
        rsa = RSA()
        rsa.setup()

        self.clientPublicKey = rsa.publicKeys
        self.clientPrivateKey = rsa.privateKeys

    def authUser(self, login, password):
        '''User authentication method'''
        # Check if user exists
        if self.isUser(login):
            # Check if the given password is correct
            if self.userPassword[self.userList.index(login)] == password:
                print('\nSuccessfully logged as ' + login + '!\n')
                return True
            else:
                print('\nInvalid password, please try again.\n')
                return False
        else:
            print('\nUsername is invalid or not found, please try again.\n')
            return False

    def isUser(self, login):
        '''Checks if user exists in a user list'''
        userFound = False
        for x in self.userList:
            if userFound == True:
                break
            elif x == login:
                userFound = True
        return userFound

    def addUser(self, login, password):
        '''Adds user in a users list'''
        # Check if username is available
        if self.isUser(login):
            return '\nUsername already exists, please try again.\n'

        self.userList.append(login)
        self.userPassword.append(password)

        return '\nUser successfully added!\n'

    def delUser(self, login):
        '''Deletes user from a users list'''
        if not self.isUser(login):
            return "\nUser doesn't exist, please try again.\n"

        ind = self.userList.index(login)
        self.userList.remove(login)
        del self.userPassword[ind]

        return '\nUser successfully removed!\n'
