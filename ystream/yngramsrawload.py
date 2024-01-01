from yabstract import yStream

class yNGramsRawLoad(yStream):

    def __init__(self,  split_symbol,  noweight = False):
        self.init(split_symbol, noweight)

    def init(self, split_symbol, noweight):
        self.split_symbol = split_symbol
        self.noweight = noweight

    def store2(self):
        for line in self.source:
            items = line.split(self.split_symbol)
            items = [item.strip() for item in items]
            subject, verb, *objects = items
            key = subject
            yield key, None,None
            for object in objects:
                item = verb,object
                yield None, item, 1

    def __iter__(self):
        #backwards = self.backwards
        noweight = self.noweight
        expected_len = 2 if self.noweight else 3

        for line in self.source:
            items = line.split(self.split_symbol)
            items = [item.strip() for item in items]
            if len(items) != expected_len :
                continue
            if noweight:
                key, item  = items
                weight = 1
            else:
                key, item, weight = items
                weight = int(weight)

            yield key, item,  weight
