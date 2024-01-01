from  ystream import *
from yngrams import yNgramsTagDict , yNgramsSimpleDict
import spacy

input_file = ySequence("../datasets/my_out/out_facts_gpt.txt")

file_lines = yInputFileLinesStream()

tag_pairs = yNGramsTagsLoad()

#ngdict = yNgramsSimpleDict()
ngdict =  yNgramsTagDict()

input_file>file_lines>tag_pairs > ngdict


#print(spacy.explain("advcl"))

ngdict.store_tags()

#for pair in ngdict:
#    print(pair)
key = None#"полуостров"
vroot_tag = 'VERB ROOT'


print(" ".join(ngdict.random(vroot_tag, key)))

#print(ngdict.tag_pairs[vroot_tag])

