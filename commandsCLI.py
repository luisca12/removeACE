from netmiko import ConnectHandler
from functions import *
from log import *
from strings import *
from auth import *

import os
import traceback

shRun = "show run"
shACL = "show ip acce qos-trusted-20230615"
shHostname = "show run | i hostname"

def changeACL(validIPs, username, netDevice):
    # This function is to show the interfaces not connected.
    # show interface status | include Port | notconnect
    try:
        for validDeviceIP in validIPs:
            validDeviceIP = validDeviceIP.strip()
            currentNetDevice = {
                'device_type': 'cisco_xe',
                'ip': validDeviceIP,
                'username': username,
                'password': netDevice['password'],
                'secret': netDevice['secret'],
                'global_delay_factor': 2.0,
                'timeout': 60,
                'session_log': 'netmikoLog.txt',
                # 'verbose': True,
                'session_log_file_mode': 'append'
            }

            print(f"Connecting to device {validDeviceIP}...")
            with ConnectHandler(**currentNetDevice) as sshAccess:
                sshAccess.enable()
                shHostnameOut = sshAccess.send_command(shHostname)
                shHostnameOut = shHostnameOut.replace('hostname ', '')
                shHostnameOut = shHostnameOut.strip()

                with open(f"{validDeviceIP}_Outputs.txt", "a") as file:
                    file.write(f"User {username} connected to device IP {validDeviceIP}\n\n")
                    shACLOut = sshAccess.send_command(shACL)
                    file.write(f"{shHostnameOut}{shACL}\n{shACLOut}\n\n")

    except Exception as error:
        print(f"An error occurred: {error}")
        authLog.info(f"User {username} connected to {validDeviceIP} got an error: {error}\n")
        authLog.info(traceback.format_exc())
        return []
    
    finally:
        print("Outputs and files successfully created.")
        print("For any erros or logs please check authLog.txt\n")
        os.system("PAUSE")