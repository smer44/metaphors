from ystream.yabstract import yStream


class ySplitStream(yStream):

    def __init__(self, skip = " \t\r\n" , keep = ".,:;-!?'\"", lookupLen = 256):
        self.init(skip, keep, lookupLen)


    def init(self, skip = " \t\r\n" , keep = ".,:;-!?'\"", lookupLen = 256):
        lookup = [0 for _ in range(lookupLen)]
        self.lookup = lookup
        for c in skip:
            lookup[ord(c)] = 1

        for c in keep:
            lookup[ord(c)] = -1

    def __iter__(self):
        lookup = self.lookup
        lookup_len = len(lookup)
        for text in self.source:
            assert isinstance(text, str)
            begin = 0
            for n, c in enumerate(text):
                ordc = ord(c)
                flag = lookup[ordc] if ordc < lookup_len else 0
                if flag != 0 :
                    if n > begin:
                        yield text[begin:n]
                    begin = n+1
                    if flag < 0 :
                        yield c
