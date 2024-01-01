from ystream.yabstract import yStream


class yBag(yStream):

    def __init__(self,noweight = True ):
        self.bag = dict()
        self.noweight = noweight

    def store(self):
        bag = self.bag
        if self.noweight:
            for item in self.source:
                self.add_to_bag(bag,item,1)
        else:
            for item,weight in self.source:
                self.add_to_bag(bag,item,weight)

    def exclude(self):
        bag = self.bag
        if self.noweight:
            for item in self.source:
                if item in bag:
                    del bag[item]



    def add_to_bag(self,bag, key, weight):
        bag[key] = bag.get(key,0)+ weight


    def addall(self,other):
        bag = self.bag
        if isinstance(other, yBag):
            otherdict = other.bag
        elif isinstance(other, dict):
            otherdict =other
        else:
            raise ValueError(f"yBag.addall : wrong tye of other: {type(other)}")
        for item,weight in otherdict.items():
            self.add_to_bag(bag, item, weight)

    def __iter__(self):
        for item in self.bag:
            yield item

