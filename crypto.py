import ftplib
import sys
import os.path
from os import path
import linecache
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad

#crypto method
key_change = False
key = b'1111111111111111'
Nonce = get_random_bytes(16)
ENCRYPT_AND_MAC_IS_DOOMED = None
MAC_THEN_ENCRYPT_IS_DOOMED = None
ENCRYPT_THEN_MAC_IS_DOOMED = None

# ---------- Encrypt-then-MAC ----------
def hmac_sha256(data: bytes, key: bytes) -> bytes:
    h = HMAC.new(key, digestmod=SHA256)
    h.update(data)

    return h.digest()

def cbc_encrypt(p: bytes, iv: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    c = cipher.encrypt(pad(p, AES.block_size))

    return iv + c

def cbc_decrypt(c: bytes, key: bytes) -> bytes:
    iv = c[: AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return unpad(cipher.decrypt(c[AES.block_size:]), AES.block_size)

def encrypt_then_mac(
        p: bytes, iv: bytes, cipher_key: bytes, mac_key: bytes
    ) -> (bytes, bytes):
    cipher = cbc_encrypt(p, iv, cipher_key)
    mac = hmac_sha256(cipher, mac_key)
    return cipher, mac

def verify_then_decrypt(c: bytes, t: bytes, cipher_key: bytes, mac_key: bytes) -> bytes:
    mac = hmac_sha256(c, mac_key)
    if (mac == t):
        plain = cbc_decrypt(c, cipher_key)
        return plain

    else:
        raise ValueError("Invalid tag")

########AES-GCM Encryption and key change


def AES_GCM_Encrypt(filename):
    filename1 = os.path.basename(filename)
    with open(filename, "rb") as myfile:
        plaintext = myfile.read()

    encryptor = AES.new(key, AES.MODE_GCM)
    nonce = encryptor.nonce
    n = open("nonce"+filename1,"wb")
    n.write(nonce)

    AES_GCM_Cipher = encryptor.encrypt(plaintext)

    enc_file = open("encrypt" + filename1, "wb")
    enc_file.write(AES_GCM_Cipher)
    key_file = open("key"+filename1, "w")
    key_file.write(str(key))
    key_file.close()
    enc_file.close()

def AES_GCM_Decrypt(filename):
    filename1 = os.path.basename(filename)
    with open(filename, "rb") as myfile:
        plaintext = myfile.read()
    plainname=macfile_exist(filename1).rstrip()
    with open("nonce"+plainname,"rb") as myfile2:
        nonce = myfile2.read()
    encryptor = AES.new(key, AES.MODE_GCM, nonce=nonce)
    AES_GCM_Plain = encryptor.encrypt(plaintext)

    enc_file = open("decrypt" + filename1, "wb")
    enc_file.write(AES_GCM_Plain)
    key_file = open("key"+filename1, "w")
    key_file.write(str(key))
    key_file.close()
    enc_file.close()

iv = get_random_bytes(AES.block_size)
cipher_key = get_random_bytes(AES.block_size)
mac_key = get_random_bytes(AES.block_size)

def uploadmain(plainfilename,name,password):
    port = 8080
    ftp = ftplib.FTP()
    ftp.connect('', port)
    ftp.login(name, password)
    changedir(ftp, name)
    mac_key = get_random_bytes(AES.block_size)
    AES_GCM_Encrypt(plainfilename)
    plainfilename1=os.path.basename(plainfilename)
    # open the encrypted file and record the original filename with cipherfilename(for MAC matching in server list), then upload the encrypted file with encrypted filename(using hex to store looks like random charactors with random number)
    f = open("encrypt" + plainfilename1, "rb")
    c, t = encrypt_then_mac(bytes("encrypt" + plainfilename1, 'utf-8'), iv, cipher_key, mac_key)
    macname = t.hex()

    ftp.storbinary("STOR " + macname, f)
    print("file sent.")

    fname = open("filenamesent.txt", "a+")
    fname2 = open("plainfilenamesent.txt","a+")
    fname.write(os.path.basename(plainfilename) + "\n")
    fname2.write(os.path.basename(plainfilename) + "\n")
    fname.write(c.hex() + "\n")
    fname.write(mac_key.hex() + "\n")
    # close files
    f.close()
    fname.close()
    ftp.quit()

##download file if exist
def download(filename,name,password,checkmessage):
    port = 8080
    ftp = ftplib.FTP()
    ftp.connect('', port)
    ftp.login(name, password)
    changedir(ftp, name)
    checkmessage=False
    #check file exist, and out put the mac if exists
    file_exist(ftp,filename,checkmessage)
    ftp.quit()
##check file is existing in server
def file_exist(ftp,filename,check1):
    openfile = open("filenamesent.txt", 'rb')
    linecount = 0
    # count the line number of the file
    for line in openfile:
        if line != "\n":
            linecount += 1
    index = 1
    # using line number to iterate each line and find the filename matched, then use the corresponding cipher to MAC
    machex = hex(1)
    for index in range(linecount + 1):
        if linecache.getline('filenamesent.txt', index) == filename + "\n":
            print("found file in filenamesent.txt")
            c = linecache.getline('filenamesent.txt', index + 1)
            key = linecache.getline('filenamesent.txt', index + 2)
            mac = hmac_sha256(bytes.fromhex(c.rstrip("\n")), bytes.fromhex(key.rstrip("\n")))
            machex = mac.hex()
    print(machex)
    openfile.close()
    # using hex of the MAC match with the filename which is also hex of MAC in server list(if matched then its the same file)
    if filename in ftp.nlst():
        print("found")
        f = open(filename, "wb")
        ftp.retrbinary("RETR " + filename, f.write)
        print("file downloaded")
        check1=True
        f.close()
    else:
        print("file doesnt exist")

#find the macname and transfer to the plaintext name
def macfile_exist(macfile):
    openfile = open("filenamesent.txt", 'rb')
    linecount = 0
    # count the line number of the file
    for line in openfile:
        if line != "\n":
            linecount += 1

    # using line number to iterate each line and find the filename matched, then use the corresponding cipher to MAC
    machex = hex(1)
    for index in range(1,linecount,3):
        c = linecache.getline('filenamesent.txt', int(index+1))
        key = linecache.getline('filenamesent.txt', int(index+2))

        mac = hmac_sha256(bytes.fromhex(c.rstrip("\n")), bytes.fromhex(key.rstrip("\n")))
        machex = mac.hex()
        #check macname, if found then print the plainfile name
        if macfile == machex:
            #file = openfile.readlines()
            #return file[index]
            print("found file ")
            return linecache.getline('filenamesent.txt',int(index))
        index += 3
    #print(machex)
    openfile.close()

##get serverlist for user account
def getlist(name,password):
    port = 8080
    ftp = ftplib.FTP()
    ftp.connect('', port)
    ftp.login(name, password)
    changedir(ftp, name)
    nlst = ftp.nlst()
    ftp.quit()
    return nlst




def delete(filename,name,password):
    port = 8080
    ftp = ftplib.FTP()
    ftp.connect('', port)
    ftp.login(name, password)
    changedir(ftp, name)
    openfile = open("filenamesent.txt", 'rb')
    linecount = 0

    # count the line number of the file
    for line in openfile:
        if line != "\n":
            linecount += 1

    index = 1
    machex = hex(1)
    # using line number to iterate each line and find the filename matched, then use the corresponding cipher to MAC
    for index in range(linecount + 1):
        if linecache.getline('filenamesent.txt', index) == filename + "\n":
            print("found file in filenamesent.txt")
            c = linecache.getline('filenamesent.txt', index + 1)
            key = linecache.getline('filenamesent.txt', index + 2)
            mac = hmac_sha256(bytes.fromhex(c.rstrip("\n")), bytes.fromhex(key.rstrip("\n")))
            machex=mac.hex()
    # using hex of the MAC match with the filename which is also hex of MAC in server list(if matched then its the same file)
    if filename in ftp.nlst():
        print("found you want to delete file")
        ftp.delete(filename)

        print("file deleted")
    else:
        for i in ftp.nlst():
            print(i)
        print("can not find the file you want to delete")
    ftp.quit()

##check if server have the directory
def direc_exist(ftp,dir):
    if dir in ftp.nlst():
        return True
    return False

#change direc if exist , if no exist then create one
def changedir(ftp,dir):
        if direc_exist(ftp,dir) is False:
            ftp.mkd(dir)
        else:
            ftp.cwd(dir)
#######FTPclient side-ChaoWu
def connect(name,password):
    port = 8080
    ftp = ftplib.FTP()
    ftp.connect('', port)
    ftp.login(name,password)
    changedir(ftp,name)
    ftp.quit()
