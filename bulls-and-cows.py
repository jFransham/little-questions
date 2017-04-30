import random

def generate_secret(length):
    digits = list(range(10))
    random.shuffle(digits)
    return digits[:length]


def guess_one(secret, guess):
    bulls = 0
    cows = 0

    # As far as I can tell the only way to get an index safely in O(n) in
    # Python is to catch the exception or write your own `index` implemenation
    for (i, val) in enumerate(guess):
        try:
            if secret.index(val) == i:
                bulls += 1
            else:
                cows += 1
        except ValueError:
            continue

    return (bulls, cows)


num_chars = 4
secret = generate_secret(num_chars)

while True:
    guess = input('Guess: ')
    try:
        guess_numbers = list(map(int, list(guess)))
        if len(guess_numbers) != num_chars:
            print('You have to guess a', num_chars, 'digit code!')
            continue
    except ValueError:
        print('Not a number:', guess)
        continue

    (bulls, cows) = guess_one(secret, guess_numbers)
    if bulls == num_chars:
        print('Correct!')
        break
    else:
        print(bulls, 'bulls,', cows, 'cows')
