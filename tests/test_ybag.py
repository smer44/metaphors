from ystream import  *


items = ySequence("a" , "b" , "c", "d", "e")

ex = ySequence("b", "c")


ybag = yBag()

items > ybag

ybag.store()

assert ybag.bag == {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1}

#print("after store " , ybag.bag)

ex > ybag

ybag.exclude()

#print("after exclude " ,ybag.bag)

assert ybag.bag == {'a': 1, 'd': 1, 'e': 1}




