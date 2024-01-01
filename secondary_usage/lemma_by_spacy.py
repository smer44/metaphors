import spacy


lang_name = 'ru_core_news_sm'

spacy.prefer_gpu()


nlp = spacy.load(lang_name)

filename = "../../metaphors/input/by_endings.txt"
encoding=  'utf-8'
outputname = "../../metaphors/input/mask_by_endings.txt"

with open(filename, 'r', encoding=encoding) as file:
    text = file.read()

doc = nlp(text)
masc = []
fem = []
neu = []

male_msg = "Gender=Masc"
female_msg = "Gender=Fem"
neutr_msg = "Gender=Neut"

for token in doc:
    if token.pos_ == "NOUN":
        morph = str(token.morph)
        word = token.lemma_
        if male_msg in morph:
            masc.append(word + "\n")

"""        elif female_msg in morph:
            fem.append(word)
        elif neutr_msg in morph:
            neu.append(word)"""

print(" - masc - ")

with open(outputname, 'w', encoding=encoding) as file:
    text = file.writelines(masc)



