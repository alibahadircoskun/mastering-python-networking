
# Paramiko

## Overview
Paramiko is a Python implementation of SSHv2 protocol focused exclusively on SSH (no Telnet support). It's the underlying transport layer used by Ansible for network modules. Unlike Pexpect, Paramiko requires manual buffer management with `recv()` and `send()` methods, and uses `invoke_shell()` for interactive sessions with network devices.

Built automation scripts that progress from basic SSH connections to production-ready tools reading device inventories from JSON files and executing configuration changes across multiple devices. Key limitation: Cisco IOS drops connections after `exec_command()`, so must use `invoke_shell()` for multiple commands. Also implemented key-based authentication for managing Linux servers.

## Scripts

**chapter2_3.py** - Basic Paramiko with SSH connections and show commands  
**chapter2_4.py** - Production script using external `devices.json` and `commands.txt` files  

## Real-World Relevance

**When Paramiko is useful:**
- SSH-only automation requirements
- Key-based authentication needed
- Server and network device automation
- Foundation for building custom automation tools
- Linux-based network devices (Cumulus, Vyatta)

**Why it matters:**
- **Powers Ansible** - Network modules use Paramiko transport
- **Secure by design** - SSHv2 only, supports key authentication
- **Server management** - Better than Pexpect for Linux servers
- **Production-ready** - Robust error handling and session management
