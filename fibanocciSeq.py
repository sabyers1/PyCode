#fibanocci sequence
# b = a+b

a, b = 0 , 1
for i in range(1,20):
    print a
    a , b = b, a + b

#Fibonacci Generator
#yield is a generator
def fib(num):
    a,b = 0,1
    for i in xrange(0,num):
        yield "{}: {}".format(i+1, a)
        a, b = b, a + b

for item in fib(10):
    print(item)