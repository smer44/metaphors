
import os
import pprint as pp


def load_dict_folder(folder_path):
    dictionary = dict()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            tags = str(file_path).split("\\")[1:]
            if tags:
                file_tag = tags.pop()
                pair = file_tag.split(".")
                if len(pair) != 2:
                    print(f"file name is wrong : {file_path}")
                    continue
                file_name , extention = pair
                if extention != "txt":
                    continue
                file_tag = file_name.split()
                tags.extend(file_tag)
            tags = set(tags)
            #print(file, tags)
            load_words_from_file(file_path,tags,dictionary)
    return dictionary

def load_words_from_file(file_path,file_tags,dictionary):
    with open(file_path, "r", encoding='utf-8') as file:
        current_tags = file_tags
        for line in file.readlines():
            line = line.strip()
            if line:
                if line[0] == "-":
                    # it is a tag line
                    line_tags = set(word.strip() for word in line[1:].split())
                    current_tags = file_tags.union(line_tags)
                    # print("ney line tags :", current_tags)
                elif line[0] == "#":
                    pass
                else:
                    line = line.lower()
                    dictionary[line] = current_tags


dictionary = load_dict_folder("dictionaries")

print("dictionary size : ", len(dictionary))
pp.pprint(dictionary)

def read_file_to_words(file_name):
    #TODO - not supported ""
    words = []
    with open(file_name, "r", encoding='utf-8') as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                line = line.replace("," , " ")
                line = line.replace(".", " ")
                line = line.replace("!", " ")
                line = line.replace("?", " ")
                line_words = [word.strip() for word in  line.split()]
                words.extend(line_words)
    return words



def read_file_to_stammings(file_name):
    stammings = dict()
    with open(file_name, "r", encoding='utf-8') as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                line_words = [word.strip() for word in line.split()]
                assert(len(line_words)) == 2 , f"load_stammings: wrong line in stamming file : {line}"
                changed_word, stam_word = line_words
                stammings.setdefault(changed_word, set()).add(stam_word)
    return stammings








def check_known(dictionary, stammings, words):
    for word in words:
        word = word.lower()
        if word in dictionary:
            continue
        possible_stammings = stammings.get(word, [])
        for word_variant in possible_stammings:
            if word_variant in dictionary:
                break
        else:
            raise ValueError(f"word {word} and possible stammings {possible_stammings} are  not in dictionary")


words = read_file_to_words("../datasets/dummy_text.txt")
stammings = read_file_to_stammings("russian_stamming.txt")

check_known(dictionary,stammings, words)
