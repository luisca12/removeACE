from netmiko import ConnectHandler
from functions import *
from log import *
from strings import *
from auth import *

import os
import traceback
import re

shRun = "show run"
shACL = "show ip access-list qos-trusted-20230615"
shHostname = "show run | i hostname"

ipIntBrief = "show interface status | include Port | notconnect" #Real regex for production
intNotConnPatt = r'(Gi|Te)\d+/\d+/\d+' #Real regex for production

removeACE = [
    'ip access-list extended qos-trusted-20230615',
    'no 70',
    'no 80',
    '70 permit ip any host 30.230.15.145',
    '80 permit ip host 30.230.15.145 any',
    'do wr',
    'end'
]

def changeACL(validIPs, username, netDevice):
    # This function is to show the interfaces not connected.
    # show interface status | include Port | notconnect
    
    for validDeviceIP in validIPs:
        try:
            validDeviceIP = validDeviceIP.strip()
            currentNetDevice = {
                'device_type': 'cisco_xe',
                'ip': validDeviceIP,
                'username': username,
                'password': netDevice['password'],
                'secret': netDevice['secret'],
                'global_delay_factor': 2.0,
                'timeout': 120,
                'session_log': 'netmikoLog.txt',
                'verbose': True,
                'session_log_file_mode': 'append'
            }

            print(f"Connecting to device {validDeviceIP}...")
            with ConnectHandler(**currentNetDevice) as sshAccess:
                sshAccess.enable()
                shHostnameOut = sshAccess.send_command(shHostname)
                authLog.info(f"User {username} successfully found the hostname {shHostnameOut}")
                shHostnameOut = shHostnameOut.replace('hostname', '')
                shHostnameOut = shHostnameOut.strip()
                shHostnameOut = shHostnameOut + "#"

                with open(f"{validDeviceIP}_Outputs.txt", "a") as file:
                    file.write(f"User {username} connected to device IP {validDeviceIP}\n\n")
                    authLog.info(f"User {username} is now running commands at: {validDeviceIP}")

                    print(f"INFO: Taking a {shACL} for device: {validDeviceIP}")
                    shACLOutBefore = sshAccess.send_command(shACL)
                    print(f"Current (Old) ACL Configuration:\n{shACLOutBefore}")
                    authLog.info(f"Automation successfully ran the command: {shACL}\n{shACLOutBefore}")
                    file.write(f"INFO: Current ACL qos-trusted-20230615\n")
                    file.write(f"{shHostnameOut}{shACL}\n{shACLOutBefore}\n\n")

                    print(f"INFO: Deleting ACEs 70 & 80 from ACL qos-trusted-20230615 for device: {validDeviceIP}")
                    print(f"INFO: Adding new ACEs 70 & 80 for ACL qos-trusted-20230615 for device: {validDeviceIP}")
                    authLog.info(f"Automation is running the following commands for device: {validDeviceIP}:\n {removeACE}")

                    file.write(f"INFO: Starting to delete old ACEs and adding new ACEs\n")
                    file.write(f"INFO: Running the following commands\n {removeACE}\n")

                    removeACEOut = sshAccess.send_config_set(removeACE)
                    authLog.info(f"Automation successfully ran the commands for device: {validDeviceIP}:\n {removeACEOut}")
                    file.write(f"INFO: The following commands were executed:\n{removeACEOut}\n")
                    print(f"INFO: Successfully deleted the old 70 & 80 ACEs and added the new 70 & 80 ACEs for device: {validDeviceIP}")
                    shACLOutAfter = sshAccess.send_command(shACL)
                    file.write(f"INFO: New configuration for device {validDeviceIP} ACL qos-trusted-20230615:\n{shACLOutAfter}\n")
                    print(f"INFO: New configuration for device {validDeviceIP} ACL qos-trusted-20230615:\n{shACLOutAfter}\n")
                    authLog.info(f"New configuration for ACL qos-trusted-20230615 in device {validDeviceIP}:\n {removeACE}")

        except Exception as error:
            print(f"An error occurred: {error}\n", traceback.format_exc())
            authLog.error(f"User {username} connected to {validDeviceIP} got an error: {error}")
            authLog.debug(traceback.format_exc(),"\n")
            with open(f"failedDevices.txt","a") as failedDevices:
                failedDevices.write(f"User {username} connected to {validDeviceIP} got an error.\n")
        
        finally:
            print("Outputs and files successfully created.\n")
            print("For any erros or logs please check authLog.txt\n")