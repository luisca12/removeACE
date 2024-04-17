from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException, NetMikoTimeoutException
from functions import *
from strings import greetingString
from log import *
from log import invalidIPLog
import socket
import traceback
import csv
import os
import logging

username = ""
execPrivPassword = ""
netDevice = {}
validIPs = []

def Auth():
    global username, execPrivPassword, netDevice, validIPs

    manualInput = input("\nDo you want to choose a CSV file?(y/n):")

    while not checkYNInput(manualInput):
        print("Invalid input. Please enter 'y' or 'n'.\n")
        authLog.error(f"User tried to choose a CSV file but failed. Wrong option chosen: {manualInput}")
        manualInput = input("\nDo you want to choose a CSV file?(y/n):")

    if manualInput == "y":
        while True:
            csvFile = input("Please enter the path to the CSV file: ")
            authLog.info(f"User chose to input a CSV file. CSV File path: {csvFile}")
            try:
                with open(csvFile, "r") as deviceFile:
                    csvReader = csv.reader(deviceFile)
                    for row in csvReader:
                        for ip in row:
                            ip = ip.strip()
                            ip = ip + ".mgmt.internal.das"
                            print(ip)
                            if validateIP(ip):
                                authLog.info(f"Valid IP address found: {ip} in file: {csvFile}")
                                validIPs.append(ip)
                                break
                            else:
                                print(f"Invalid IP address format: {ip}, will be skipped.\n")
                                authLog.error(f"Invalid IP address found: {ip} in file: {csvFile}")
            except FileNotFoundError:
                print("File not found. Please check the file path and try again.")
                authLog.error(f"File not found in path {csvFile}")
                authLog.error(traceback.format_exc())
                print("Exiting the program...")
                os.system("PAUSE")
                continue

            if not validIPs:
                print(f"No valid IP addresses found in the file path: {csvFile}\n")
                authLog.error(f"No valid IP addresses found in the file path: {csvFile}")
                authLog.error(traceback.format_exc())
                os.system("PAUSE")
                return None
            
            return validIPs,username,netDevice
    else:
        authLog.info(f"User decided to manually enter the IP Addresses.")
        while True:
            os.system("CLS")
            greetingString()
            deviceIPs = input("\nPlease enter the devices IPs separated by commas: ")
            deviceIPsList = deviceIPs.split(',')

            for ip in deviceIPsList:
                ip = ip.strip()
                if validateIP(ip):
                    try:
                        connTest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        connTest.settimeout(3)
                        connResult = connTest.connect_ex((ip, 22))
                        if connResult == 0:
                            validIPs.append(ip)
                            print(f"Device {ip} is reachable on port TCP 22.")
                            authLog.info(f"Device {ip} is reachable on port TCP 22.")
                        else:
                            print(f"Device {ip} is not reachable on port TCP 22, will be skipped.")
                            authLog.error(f"Device IP: {ip}, is not reachable on port TCP 22.")
                            authLog.debug(traceback.format_exc())

                    except Exception as error:
                        print("Error occurred while checking device reachability:", error,"\n")
                        authLog.error(f"Error occurred while checking device reachability for IP {ip}: {error}")
                        authLog.debug(traceback.format_exc())
                else:
                    print(f"Invalid IP address format: {ip}, will be skipped.")
                    authLog.error(f"User {username} input the following invalid IP: {ip}")
                    authLog.debug(traceback.format_exc())
            if validIPs:
                break

        while True:
            try:
                username = input("Please enter your unsername: ")
                password = input("Please enter your password: ")
                execPrivPassword = input("Pleae input your enable password: ")

                for deviceIP in validIPs:
                    netDevice = {
                        'device_type' : 'cisco_ios',
                        'ip' : deviceIP,
                        'username' : username,
                        'password' : password,
                        'secret' : execPrivPassword
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