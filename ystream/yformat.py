from ystream.yabstract import yStream

def format_dict_to_line(d, join_symbol):
    return join_symbol.join(f"{key[0]}, {key[1]}: {value}" for key, value in d.items() )

class yFormatItemsToString(yStream):

    def __init__(self,join_string = " "):
        self.join_string = join_string

    def __iter__(self):
        join_string = self.join_string
        for items in self.source:
            yield join_string.join(items)




class yFormatKeyDictDuoToString(yStream):

    def __init__(self, kv_symbol = "~",join_symbol = "; "):
        self.kv_symbol = kv_symbol
        self.join_symbol =join_symbol

    def __iter__(self):
        kv_symbol = self.kv_symbol
        join_symbol = self.join_symbol
        for key, d in self.source:
            value_str = format_dict_to_line(d,join_symbol)
            yield f"{key}{kv_symbol}{value_str}"
