from ystream import *


abc = ySequence("a" , "b" , "c")

deff = ySequence("d" , "e" , "f")

ymap = yMapStream(lambda x : f"-{x}-")

abc + deff > ymap

items = [item for item in ymap]
expected = ["-a-","-b-","-c-","-d-","-e-","-f-",]

assert items == expected


ycap = yConcatStream()

abc >> ycap
deff >> ycap
ycap > ymap

items2 = [item for item in ymap]

assert items2 == expected


ghi = ySequence("g" , "h" , "i")

ymap = yMapStream(lambda x : f"-{x}-")

abc + deff+ghi > ymap

expected =  ['-a-', '-b-', '-c-', '-d-', '-e-', '-f-', '-g-', '-h-', '-i-']

items3 = [item for item in ymap]

assert items3 == expected

# TEST 4

abc = ySequence("a" , "b" , "c","d" , "e" , "f")



ymap = yMapStream(lambda x : f"-{x}-")
ymap2 = yMapStream(lambda x : f"+{x}+")
ymap3 = yMapStream(lambda x : f"*{x}*")

repeat = yMapStream(lambda x : x)

abc > ymap + ymap2 +ymap3 >repeat

items4 = [item for item in repeat]

expected = ['-a-', '-b-', '-c-', '-d-', '-e-', '-f-', '+a+', '+b+', '+c+', '+d+', '+e+', '+f+', '*a*', '*b*', '*c*', '*d*', '*e*', '*f*']

assert items4 == expected

