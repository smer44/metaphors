from ystream.yabstract import yStream


class yStorageW2V(yStream):

    def __init__(self,store_before_iter = True ):
        self.words = list()
        self.matrix = list()
        self.store_before_iter = store_before_iter


    def store(self):
        for name, values in self.source:
            self.words.append(name)
            self.matrix.append(values)

    def __iter__(self):
        yield self

    def pp(self):
        print(" - yStorageW2V -")
        for word, vector in zip(self.words,self.matrix):
            print(word,vector)

