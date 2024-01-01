from ystream.yabstract import yStream


class yStorageMultipletOld(yStream):

    def __init__(self,*markers):
        self.init(*markers)
        self.iter_marker = "SVO"

    def init(self,*markers):
        self.multi_dict = {marker : dict() for marker in markers}


    def store(self):
        multi_dict = self.multi_dict
        for marker,key1,key2,item in self.source:
            key = (key1,key2)
            self.store_item_counted(multi_dict[marker],key,item, 1)


    def __iter__(self):
        self.store()
        yield self.multi_dict[self.iter_marker]




    def store_item_counted(self,d,key,item,add_weight):
        row = d.setdefault(key, dict())
        weight = row.setdefault(item, 0)
        row[item] = weight+add_weight



