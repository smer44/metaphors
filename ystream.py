import os
from yngrams import to_sorted_lists
from yabstract import yStream

encoding_std = "utf-8"
encoding_ru =   'cp1251'

def toystream(*items):
    obj = yStream()
    obj.iter_items = iter(items)
    return obj


class yOutputFileLinesStream(yStream):

    def __init__(self, encoding = encoding_std,append=False, printout=False):
        self.opts( encoding, append , printout)

    def opts(self, encoding, append=False, printout=False):
        self.encoding = encoding
        self.printout = printout
        self.mode  = 'a' if append else 'w'

    def save(self):
        self.before()
        for line in self.source:
            self.action(line)
        self.after()

    def before(self):
        self.file = open(self.filename,self.mode, encoding=self.encoding)
        print("yFileLinesSaver: saving file: " , self.filename, f", mode : {self.mode}")

    def after(self):
        self.file.close()

    def action(self,line):
        self.file.write(line)
        self.file.write('\n')
        if self.printout :
            print(line)

    def __gt__(self, other):
        self.filename = next(other)


class yFileNamesStream(yStream):

    def __init__(self,rootdir):
        self.init(rootdir)

    def init(self,rootdir):
        self.rootdir = rootdir

    def __iter__(self):
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                filepath = subdir + os.sep + file
                yield filepath




class yInputFileLinesStream(yStream):
    """
    Class what represents an input file stream of lines of this file,
    splitted by file.readlines(), stripped with line.strip() and
    empty strings are skipped
    init variables:
    - encoding
    - max_lines - amount of lines, read from the file. put negative value for all lines from a file
    """

    def __init__(self, encoding=encoding_std, max_lines = -1):
        self.opts(  encoding, max_lines)

    def opts(self,  encoding, max_lines = -1):
        self.encoding = encoding
        self.max_lines = max_lines

    def __iter__(self):
        for token in self.source:
            with (open(token, 'r', encoding=self.encoding) as file):
                print("yFileLinesLoader : loading file" , token)
                max_lines = self.max_lines
                for line in file.readlines():
                    line = line.strip()
                    if line:
                        if max_lines == 0:
                            break
                        max_lines -=1
                        yield line




class yFilterLastLineItemStream(yStream):

    def __init__(self,  split_symbol):
        self.opts(split_symbol)

    def opts(self, split_symbol):
        self.split_symbol = split_symbol

    def __iter(self):
        for line in self.source:
            items = line.split(self.split_symbol)
            yield items[-1]

class yUniqueStream(yStream):

    def __init__(self):
        self.last_hash = 0

    def __iter__(self):
        for item in self.source:
            this_hash = hash(item)
            if this_hash != self.last_hash:
                self.last_hash = this_hash
                yield item

class yNGramsLinesLoad:

    def __init__(self, split_key_value, split_list):
        self.conf(split_key_value,split_list)

    def conf(self, split_key_value, split_list):
        self.split_key_value = split_key_value
        self.split_list =split_list


    def __iter__(self):

        for line in self.source:
            line = line.strip()
            if line:
                key, vector = line.split(self.split_key_value, maxsplit = 1)
                key, vector = key.strip(), vector.strip()

                yield key, None, None
                for item_pair in vector.split(self.split_list):
                    item_pair = item_pair.strip()
                    item , weight = item_pair.split(self.split_key_value)
                    item, weight = item.strip(), weight.strip()
                    weight = int(weight)
                    yield None, item, weight


class yNGramsTagsLoad(yStream):

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



class yNGramsRawLoad(yStream):

    def __init__(self,  split_symbol,  noweight = False):
        self.init(split_symbol, noweight)

    def init(self, split_symbol, noweight):
        self.split_symbol = split_symbol
        #self.backwards = backwards
        self.noweight = noweight

    def store2(self):
        for line in self.source:
            items = line.split(self.split_symbol)
            items = [item.strip() for item in items]
            subject, verb, *objects = items
            key = subject
            yield key, None,None
            for object in objects:
                item = verb,object
                yield None, item, 1

    def __iter__(self):
        #backwards = self.backwards
        noweight = self.noweight
        expected_len = 2 if self.noweight else 3

        for line in self.source:
            items = line.split(self.split_symbol)
            items = [item.strip() for item in items]
            if len(items) != expected_len :
                continue

            if noweight:
                key, item  = items
                weight = 1
            else:
                #if backwards:
                #     item, key, weight = items
                #else:
                #    key, item,  weight = items
                key, item, weight = items
                weight = int(weight)

            yield key, item,  weight




