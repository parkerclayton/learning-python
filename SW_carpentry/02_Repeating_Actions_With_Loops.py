#! /usr/bin/python


#counts number of vowels in the string and prints them
length = 0
for vowel in 'aeiou':
	length = length +1
print('There are', length, 'vowels')             

print(len('aeiou'))


#computes an exponent
for x in range(4):
	x=5**(x)
print(x)


#takes a string and reverses it
N="Parker"

for x in range(len(N)):
	y=len(N)-x
	str=N[y-1]
	print(str)