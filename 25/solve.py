#!/usr/bin/python3

from math import log

def solve(filename):

    with open(filename) as f_in:
        
        total = 0

        for line in f_in:
            number = list(line.strip())

            #replace "minus"/"double-minus" with int strings
            for idx, digit in enumerate(number):
                digit = digit.replace('-', '-1')
                digit = digit.replace('=', '-2')
                number[idx] = int(digit)

            value = base_5_to_10(number)
            total += value

            print(value)
        
        print()
        print(total)
        print()
        
        base_5 = base_10_to_5(total)
        print(base_5)
        print(base_5_to_10(base_5))

        snafu = base_5_to_snafu(base_5)
        print(snafu)

        for digit in snafu:
            print(digit, end='')
        print()


            
        breakpoint()

def base_5_to_snafu(number):
    #reverse number, append extra digit in case of overflow
    number = number[::-1]
    number.append(0)

    for idx, digit in enumerate(number):

        #if 3 or larger increment next power and set negative
        if digit == 3:
            number[idx] = -2
            number[idx + 1] += 1

        elif digit == 4:
            number[idx] = -1
            number[idx + 1] += 1

        elif digit == 5:
            number[idx] = 0
            number[idx + 1] += 1

    #un-reverse number
    number = number[::-1]

    #construct snafu list of strings
    snafu = list()

    for digit in number:
        if digit == -2:
            snafu.append('=')

        elif digit == -1:
            snafu.append('-')

        else:
            snafu.append(str(digit))

    return snafu

def base_10_to_5(value):
    #number of digits required to represent value base 5
    nummber_len = int(log(value, 5)) + 1

    number = [0] * nummber_len

    while value > 0:
        #find exponent base 5
        exp = int(log(value, 5))

        #find the digit at that power of 5
        digit = value // 5**exp

        #set digit of exponent in number
        number[exp] = digit

        #decrement value
        value -= digit * 5**exp
        
    #reverse number
    number = number[::-1]

    return number

def base_5_to_10(number):
    value = 0
    exp = 0

    for digit in number[::-1]:
        value += digit * 5**exp
        exp += 1

    return value
         
if __name__ == "__main__":
    solve("test_input.txt")
    solve("input.txt")
