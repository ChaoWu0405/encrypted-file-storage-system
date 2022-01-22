# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import ftpserver

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

#login in
def login(name,password):
    pass

def register(name,password):
    pass

def access(option):
    if(option=="login"):
        name = input("Enter your name: ")
        password = input("password: ")
        login(name,password)
    else:
        print("register")
        name = input

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    f = ftpserver
    f.ftpServerOn()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
