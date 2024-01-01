from ystream.yabstract import yStream


class yStorageSimplest(yStream):

    def __init__(self,
                 store_before_iter=False,

                 ):
        self.store_before_iter = store_before_iter
        self.ngrams = dict()

    def store(self):
        if self.store_before_iter:
            raise RuntimeError("yStorageSimple.store: store called while it should hapen automatically: store_before_iter is set to True")

        self.__store__()

    def __store__(self):
        d = self.ngrams
        for key, value in self.source:
            self.store_item_simplest(d, key, value)

    def store_item_simple(self, d, key, value):
        row = d.setdefault(key, set())
        row.add(value)

    def __iter__(self):
        if self.store_before_iter:
            self.__store__()

        yield self










