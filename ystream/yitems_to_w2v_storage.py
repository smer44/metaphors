from ystream.yabstract import yStream


class yItemstoW2VEntry(yStream):

    filter_variants  = {"noun","verb", "adj" ,"adv" }

    def __init__(self,
                 name_split = "_" ,
                 filterPOS = {"noun","verb",}):
        self.filterPOS = filterPOS



    def __iter__(self):
        filterPOS = self.filterPOS
        for vector in self.source:
            namepos = vector[0].strip()
            name, pos = namepos.split("_")
            name, pos = name.strip(),  pos.strip()
            if pos not in filterPOS:
                continue
            values = [float(x) for x in vector[1:]]
            yield name, values
