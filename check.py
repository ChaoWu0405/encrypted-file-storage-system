import crypto
import ftplib
import sys
from ftplib import FTP
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad
import os.path
from os import path
import linecache
def login(name, password):
    global loginValid
    loginValid = False
    file = open("/Users/charles/PycharmProjects/pythonProject/server/user_info.txt", "r")
    for i in file:
        n, p = i.split(",")
        p = p.strip()
        if (n == name and p == password):
            loginValid = True
            print("correct info")
            crypto.connect(name,password)
            current = open("current.txt", "a")
            current.write(name + "," + password + "\n")
            current.close()
            break
    return loginValid
    file.close()

def register(name, password):
    file = open("/Users/charles/PycharmProjects/pythonProject/server/user_info.txt", "a")
    file.write(name+","+password+"\n")
    file.close()

key_change = False
key = b'1111111111111111'
Nonce = get_random_bytes(16)
ENCRYPT_AND_MAC_IS_DOOMED = None
MAC_THEN_ENCRYPT_IS_DOOMED = None
ENCRYPT_THEN_MAC_IS_DOOMED = None

def uploadCheck(plainfilename):

   pass

def checkUsername(name):
    check = True
    file = open("user_info.txt", "r")
    for i in file:
        n, p = i.split(",")
        p = p.strip()
        if (n == name):
            check = False
            break
    file.close()
    return check


