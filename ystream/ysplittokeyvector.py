from ystream.yabstract import yStream


class yKeyVectorToKeyValueWeightStream(yStream):


    def __init__(self):
        pass

    def __iter__(self):

        for key, vector in self.source:
            for value,weight in vector.items():
                yield key,  value, weight


class ySplitKeyVector(yStream):
    """splits strings in form
    время:день:26,работа:26,история:26,дело:25,жизнь:25,разговор:25,путь:25,операция:25,люди:24,дорога:24,группа:24,встреча:24,школа:24,праздник:24,человек:23,суд:23,город:23,выбор:23,период:23,программа:23,бой:23,игра:23,самолет:23,служба:23,срок:23,час:23,врач:23,поездка:23,команда:23,поезд:23
    key , dict( key: value)
    """


    def __init__(self,
                 main_key_split_symbol = ":",
                 items_split_symbol = ",",
                 inner_key_split_symbol = ":",
                 tolower= True,
                 weightConvertFn= int):

        self.init(main_key_split_symbol, items_split_symbol, inner_key_split_symbol,tolower,weightConvertFn)


    def init(self, main_key_split_symbol = ":", items_split_symbol = ",", inner_key_split_symbol = ":",tolower= True,weightConvertFn= int):
        self.main_key_split_symbol = main_key_split_symbol
        self.items_split_symbol = items_split_symbol
        self.inner_key_split_symbol = inner_key_split_symbol
        self.tolower = tolower
        self.weightConvertFn = weightConvertFn

    def __iter__(self):
        main_key_split_symbol = self.main_key_split_symbol
        items_split_symbol = self.items_split_symbol
        inner_key_split_symbol = self.inner_key_split_symbol
        tolower = self.tolower
        weightConvertFn = self.weightConvertFn

        for line in self.source:
            line = line.strip()
            if line:
                if tolower:
                    line = line.lower()
                #result = line.split(main_key_split_symbol, 1)
                #print("-", result)
                key, vector = line.split(main_key_split_symbol,1)
                key = key.strip()
                vector = vector.strip()
                if key and vector:
                    items = vector.split(items_split_symbol)
                    d = dict()
                    for item in items:
                        if item:
                        #print(" - split -" , item , "by " , inner_key_split_symbol)
                            item_split = item.split(inner_key_split_symbol)
                            #inner_key, value = item.split(inner_key_split_symbol)
                            if len(item_split) == 2:
                                inner_key, value = item_split

                                if weightConvertFn:
                                    value = weightConvertFn(value)
                                assert inner_key not in d , f"inner_key:{ inner_key} not in d"
                                d[inner_key] = value
                            else:
                                print(" wrong split for items :  " , items)
                    yield key, d


