#!/usr/bin/env python3

numbers = [1, 2, 3, 2, 5, 3, 3, 5, 6, 3, 4, 5, 7]

duplicates = [number for number in numbers if numbers.count(number) > 1]
unique_duplicates = list(set(duplicates))

print(unique_duplicates)
