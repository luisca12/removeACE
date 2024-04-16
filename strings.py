import os

def greetingString():
        os.system("CLS")
        print('  ------------------------------------------------- ')
        print("    Welcome to the automated remove ACE program ")
        print('  ------------------------------------------------- ')

def menuString(deviceIP, username):
        os.system("CLS")
        print(f"Connected to: {deviceIP} as {username}\n")
        print('  -------------------------------------------------------------- ')
        print('\t\tMenu - Please choose an option')
        print('\t\t  Only numbers are accepted')
        print('  -------------------------------------------------------------- ')
        print('  >\t\t1. To run the following commands:\t       <\n')
        print('\t       show access-list qos-trusted-20230615')
        print('\t\t\tremove ACEs 70 & 80')
        print('\t     Add back 70 & 80 but with IP 30.230.15.145\n')          
        print('  >\t\t\t2. Exit the program\t\t       <')
        print('  -------------------------------------------------------------- \n')

def inputErrorString():
        os.system("CLS")
        print('  ------------------------------------------------- ')  
        print('>      INPUT ERROR: Only numbers are allowed       <')
        print('  ------------------------------------------------- ')

def shRunString(validIPs):
        print('  ------------------------------------------------- ')  
        print(f'> Taking a show run of the device {validIPs} <')
        print('>\t   Please wait until it finishes\t  <')
        print('  ------------------------------------------------- ')
