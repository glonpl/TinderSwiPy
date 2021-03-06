from getpass import getpass

from cryptography.fernet import Fernet


def encrypt():
    key = Fernet.generate_key()
    file = open('./key.key', 'wb')
    file.write(key)
    file.close()
    f = Fernet(key)
    email = f.encrypt(input("Type Your Email: ").encode())
    file = open('./mail.key', 'wb')
    file.write(email)
    file.close()
    password = f.encrypt(getpass("Type Your password: ").encode())
    file = open('./passwd.key', 'wb')
    file.write(password)
    file.close()
