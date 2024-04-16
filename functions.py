import socket
from log import *

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

def validateIP(deviceIP):
    try:
        socket.inet_aton(deviceIP)
        authLog.info(f"IP successfully validated: {deviceIP}")
        return True
    except socket.error:
        authLog.error(f"Not a valid IP address: {deviceIP}") 
        try:
            socket.gethostbyname(deviceIP)
            authLog.info(f"Hostname successfully validated: {deviceIP}")
            return True
        except socket.gaierror:
            authLog.error(f"Not a valid hostname: {deviceIP}")
            return False
                
def delStringFromFile(filePath, stringToDel):
    with open(filePath, "r") as file:
        file_content = file.read()

    updated_content = file_content.replace(stringToDel, "")

    with open(filePath, "w") as file:
        file.write(updated_content)

def checkYNInput(stringInput):
    return stringInput.lower() == 'y' or stringInput.lower() == 'n'