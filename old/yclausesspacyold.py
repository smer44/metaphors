
from yabstract import yStream

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
