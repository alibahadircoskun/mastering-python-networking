#!/usr/bin/env python3
import getpass
import pexpect

# List of devices
devices = {
    'iosv-1': '192.168.100.51',
    'iosv-2': '192.168.100.52',
}

# Commands to run
commands = ['terminal length 0', 'show version', 'show run']

# Get credentials
username = input('Username: ')
password = getpass.getpass('Password: ')

# Connect to each device
for device_name, device_ip in devices.items():
    print(f"\nConnecting to {device_name}...")
    
    # SSH command (with options for older Cisco devices)
    ssh_command = (f'ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 '
                   f'-o HostKeyAlgorithms=+ssh-rsa '
                   f'-o StrictHostKeyChecking=no '
                   f'{username}@{device_ip}')
    
    try:
        # Start SSH session
        session = pexpect.spawn(ssh_command, encoding='utf-8', timeout=30)
        
        # Login
        session.expect('assword:')
        session.sendline(password)
        
        # Wait for prompt (> or #)
        session.expect(['>', '#'])
        
        # Go to enable mode
        session.sendline('enable')
        session.expect('assword:')
        session.sendline(password)
        session.expect('#')
        
        print(f"Connected to {device_name}")
        
        # Run commands and save output
        output_file = open(f'{device_name}_output.txt', 'w')
        output_file.write(f"Device: {device_name}\n\n")
        
        for command in commands:
            session.sendline(command)
            session.expect('#')
            
            output_file.write(f"### {command} ###\n")
            output_file.write(session.before + "\n\n")
        
        output_file.close()
        print(f"Output saved to {device_name}_output.txt")
        
        # Logout
        session.sendline('exit')
        session.close()
        
    except Exception as e:
        print(f"Error connecting to {device_name}: {e}")

print("\nDone!")
