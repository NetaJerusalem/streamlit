##5{"explain":"בתשובה התעלמו מירידות שורה ורווחים"}
import string

def start_in_letter(name: str):
    return name.startswith(tuple(string.ascii_letters))


def is_valid_name(name):
    if type(name) == str and start_in_letter(name):
        print(name)


is_valid_name("9avi")
is_valid_name("a3vi")
is_valid_name("avi")





##4{"explain":"`string.ascii_letters` contians all letters without numbers  of another signs"}
import string


def foo(word: str):
    for char in string.ascii_letters:
        if word.startswith(char):
            return char
    return ""


word = foo("nachman")
word += foo("4guy")
word += foo("eliau")
word += foo("tamer")
word += foo("aviv")
print(word)


##3 {"explain":"`str.startswith(STR_VAR)` Can receive a tuple with several letters, if the word starts with one of the letters it returns True", "playground":"print('ghe'.startswith('a','g'))"}

abc = "abc"
defg = "defg"
hij = "hij"

x = abc.startswith("a")
y = defg.startswith("b")
z = hij.startswith(("a", "b", "h"))
if x:
    print("Omer")
if y:
    print("Adam")
if z:
    print("Azili")


##2{}


def bla():
    return 3 < 450


def blabla():
    if bla():
        return 3 > 450


if blabla():
    print("blabla")
else:
    print("bla")



##1 {"explain":"`str.startswith(STR_VAR)` return True if the string starts with STR_VAR, else False", "playground":"print('abc'.startswith('a'))"}
abc = "abc"
defg = "defg"

x = abc.startswith("a")
y = defg.startswith("b")
if x:
    print("Maccabi")
if y:
    print("Hapoel")
