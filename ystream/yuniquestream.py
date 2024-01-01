from ystream.yabstract import yStream

class yUniqueStream(yStream):

    def __init__(self):
        self.last_hash = 0

    def __iter__(self):
        for item in self.source:
            this_hash = hash(item)
            if this_hash != self.last_hash:
                self.last_hash = this_hash
                yield item