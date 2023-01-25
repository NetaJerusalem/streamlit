##1 {"key":"value","more_key":["list", "of", "values"],"and_more_key":[{"dict":1,"of":False,"data":True}]}
def foo():
    print("foo")

foo()


##2   {"key":"value","more_key":["list", "of", "values"],"and_more_key":[{"dict":1,"of":False,"data":True}]}
def foo():
    return "foo"


def boo():
    print("boo")


foo()
boo()

##3
def plus(x, y): 
    return x + y


def print_plus(x, y):
    print(x + y)


plus(1, 2)
print_plus(3, 4)

##4
def foo():
    return 10


def plus(x, y):
    return x + y


print(plus(foo(), 1))

##5

def print_plus(x, y):
    print(x + y)


num = 10
num_2 = 1+1

print_plus(num, num_2)

##6
def foo(text):
    return text * 3


num = int(foo("1"))
print(num + 222)

##7


def boo():
    print("boo")

f = boo
f()


##8
def foo(text):
    return text.replace("A", "B")


def ABC():
    return "ABC"


print(foo(ABC()))

##9
def plus(x, y):
    return x + y


def print_plus(x, y):
    print(x + y)


num = plus(1, 1)
num_2 = plus(2, 2)

print_plus(num, num_2)

##10
def boo(f):
    f()


def print_hello():
    print("hello")


boo(print_hello)

##11
def foo(text):
    return text.replace("boo", "foo")


def boo(text):
    return text + "boo"


print(foo(boo("foo")))

##12
def plus(x, y):
    return x + y


def print_plus(x, y):
    print(x + y)


print_plus(plus(1, 2), 4)


##13
def boo(f):
    print(f())


def foo():
    return "foo"


boo(foo)
