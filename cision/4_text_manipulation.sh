#!/bin/bash

## PROBLEM STATEMENT
## Analyze SSH login attempts recorded in the syslog file, syslog.txt, to determine the status of these attempts. 
## The file contains logs related to SSHD (SSH Daemon) with both successful and failed login attempts. 
## Extract relevant entries, format the information in a readable table, and save the results to ssh_login_status.txt. 
## The table should have two columns: IP and SSH STATUS. 
## The IP column should contain the IP address of the client attempting to log in, and the SSH STATUS column should contain the status of the login attempt (either FAILED PASSWORD or ACCEPTED PASSWORD). 

# Define the output file
output_file="4_bash_ssh_login_status.txt"

# Print the header to the output file
echo "+------------------+--------------+" > "$output_file"
echo "| IP               | SSH STATUS   |" >> "$output_file"
echo "+------------------+--------------+" >> "$output_file"

# Process the syslog file
grep 'sshd' syslog.txt | grep -E 'Failed password|Accepted password' | awk '{
    status = $6
    ip = $(NF-3)
    printf "| %-16s | %-12s |\n", ip, status
}' | tr '[:lower:]' '[:upper:]' >> "$output_file"

# Print the footer to the output file
echo "+------------------+--------------+" >> "$output_file"
