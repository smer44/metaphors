from ystream import *

abc = ySequence("a" , "b" , "c")

deff = ySequence("d" , "e" , "f")

ghi = ySequence("g" , "h" , "i")

ymap = yMap2Stream(lambda x,y : f"-{x}-{y}-")

ymap2 = yMap2Stream(lambda x,y : f"+{x}+{y}+")


abc*deff >=ymap > ymap2

ghi >> ymap2


items = [item for item in ymap2]
expected = ['+-a-d-+g+', '+-b-e-+h+', '+-c-f-+i+']

assert items == expected


#abc*deff *deff>=ymap > ymap2