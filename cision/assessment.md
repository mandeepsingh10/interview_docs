
## 1. Dockerfile for nginx 1.19 [5 pts]
Write a Dockerfile to run nginx version 1.19 in a container. Choose a base image, considering security best practices, and aim for the image to pass a container image security test.

```Dockerfile
FROM nginx:1.19.2-alpine

# Copy custom configuration
COPY custom-nginx.conf /etc/nginx/nginx.conf

# Expose the default Nginx port
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
```
## 2. Kubernetes StatefulSet [5 pts]
Write a Kubernetes StatefulSet to deploy the nginx container from the previous question. Utilize persistent volume claims and define resource limits for optimal performance.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx # Specifies the labels used to select the Pods managed by this StatefulSet.
  serviceName: "nginx"
  replicas: 3 
  minReadySeconds: 10 
  template:
    metadata:
      labels:
        app: nginx # The label to apply to the Pods.
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: DOCKER_IMAGE
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "my-storage-class"
      resources:
        requests:
          memory: "256Mi"
          cpu: "250m"
        limits:
          memory: "512Mi"
          cpu: "500m"
```
## 3. Build a Deployment Pipeline [10 pts]
Set up a streamlined build and deployment pipeline for the nginx application using GitHub Actions or an equivalent CI/CD tool. Ensure the pipeline covers building the Docker image, running security checks, and deploying to a Kubernetes cluster.

```yaml
name: Deploy-to-k8s

on:
  push:
    branches: [ main ] ## Assumption - We only want to deploy to the k8s cluster when code is pushed to master branch.

env:
  ECR_REPOSITORY: nginx-app
  EKS_CLUSTER_NAME: my-org-dev-01 
  AWS_REGION: us-east-1

jobs:
  
  deploy_to_k8s:
    name: K8s-Deployment
    runs-on: ubuntu-latest

    steps:
    - name: Set short git commit SHA
      id: commit
      uses: prompt/actions-commit-hash@v3

    - name: Checkout code
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.CICD_TOKEN }}
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ vars.AWS_ROLE_TO_ASSUME }} #Variable defined at repo/org level
        aws-region: us-east-1

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
      with:
        mask-password: 'true'

    - name: Build docker image tag, and push image to Amazon ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}        
        IMAGE_TAG: ${{ steps.commit.outputs.short }}
      run: docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG -f docker/Dockerfile .

    - name: Scan image for vulnerabilities
      continue-on-error: true # change this if you want the job to fail if trivy vulnerabilities are found
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        format: 'table'
        exit-code: '1'
        ignore-unfixed: true
        vuln-type: 'os,library'
        severity: 'CRITICAL,HIGH'

    - name: Push image to Amazon ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}        
        IMAGE_TAG: ${{ steps.commit.outputs.short }}
      run: docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

    - name: Update kube config
      run: aws eks update-kubeconfig --name $EKS_CLUSTER_NAME --region $AWS_REGION

    - name: Deploy to EKS
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}        
        IMAGE_TAG: ${{ steps.commit.outputs.short }}
      run: |
        sed -i.bak "s|DOCKER_IMAGE|$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG|g" manifests/nginx.yaml && \
        kubectl apply -f manifests/nginx.yaml

    - name: Run Kube-Bench to check cluster config
      continue-on-error: true
      run: |
        kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/master/job-eks.yaml
        sleep 30s
        kubectl logs job.batch/kube-bench
        kubectl delete job.batch/kube-bench
