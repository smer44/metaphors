from ystream.yabstract import yStream


class yItemsSimpleFillWeight(yStream):

    def __init__(self, fill_weight = 1):
        self.fill_weight  = fill_weight

    def __iter__(self):
        fill_weight = self.fill_weight
        for items in self.source:
            yield *items, 1

class yItemsToKeyValueEntry(yStream):

    def __init__(self,
                 inverse = False,
                 fill_weight = 1,
                 weight_to_int = True):
        self.inverse = inverse
        self.fill_weight = fill_weight
        self.weight_to_int = weight_to_int


    def __iter__(self):
        fill_weight = self.fill_weight
        weight_to_int = self.weight_to_int
        if fill_weight is None or fill_weight is False:
            if weight_to_int:
                if self.inverse:
                    for key, value, weight in self.source:
                        weight = int(weight)
                        yield value, key, weight
                else:
                    for key, value, weight  in self.source:
                        weight = int(weight)
                        yield key, value, weight

            else:

                if self.inverse:
                    for key, value, weight in self.source:
                        yield value, key, weight
                else:
                    for key, value, weight  in self.source:
                        yield key, value, weight
        else:
            if self.inverse:
                for key, value, *rest in self.source:
                    yield value,key, fill_weight
            else:
                for key,  value, *rest in self.source:
                    yield key, value, fill_weight

class yItemsToSimpleEntryDoubleValue(yStream):

    def __init__(self, forwards = True, backwards = False, fill_relation = None,enclause = True):
        self.forwards = forwards
        self.backwards = backwards
        self.fill_relation = fill_relation
        self.enclause = enclause

    def __iter__(self):
        forwards = self.forwards
        backwards = self.backwards
        fill_relation = self.fill_relation
        enclause = self.enclause

        if forwards or backwards:
                for items in self.source:
                    items = self.fill_if_need(items)
                    if items:
                        key, relation, noun = items
                        if forwards:
                            if enclause:
                                yield key, (noun, relation), 1
                            else:
                                yield key, noun, relation, 1
                        if backwards:
                            if enclause:
                                yield noun, (key, relation), 1
                            else:
                                yield key, noun, relation, 1



    def fill_if_need(self,items):
        if len(items) == 2:
            return items[0], self.fill_relation, items[1]
        elif len(items) == 3:
            return items
        else:
            return None






class yItemsFilterByFirstItem(yStream):

    def __init__(self, first_item , weight_absent = True):
        self.first_item = first_item
        self.weight_absent = weight_absent

    def __iter__(self):
        first_item = self.first_item
        weight_absent = self.weight_absent
        for items in self.source:
            if items[0] == first_item:
                items = items[1:]
                if weight_absent:
                    yield *items,1
                else:
                    yield items





class yItemsFilterToMultiEntry(yStream):

    def __init__(self,invert_marker = None, multiple_values = False, weight_absent = True):
        self.invert_marker = invert_marker
        self.multiple_values = multiple_values
        self.weight_absent = weight_absent



    def __iter__(self):
        invert_marker = self.invert_marker
        multiple_values = self.multiple_values
        weight_absent = self.weight_absent
        for items in self.source:
            if weight_absent:
                weight = 1
                if multiple_values:
                    key1, key2, *value = items
                else:
                    key1, key2, value = items
            else:
                if multiple_values:
                    key1, key2, *value,weight = items
                    weight = int(weight)
                else:
                    key1, key2, value,weight = items
                    weight = int(weight)

            yield key1, key2, value, weight
            if invert_marker:
                yield value, key2+invert_marker, key1,weight
