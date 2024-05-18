#!/usr/bin/env python3
## PROBLEM STATEMENT
## Analyze SSH login attempts recorded in the syslog file, syslog.txt, to determine the status of these attempts. 
## The file contains logs related to SSHD (SSH Daemon) with both successful and failed login attempts. 
## Extract relevant entries, format the information in a readable table, and save the results to 5_python_ssh_login_status.txt. 
## The table should have two columns: IP and SSH STATUS. 
## The IP column should contain the IP address of the client attempting to log in, and the SSH STATUS column should contain the status of the login attempt (either FAILED PASSWORD or ACCEPTED PASSWORD). 

def write_header(output_file):
    with open(output_file, "w") as file:
        file.write("+------------------+--------------+\n")
        file.write("| IP               | SSH STATUS   |\n")
        file.write("+------------------+--------------+\n")

def process_syslog(input_file, output_file):
    with open(input_file, "r") as syslog, open(output_file, "a") as output:
        for line in syslog:
            if "sshd" in line and ("Failed password" in line or "Accepted password" in line):
                parts = line.split()
                status = "ACCEPTED" if "Accepted" in line else "FAILED"
                ip = parts[parts.index("from") + 1]
                ip = ip.strip(":")

                output.write(f"| {ip:16} | {status:12} |\n")

def write_footer(output_file):
    with open(output_file, "a") as file:
        file.write("+------------------+--------------+\n")

def main():
    input_file = "syslog.txt"
    output_file = "5_python_ssh_login_status.txt"
    
    write_header(output_file)
    process_syslog(input_file, output_file)
    write_footer(output_file)

if __name__ == "__main__":
    main()
