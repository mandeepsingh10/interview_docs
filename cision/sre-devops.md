Please answer these questions to the best of your abilities. Higher points are awarded for more detailed and complete answers. Bonus points for good security throughout. 

N.B. If you decide to use AI, do make sure you understand what is generated. Most generated responses do not score highly. You will be questioned on your answers in an interview.

1. Dockerfile for nginx 1.19 [5 pts]
Write a Dockerfile to run nginx version 1.19 in a container. Choose a base image, considering security best practices, and aim for the image to pass a container image security test.
**Solution - 1_Dockerfile**

2. Kubernetes StatefulSet [5 pts]
Write a Kubernetes StatefulSet to deploy the nginx container from the previous question. Utilize persistent volume claims and define resource limits for optimal performance.
**Solution - 2_nginx.yaml**

3. Build a Deployment Pipeline [10 pts]
Set up a streamlined build and deployment pipeline for the nginx application using GitHub Actions or an equivalent CI/CD tool. Ensure the pipeline covers building the Docker image, running security checks, and deploying to a Kubernetes cluster.
**Solution - 3_gha_deploy_to_k8s.yaml**

4. Text Manipulation Problem [5 pts]
Choose or create a text manipulation problem that involves using awk, sed, tr, and/or grep. Solve the problem, considering efficiency and readability.
**Solution - 4_text_manipulation.sh (Input file is syslog.txt & Output file is 4_bash_ssh_login_status.txt)**

5. Text Manipulation with an Object Orientated Programming Language [5 pts]
Solve the text manipulation problem from the previous question using any Object Orientated Programming language of your choice. Provide a clear and well-documented solution.
**Solution - 5_text_manipulation.py (Input file is syslog.txt & Output file is 5_python_ssh_login_status.txt)**

6. Sum of Even Fibonacci Numbers [10 pts]
Write a program in an Object Oriented Programming language of your choice to calculate the sum of the first 100 Fibonacci numbers that are even. Ensure efficiency and demonstrate good coding practices.
**Solution - 6_fibonacci.py**

7. Intersection of Sorted Arrays [10 pts]
Write a function in a Object Orientated Programming language of your choice that takes two sorted arrays of integers as input and returns an array containing numbers common to both arrays without duplicates.
**Solution - 7_common_array.py**

8. Decimal Digit Transformation [10 pts]
Write a function in an Object Orientated Programming language of your choice that, when passed a decimal digit X, calculates and returns the value of X + XX + XXX + XXXX. For example, if X is 3, the function should return 3702 (3 + 33 + 333 + 3333). Ensure the function handles valid inputs and provides meaningful error messages for invalid inputs.
**Solution - 8_xdigit.py**