#!/usr/bin/env python3
import getpass
from pexpect import pxssh

devices = {
    'iosv-1': {'prompt': 'iosv-1#', 'ip': '192.168.100.51'},
    'iosv-2': {'prompt': 'iosv-2#', 'ip': '192.168.100.52'},
}

commands = ['terminal length 0', 'show version', 'show run']

username = input('Username: ')
password = getpass.getpass('Password: ')

# SSH Options to ensure connection to older Cisco devices/Labs
SSH_OPTIONS = {
    "StrictHostKeyChecking": "no",
    "UserKnownHostsFile": "/dev/null",
    "KexAlgorithms": "+diffie-hellman-group14-sha1",
    "HostKeyAlgorithms": "+ssh-rsa",
    "PubkeyAcceptedAlgorithms": "+ssh-rsa"
}

# The Main Loop
for device in devices:
    outputFileName = device + '_output.txt'
    device_prompt = devices[device]['prompt']
    ip = devices[device]['ip']

    print(f"Connecting to {device} ({ip})...")

    try:
        child = pxssh.pxssh(options=SSH_OPTIONS, encoding='utf-8')
        
        child.login(ip, username, password, auto_prompt_reset=False)

        # Open file and run commands
        with open(outputFileName, 'w') as f:
            for command in commands:
                child.sendline(command)
                
                # Wait until the device prompt appears again
                child.expect(device_prompt, timeout=60)
                
                # Write the output (child.before contains the output of the command)
                f.write(f"##### {command} #####\n")
                f.write(child.before)
                f.write("\n\n")

        child.logout()
        print(f"Finished {device}.")

    except Exception as e:
        print(f"Error connecting to {device}: {e}")