```
## 4.Text Manipulation Problem [5 pts]
Choose or create a text manipulation problem that involves using awk, sed, tr, and/or grep. Solve the problem, considering efficiency and readability.
- **Problem Statement**
Analyze SSH login attempts recorded in the syslog file, syslog.txt, to determine the status of these attempts. The file contains logs related to SSHD (SSH Daemon) with both successful and failed login attempts. Extract relevant entries, format the information in a readable table, and save the results to ssh_login_status.txt. The table should have two columns: IP and SSH STATUS. The IP column should contain the IP address of the client attempting to log in, and the SSH STATUS column should contain the status of the login attempt (either FAILED  or ACCEPTED). 
- **Sample file - syslog.txt**
```
May 17 10:15:32 server1 sshd[12345]: Failed password for root from 172.20.1.10 port 22 ssh2
May 17 10:16:01 server1 CRON[12346]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)
May 17 10:16:02 server1 sshd[12347]: Accepted password for user1 from 172.20.1.11 port 22 ssh2
May 17 10:17:10 server1 sudo:    user1 : TTY=pts/1 ; PWD=/home/user1 ; USER=root ; COMMAND=/bin/ls
May 17 10:17:12 server1 sshd[12348]: Failed password for invalid user guest from 172.20.1.19 port 22 ssh2
May 17 10:18:32 server1 sshd[12349]: Failed password for root from 172.20.1.17 port 22 ssh2
```

```sh
#!/bin/bash
# Define the output file
output_file="ssh_login_status.txt"

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
```
- **Output File - ssh_login_status.txt**
```
+------------------+--------------+
| IP               | SSH STATUS   |
+------------------+--------------+
| 172.20.1.10      | FAILED       |
| 172.20.1.11      | ACCEPTED     |
| 172.20.1.19      | FAILED       |
| 172.20.1.17      | FAILED       |
+------------------+--------------+
```
## 5. Text Manipulation with an Object Orientated Programming Language [5 pts]
Solve the text manipulation problem from the previous question using any Object Orientated Programming language of your choice. Provide a clear and well-documented solution.

```python
#!/usr/bin/env python3

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
    output_file = "ssh_login_status.txt"
    
    write_header(output_file)
    process_syslog(input_file, output_file)
    write_footer(output_file)

if __name__ == "__main__":
    main()
```
- **Output File - ssh_login_status.txt**
```
+------------------+--------------+
| IP               | SSH STATUS   |
+------------------+--------------+
| 192.168.0.1      | FAILED       |
| 192.168.0.2      | ACCEPTED     |
| 192.168.0.3      | FAILED       |
| 192.168.0.1      | FAILED       |
+------------------+--------------+
```
## 6. Sum of Even Fibonacci Numbers [10 pts]
Write a program in an Object Oriented Programming language of your choice to calculate the sum of the first 100 Fibonacci numbers that are even. Ensure efficiency and demonstrate good coding practices.

```python
a, b = 0, 1
even_fibs = []
count = 0
sum_even = 0

while len(even_fibs) < 100:
    fib_num = a  # Current Fibonacci number
    if fib_num % 2 == 0:  # Check if the number is even
        even_fibs.append(fib_num)  # Add the even Fibonacci number to the list
        sum_even += fib_num  # Add the even Fibonacci number to the sum
        #print(fib_num)  # Print the even Fibonacci number
    a, b = b, a + b  # Update Fibonacci sequence
    count += 1

print(sum_even)  # Print the sum of even Fibonacci numbers
```
## 7. Intersection of Sorted Arrays [10 pts]
Write a function in a Object Orientated Programming language of your choice that takes two sorted arrays of integers as input and returns an array containing numbers common to both arrays without duplicates.

```python
def find_common_numbers(array1, array2):
    set1 = set(array1)
    set2 = set(array2)
    return list(set1.intersection(set2))

# Example usage:
array1 = [10, 31, 41, 62, 17, 99]
array2 = [62, 3, 99, 17, 8]
print(find_common_numbers(array1, array2))
```
## 8. Decimal Digit Transformation [10 pts]
Write a function in an Object Orientated Programming language of your choice that, when passed a decimal digit X, calculates and returns the value of X + XX + XXX + XXXX. For example, if X is 3, the function should return 3702 (3 + 33 + 333 + 3333). Ensure the function handles valid inputs and provides meaningful error messages for invalid inputs.

```python
def calculate_sum(n):
    sum = 0
    number_as_string = str(n)
    for i in range(1, 5):
        X = int(number_as_string * i)
        sum += X
    return sum

while True:
    my_num = input("Enter a single-digit number: ")
    
    if my_num.isdigit():
        my_num = int(my_num)
        if 0 <= my_num <= 9:
            result = calculate_sum(my_num)
            print("Result:", result)
            break
        else:
            print("Error: Input must be between 0 and 9.")
    else:
        print("Error: Alphabets, special character and floating point numbers are not allowed.")
```