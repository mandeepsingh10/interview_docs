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
