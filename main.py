'''Runs through Client and RSA modules.'''

import math
import getpass
import sys
from rsa.rsa import *
from client import *


def main():
    '''Runs through Client and RSA modules.'''
    # Load RSA module and Client module
    rsa = RSA()
    client = Client()

    # Enter frontPage loop to handle Client functions
    logged = False
    while logged == False:
        func = clientPage()
        if func == '0':
            # Save users list and exit program
            client.encryptUsers()
            sys.exit(0)
        elif func == '1':
            # Add user
            addUser(client)
        elif func == '2':
            # Remove user
            removeUser(client)
        elif func == '3':
            # Try to log user in RSA Module
            logged = loginUser(client)
        else:
            # General invalid function
            print('\nInvalid function, please try again.\n')

    # Once the user is logged in start handling RSA Module setup
    ready = False
    while ready == False:
        func = rsaPage()
        if func == '0':
            # Save users list and exit program
            client.encryptUsers()
            sys.exit(0)
        elif func == '1':
            # Setup RSA module with random key
            setupRsa(rsa)
            ready = True
        elif func == '2':
            # Setup RSA module with provided key
            print("\nPlease enter your public key in format")
            print("n c\n")
            n, c = map(int, input().split())
            setupRsa(rsa, n, c)
            ready = True
        else:
            # General invalid function
            print('\nInvalid function, please try again.\n')

    # Enter encrypt/decrypt page
    while True:
        func = encDecPage()
        if func == '0':
            # Save users list and exit program
            client.encryptUsers()
            sys.exit(0)
        elif func == '1':
            # Encrypt a message
            encryptMessage(rsa)
        elif func == '2':
            # Decrypt a message
            decryptMessage(rsa)
        else:
            # General invalis function
            print('\nInvalid function, please try again.\n')


def clientPage():
    '''Print Client functions page'''
    print("Type:\n0 - Exit\n1 - Add user")
    print("2 - Remove user\n3 - Login RSA Module\n")
    select = input()

    return select


def addUser(Client):
    '''Adds user to Client'''
    username = input('\nUsername: ')
    password = getpass.getpass('Password: ')

    # Check if username and password are valid before adding
    if (username.isalnum() and username.islower()) or username.isdigit():
        if (password.isalnum() and password.islower()) or password.isdigit():
            print(Client.addUser(username, password))
        else:
            print('\nPassword must contain only letters in lower case or numbers.')
            print('Please, try again.\n')
    else:
        print('\nUsername must contain only letters in lower case or numbers.')
        print('Please, try again.\n')


def removeUser(Client):
    '''Removes user from Client'''
    username = input('\nUsername: ')
    # Ask for password for security
    password = getpass.getpass('Confirm user password: ')
    print(Client.delUser(username))


def loginUser(Client):
    '''Logs user in Client'''
    username = input('\nUsername: ')
    password = getpass.getpass('Password: ')
    return Client.authUser(username, password)


def rsaPage():
    '''Print RSA functions page'''
    print("Type:\n0 - Exit\n1 - Generate a random key")
    print("2 - Enter your key\n")
    select = input()

    return select


def setupRsa(RSA, *args):
    '''Setup RSA module with or without a given key'''
    key = RSA.setup(*args)
    print("\nYour public key (n, c) is " + str(key) + "\n")


def encDecPage():
    '''Print Encrypter and Decrypter page'''
    print("Type:\n0 - Exit\n1 - Encrypt message")
    print("2 - Decrypt message\n")
    select = input()

    return select


def encryptMessage(RSA):
    '''Encrypt a message'''
    message = input('\nPlease type your message:\n')

    # Checks if 'message' is a valid message
    if validateMessage(message):
        print('\n' + RSA.encrypt(message) + '\n')
    else:
        print('\nInvalid message!')
        print('Your message must contain lower case letters or numbers.')
        print('Please, try again.\n')


def decryptMessage(RSA):
    '''Decrypt a message'''
    message = input('\nPlease type your message:\n')
    print('\n' + RSA.decrypt(message) + '\n')


def validateMessage(message):
    '''Checks if 'message' is a valid message for encryption'''
    # Message must be in lower case and alpha-numerical
    if message.islower():
        validate = message.split()

        for x in validate:
            if not x.isalnum():
                return False
    # Message can be all numerical
    elif message.isdigit():
        return True
    # Invalid message
    else:
        return False

    return True


if __name__ == '__main__':
    main()
