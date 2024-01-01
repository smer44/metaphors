from ystream.yabstract import yStream

class yLinesToSimpleOntology(yStream):

    def __init__(self):
        self.key_value_split = ":"
        self.sequence_split = ","
        self.backwards_marker= "@"


    def __iter__(self):
        key_value_split = self.key_value_split
        sequence_split =self.sequence_split
        backwards_marker =self.backwards_marker

        for line in self.source:
            if line:
                line = line.lower()
                key, value = line.split(key_value_split)
                key, value = key.strip(), value.strip()
                items = key.split(sequence_split)
                items =[item.strip() for item in items]
                keys, relation = items[:-1], items[-1]
                values = value.split(sequence_split)
                values = [item.strip() for item in values]
                if relation[-1] == backwards_marker:
                    backwards_relation = relation[:-1]
                else:
                    backwards_relation = relation + "@"

                for key in keys:
                    if key:
                        for value in values:
                            if value:
                                yield key, (value, relation), 1
                                yield value, (key, backwards_relation), 1






