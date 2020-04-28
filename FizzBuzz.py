#!/bin/env python
#fizz Buzz
""" Silly fizz buzz program as a demo for conditionals. """

results = {'Fizz':0,
    'Buzz':0,
    'Fizz buzz':0,
    'Other':0
}

for num in range(1,101):
    if (num % 5 == 0) and (num % 3 == 0):
        print ("Fizz buzz")
        results['Fizz buzz']+=1
    elif num % 5 == 0:
        print ("Fizz")
        results['Fizz']+=1
    elif num % 3 == 0:
        print ("Buzz")
        results['Buzz']+=1
    else:
        print (num)
        results['Other']+=1

print (results)