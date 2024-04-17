import socket
from log import *
from log import invalidIPLog
import csv
import traceback

def checkIsDigit(input_str):
    try:
        authLog.info(f"String successfully validated selection number {input_str}, from checkIsDigit function.")
        return input_str.strip().isdigit()
    
    except Exception as error:
        authLog.error(f"Invalid option chosen: {input_str}, error: {error}\n")

    #if input_str.strip().isdigit():
    #    return True
    #else:
    #    return False

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