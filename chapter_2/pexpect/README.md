# Pexpect

## Overview
This chapter explores automating CLI-based network device interactions using Python's Pexpect library. While modern network automation increasingly relies on APIs and declarative tools, understanding low-level SSH/Telnet automation remains essential for legacy devices, emergency situations, and understanding how higher-level tools work under the hood.

## Scripts

### `chapter2_1.py` - Basic Pexpect with Telnet
Demonstrates fundamental Pexpect concepts using Telnet to connect to multiple devices and retrieve version information.

### `chapter2_2.py` - Pexpect with SSH
Production-style script featuring SSH connections, secure credential handling, multiple command execution, and output logging to timestamped files.

## Technologies Used

**Pexpect Library** - Pure Python module for spawning and controlling child applications
- `spawn()` - Launch child process
- `expect()` - Wait for pattern in output
- `sendline()` - Send command with newline
- `pxssh` - Specialized SSH subclass

## Real-World Relevance

**When Pexpect is useful:**
- Legacy devices without API support
- Emergency break-glass automation
- Initial device bootstrapping
- Multi-vendor environments with inconsistent API support

**Modern alternatives:**
- **Netmiko** - Higher-level SSH abstraction for network devices
- **Nornir** - Parallel execution framework
- **Ansible** - Idempotent, declarative automation
- **NETCONF/RESTCONF** - Structured, reliable APIs

