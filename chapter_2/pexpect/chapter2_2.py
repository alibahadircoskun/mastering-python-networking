#!/usr/bin/env python3
import getpass
import pexpect
import sys

devices = {
    'iosv-1': {'ip': '192.168.100.51'},
    'iosv-2': {'ip': '192.168.100.52'},
}

commands = ['terminal length 0', 'show version', 'show run']

username = input('Username: ')
password = getpass.getpass('Password: ').strip()
enable_password = getpass.getpass('Enable password (Enter = same as login): ').strip()
if not enable_password:
    enable_password = password

def connect_to_device(device_name, ip, user, passwd, enable_pw):
    """Connect to a Cisco device and return the session object"""
    
    ssh_cmd = f'ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 ' \
              f'-o HostKeyAlgorithms=+ssh-rsa ' \
              f'-o PubkeyAcceptedAlgorithms=+ssh-rsa ' \
              f'-o StrictHostKeyChecking=no ' \
              f'-o UserKnownHostsFile=/dev/null ' \
              f'-o PreferredAuthentications=password ' \
              f'{user}@{ip}'
    
    try:
        child = pexpect.spawn(ssh_cmd, encoding='utf-8', timeout=30)
        child.logfile_read = open(f'{device_name}_debug.log', 'w')
        
        # Handle initial connection
        idx = child.expect(['[Pp]assword:', 'yes/no', pexpect.TIMEOUT, pexpect.EOF])
        
        if idx == 1:  # yes/no for key
            child.sendline('yes')
            child.expect('[Pp]assword:')
        elif idx in [2, 3]:
            print(f"[{device_name}] Connection failed - timeout or EOF")
            return None
        
        # Send password
        child.sendline(passwd)
        
        # Wait for prompt (> or #)
        idx = child.expect([r'[\w\-]+>', r'[\w\-]+#', '[Pp]assword:', pexpect.TIMEOUT])
        
        if idx == 2:  # Wrong password
            print(f"[{device_name}] Authentication failed")
            return None
        elif idx == 3:
            print(f"[{device_name}] Timeout waiting for prompt")
            return None
        
        in_enable = False
        
        # If we got user prompt (>), enter enable mode
        if idx == 0:
            child.sendline('enable')
            idx = child.expect(['[Pp]assword:', r'[\w\-]+#', pexpect.TIMEOUT])
            
            if idx == 0:  # Enable password required
                child.sendline(enable_pw)
                idx = child.expect([r'[\w\-]+#', '[Pp]assword:', r'[\w\-]+>', pexpect.TIMEOUT])
                
                if idx == 0:
                    in_enable = True
                else:
                    print(f"[{device_name}] Failed to enter enable mode")
                    in_enable = False
            elif idx == 1:  # Already in enable
                in_enable = True
            else:
                print(f"[{device_name}] Timeout entering enable mode")
                return None
        else:  # idx == 1, already at # prompt
            in_enable = True
        
        return child, in_enable
        
    except Exception as e:
        print(f"[{device_name}] Connection error: {e}")
        return None

def run_commands(child, device_name, in_enable, cmd_list):
    """Execute commands and capture output"""
    
    outputs = []
    
    for command in cmd_list:
        if command == 'show run' and not in_enable:
            outputs.append({
                'command': command,
                'output': 'SKIPPED: Not in enable mode'
            })
            continue
        
        try:
            child.sendline(command)
            child.expect(r'[\w\-]+#', timeout=30)
            
            output = child.before.strip()
            # Remove the echoed command from output
            if output.startswith(command):
                output = output[len(command):].strip()
            
            outputs.append({
                'command': command,
                'output': output
            })
            
        except pexpect.TIMEOUT:
            print(f"[{device_name}] Timeout on command: {command}")
            outputs.append({
                'command': command,
                'output': 'ERROR: Command timeout'
            })
    
    return outputs

# Main execution
for device_name, device_info in devices.items():
    print(f"\n[{device_name}] Connecting to {device_info['ip']}...")
    
    result = connect_to_device(device_name, device_info['ip'], username, password, enable_password)
    
    if result is None:
        print(f"[{device_name}] Skipping due to connection failure")
        continue
    
    child, in_enable = result
    
    print(f"[{device_name}] Connected successfully (Enable mode: {in_enable})")
    
    # Run commands
    outputs = run_commands(child, device_name, in_enable, commands)
    
    # Write to file
    output_file = f'{device_name}_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Device: {device_name} ({device_info['ip']})\n")
        f.write(f"Enable mode: {in_enable}\n\n")
        f.write("=" * 80 + "\n\n")
        
        for item in outputs:
            f.write(f"##### {item['command']} #####\n")
            f.write(item['output'] + "\n\n")
            f.write("-" * 80 + "\n\n")
    
    print(f"[{device_name}] Output saved to {output_file}")
    
    # Close connection
    try:
        child.sendline('exit')
        child.expect(pexpect.EOF, timeout=5)
    except:
        pass
    
    if child.logfile_read:
        child.logfile_read.close()

print("\n✓ All devices processed")
