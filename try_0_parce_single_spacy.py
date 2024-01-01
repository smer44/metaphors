"""
POS: NOUN , DEP: obl - обстоятельство с предлогом
advcl : adverbial clause modifie - внутреннее предложение
"SCONJ": "subordinating conjunction", mark - marker,

если завтра будет солнечно - солнечно adj root или advcl как вложенное


advmod -  наречие типа "завтра"

amod - прилагательное

"""


import spacy
from spacy.matcher import Matcher
from spacy import displacy
#from  ystream import *
#from yngrams import yNgramsDict

#file_name = ySequence("../datasets/my_gpt/facts_gpt.txt")
#file_lines = yInputFileLinesStream()

#file_name > file_lines



text = "Земля – это огромный шар, на поверхности которого расположены суши и водные пространства."

text = """ Мужчина, видимо оттого, что поспешно отхлёбывает кофе, беспрерывно дымя сигаретой, поперхнулся и выпускает дым через ноздри. 
Взгляд женщины остаётся абсолютно безучастным. 
Оба они - это видно с первого взгляда - совсем ещё не привыкли друг к другу, как к новой выходной одежде.
"""

text = "Жили-были в давние времена в маленькой деревне на берегу глубокого озера старик и старуха."
"""Я разбиваю камень.
Я разбиваю молотком.
Я разбиваю в лесу.


Если пойдёшь, то придёшь.
Если завтра будет солнечно, то мы пойдем на пикник.

Стол из дерева: это означает, что стол сделан из дерева.
Рабочий стол: это стол, который используется для работы.


Чтобы печь пирог, нужно приготовить тесто.
Для победы в соревновании, следует тренироваться каждый день."""


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

text = "эти типы стали есть на складе"
text = "И тем не менее тысячелетия исполины человеческой мысли снова и снова комментировали Писание, раскрывая все более глубокие его слои ."
#morph : Aspect=Imp|Mood=Ind|Number=Plur|Tense=Past|VerbForm=Fin|Voice=Act
text = "В книге критически разбирается историческая канва Евангелий и дается исторически обоснованная версия изложенных в них событий ."


doc = nlp(text)
#result = matcher(doc,as_spans = True)
#print(result)

#for text in file_lines:
#    doc = nlp(text)
#    result = matcher(doc,as_spans = True)
#    print(result)

#def match_bi_rule(token,rule):
#    children = list(token.children)


for n, sentence in enumerate(doc.sents):
    for token in sentence:
       print(token , ", POS:" , token.pos_, ", DEP:" , token.dep_ ,"morph :", token.morph ," Children:", list(token.children))

#displacy.serve(doc, style = "dep")