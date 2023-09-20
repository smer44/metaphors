import spacy
from spacy.matcher import Matcher
from spacy import displacy
from  ystream import *
from yngrams import yNgramsDict

file_name = toystream("../datasets/my_gpt/facts_gpt.txt")
file_lines = yInputFileLinesStream()

file_name > file_lines


text = "Земля – это огромный шар, на поверхности которого расположены суши и водные пространства."

#text = "Пещеры – это полости в скалах, образовавшиеся в результате долгого воздействия воды."
#roow is POS: NOUN , DEP: ROOT , what has direct attributes POS: NOUN , DEP: nsubj  with child - and part eto

#text = "Водоемы, такие как озера и реки, образуются из скопления воды в низинных местах земной поверхности."#verb based

#text = "Геологические процессы, такие как плиточные тектонические движения, формируют земную поверхность."#processes form surface
ru = 'ru_core_news_sm'

#text = "Прошлые процессы"
nlp = spacy.load(ru)

#matcher = Matcher(vocab = nlp.vocab)

takie_kak_rule = [{"POS":"DET", "DEP": "det" } , {"POS": "SCONJ" , "DEP": "case"}]

#matcher.add("takie_kak_rule", patterns = [takie_kak_rule])

my_bi_rule = {(("pos_","NOUN"),): (("pos_", "ADJ") , ("dep_", "amod") ) }

doc = nlp(text)
#result = matcher(doc,as_spans = True)
#print(result)

#for text in file_lines:
#    doc = nlp(text)
#    result = matcher(doc,as_spans = True)
#    print(result)

def match_bi_rule(token,rule):
    children = list(token.children)


for n, sentence in enumerate(doc.sents):
    for token in sentence:
       print(token , ", POS:" , token.pos_, ", DEP:" , token.dep_ , ", Children:", list(token.children))

#displacy.serve(doc, style = "dep")