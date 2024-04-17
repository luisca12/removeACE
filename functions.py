import socket
from log import *
from log import invalidIPLog
import csv
import traceback
from netmiko.exceptions import NetMikoAuthenticationException, NetMikoTimeoutException
from netmiko import ConnectHandler

def checkIsDigit(input_str):
    try:
        authLog.info(f"String successfully validated selection number {input_str}, from checkIsDigit function.")
        return input_str.strip().isdigit()
    
    except Exception as error:
        authLog.error(f"Invalid option chosen: {input_str}, error: {error}\n")

# def validateIP(deviceIP):
#     try:
#         socket.inet_aton(deviceIP)
#         authLog.info(f"IP successfully validated: {deviceIP}")
#         return True
#     except socket.error:
#         authLog.error(f"Not a valid IP address: {deviceIP}")
#         invalidIPLog.error(f"Invalid IP address: {deviceIP}")
#         try:
#             socket.gethostbyname(deviceIP)
#             authLog.info(f"Hostname successfully validated: {deviceIP}")
#             return True
#         except socket.gaierror:
#             authLog.error(f"Not a valid hostname: {deviceIP}")
#             invalidIPLog.error(f"Invalid hostname: {deviceIP}")
#             with open('invalidHostnames.csv', mode='a', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow([deviceIP])
#             return False
                
def validateIP(deviceIP):
    try:
        socket.inet_aton(deviceIP)
        authLog.info(f"IP successfully validated: {deviceIP}")
        return True
    except (socket.error, AttributeError):
        try:
            socket.gethostbyname(deviceIP)
            authLog.info(f"Hostname successfully validated: {deviceIP}")
            return True
        except (socket.gaierror, AttributeError):
            authLog.error(f"Not a valid IP address or hostname: {deviceIP}")
            invalidIPLog.error(f"Invalid IP address or hostname: {deviceIP}")
            # Append the invalid IP address or hostname to a CSV file
            with open('invalidDestinations.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([deviceIP])
            return False
        
def requestLogin(validIPs):
    while True:
        try:
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            execPrivPassword = input("Please input your enable password: ")

            for deviceIP in validIPs:
                netDevice = {
                    'device_type': 'cisco_ios',
                    'ip': deviceIP,
                    'username': username,
                    'password': password,
                    'secret': execPrivPassword
                }

                # sshAccess = ConnectHandler(**netDevice)
                # print(f"Login successful! Logged to device {deviceIP} \n")
                authLog.info(f"Successful saved credentials for username: {username}")

            return validIPs, username, netDevice

        except NetMikoAuthenticationException:
            print("\n Login incorrect. Please check your username and password")
            print(" Retrying operation... \n")
            authLog.error(f"Failed to authenticate - remote device IP: {deviceIP}, Username: {username}")
            authLog.debug(traceback.format_exc())

        except NetMikoTimeoutException:
            print("\n Connection to the device timed out. Please check your network connectivity and try again.")
            print(" Retrying operation... \n")
            authLog.error(f"Connection timed out, device not reachable - remote device IP: {deviceIP}, Username: {username}")
            authLog.debug(traceback.format_exc())

        except socket.error:
            print("\n IP address is not reachable. Please check the IP address and try again.")
            print(" Retrying operation... \n")
            authLog.error(f"Remote device unreachable - remote device IP: {deviceIP}, Username: {username}")
            authLog.debug(traceback.format_exc())

def delStringFromFile(filePath, stringToDel):
    with open(filePath, "r") as file:
        file_content = file.read()

    updated_content = file_content.replace(stringToDel, "")

    with open(filePath, "w") as file:
        file.write(updated_content)

def checkYNInput(stringInput):
    return stringInput.lower() == 'y' or stringInput.lower() == 'n'

def checkReachability(ip, port=22):
    # Used to check if an IP address is reachable on port TCP 22
    try:
        conn_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_test.settimeout(3)
        conn_result = conn_test.connect_ex((ip, port))
        if conn_result == 0:
            return 
    except Exception as error:
        print("Error occurred while checking device reachability:", error,"\n")
        authLog.error(f"Error occurred while checking device reachability for IP {ip}: {error}")
        authLog.debug(traceback.format_exc())
    return False

def readIPfromCSV(csvFile):
    try:
        with open(csvFile, "r") as deviceFile:
            csvReader = csv.reader(deviceFile)
            for row in csvReader:
                for ip in row:
                    ip = ip.strip()
                    ip = ip + ".mgmt.internal.das"
    except Exception as error:
        print("Error occurred while checking device reachability:", error,"\n")
        authLog.error(f"Error occurred while checking device reachability for IP {ip}: {error}")
        authLog.debug(traceback.format_exc())