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
