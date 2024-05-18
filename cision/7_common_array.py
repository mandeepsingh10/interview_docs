def find_common_elements(array1, array2):
    set1 = set(array1)
    set2 = set(array2)
    return list(set1.intersection(set2))

# Example usage:
array1 = [10, 31, 41, 62, 17, 99]
array2 = [62, 3, 99, 17, 8]
print(find_common_elements(array1, array2))