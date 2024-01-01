from yabstract import yStream

class yNGramsWithTagsLoad(yStream):

    def __init__(self, item_split ="~", tag_split = "|"):
        self.init(item_split,tag_split)

    def init(self, item_split="~", tag_split = "|"):
        self.item_split = item_split
        self.tag_split = tag_split

    def __iter__(self):
        item_split = self.item_split
        tag_split = self.tag_split


        for line in self.source:
            items = line.split(item_split)
            items = [item.strip() for item in items]
            key, value = items
            key_name, *key_tags =key.split(tag_split)
            value_name, *value_tags =value.split(tag_split)
            yield key_name,key_tags,value_name,value_tags
