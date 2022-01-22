from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import pathlib
import threading

name=''
password=''
authorizer = DummyAuthorizer()
file = open("user_info.txt", "r")
#"/Users/charles/PycharmProjects/pythonProject/server/"
for i in file:
    n, p = i.split(",")
    p = p.strip()
    authorizer.add_user(n, p, str(pathlib.Path(__file__).parent.resolve()), perm="elradfmw")
handler = FTPHandler
handler.authorizer = authorizer
connection = ('', 8080)
ftpd = FTPServer(connection, handler)

ftpd.serve_forever()





