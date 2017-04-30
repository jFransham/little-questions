import random


# Naive modified bubble sort, since it's simple and stable
def make_alternating(input_list):
    any_swapped = True
    while any_swapped:
        any_swapped = False
        for i in range(1, len(input_list) - 1):
            [lst, cur, nxt] = input_list[i-1:i+2]
            if lst == cur:
                input_list[i + 1] = cur
                input_list[i] = nxt
                any_swapped = True

    return input_list


k = 100
ones = [1] * k
zeroes = [0] * k
input_list = ones + zeroes

random.shuffle(input_list)

print(input_list)
print(make_alternating(input_list))
