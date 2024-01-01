from ystream.yabstract import yStream

class ySpacyTokenStream(yStream):

    en = "en_core_web_sm"
    ru = 'ru_core_news_sm'

    def __init__(self,lang_name = ru, spacy_lib = None):
        self.init(lang_name,spacy_lib)

    def init(self, lang_name = ru, spacy_lib= None):
        if spacy_lib is None:
            import spacy
            spacy_lib = spacy

        self.spacy_lib = spacy_lib
        self.lang_name = lang_name
        self.spacy_lib.prefer_gpu()
        self.nlp = self.spacy_lib.load(self.lang_name)
        self.nlp.max_length = 1500000

    def __iter__(self):
        for text in self.source:
            doc = self.nlp(text)
            for n, sentence in enumerate(doc.sents):
                for token in sentence:
                    #yield from self.yield_root_clauses(token)
                    yield token