class yDistancesLinesStream(yStream):

    def __init__(self,dictionary,trashhold):
        self.init(dictionary,trashhold)

    def init(self,dictionary,trashhold):
        self.dictionary = dictionary
        self.trashhold = trashhold

    def __iter__(self):
        d = self.dictionary
        trashhold = self.trashhold
        keys = list(d.keys())
        len_keys = len(keys)
        for i in range(len_keys-1):
            key = keys[i]
            value = d[key]
            output_vector = []
            for j in range(i+1,len_keys):
                next_key = keys[j]
                next_value = d[next_key]
                common_keys = value.keys() & next_value.keys()
                #distance = sum(min(value[x], next_value[x]) for x in common_keys)
                distance = len(common_keys)
                if distance > 0:
                    output_vector.append((next_key, distance))
            output_vector = sorted(output_vector, key=lambda pair: -pair[1])
            output_vector = output_vector[:trashhold]
            line = self.format_output(key, output_vector)
            if line:
                yield line

    def format_output(self, key, value_pairs):
        if value_pairs:
            formatted_value = ",".join(f"{pair[0]}:{pair[1]}" for pair in value_pairs)
            line = f"{key}:{formatted_value}\n"
            return line


class yNgramToLinesStream(yStream):


    def __iter__(self):
        for key, vector in self.source:
            if vector:
                formatted_vecor = ",".join(f"{item}" for item in vector)
                line = f"{key}:{formatted_vecor}\n"
                yield line






class yClausesSpacy(yStream):

    en = "en_core_web_sm"
    ru = 'ru_core_news_sm'

    def __init__(self,lang_name, spacy_lib = None):


        self.init(lang_name,spacy_lib = None)

    def init(self, lang_name , spacy_lib):
        if spacy_lib is None:
            import spacy
            spacy_lib = spacy

        self.spacy_lib = spacy_lib
        self.lang_name = lang_name
        self.spacy_lib.prefer_gpu()
        self.nlp = self.spacy_lib.load(self.lang_name)

    def __iter__(self):
        for text in self.source:
            doc = self.nlp(text)
            for n, sentence in enumerate(doc.sents):
                for token in sentence:
                    #yield from self.yield_root_clauses(token)
                    yield from self.yield_token_child_pairs(token)

    def yield_token_child_pairs(self,token):
        children = list(token.children)
        for child in children:
            yield f"{token.lemma_}|{token.pos_}|{token.dep_} ~ {child.lemma_}|{child.pos_}|{child.dep_}"

    def yield_root_clauses(self, root_token):
        if root_token.dep_ != "ROOT": return
        stack = [(root_token,0)]
        while stack:
            token,depth = stack.pop()
            children = list(token.children)
            #remove unclassifyed dependencies:
            skip = False
            objects = []
            verb = None
            subject = None
            if  token.pos_ == "VERB":
                verb =  token.lemma_
            for child in children:
                if (child.pos_ == "NOUN" or child.pos_ == "PRON"or child.pos_ == "PROPN") and child.dep_ == "nsubj":
                    subject =child.lemma_
                if ((child.pos_ == "NOUN" or child.pos_ == "PRON"or child.pos_ == "PROPN") and (child.dep_ == "obj" or child.dep_ == "obl")) or  \
                    (child.pos_ == "VERB" and child.dep_ == "xcomp" ):
                    objects.append(child.lemma_)

            if subject and verb and objects:
                yield "|".join( (subject , verb, *objects))
            children.reverse()
            depth+=1
            for child in children:
                stack.append((child,depth ))



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



