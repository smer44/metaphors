from ystream.yabstract import yStream


class ySplitSimpleStream(yStream):
    """
    Splits the strings in a stream on items with
    basic python .split() function.
    Also will turn all symbols to lowercase
    - split_symbol - symbol, by what each item is split
    - split_len - expected split length. If specified, the stream will
    return only those split results, what has given length
    -  selection - having items result, select items[selection] from it
    """

    def __init__(self,  split_symbol,
                 split_len = None,
                 selection_from = None,
                 selection_to=None,
                 tolower= True ):
        self.opts(split_symbol,
                  split_len,
                  selection_from,
                  selection_to,
                  tolower)

    def opts(self, split_symbol,
             split_len = None,
             selection_from=None,
             selection_to=None,
             tolower= True):
        self.split_symbol = split_symbol
        self.selection_from = selection_from
        self.selection_to = selection_to
        self.split_len = split_len
        self.tolower = tolower

    def __iter__(self):
        split_symbol = self.split_symbol
        #selection = self.selection
        split_len = self.split_len
        tolower = self.tolower
        selection_from = self.selection_from
        selection_to = self.selection_to

        for line in self.source:
            items = line.split(split_symbol)
            if split_len is None or len(items) == split_len:
                if tolower:
                    items = [item.strip().lower() for item in items]
                else:
                    items = [item.strip() for item in items]

                if selection_from :
                    if selection_to:
                        yield items[selection_from:selection_to]
                    else:
                        yield items[selection_from:]
                else:
                    if selection_to:
                        yield items[:selection_to]
                    else:
                        yield items
