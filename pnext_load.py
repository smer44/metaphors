uniques = {"Cardinality" , "Required"}

text = """
class Organization ## объявление структуры класса организация 
    director 1! ## объявление что у класса обязательно должно быть одно поле директор
    admin 1!..3  ## объявление что у класса обязательно должно быть одно поле админ но максимум 3
     
    manager * ## объявление что у класса может быть любое 0-n число менеджеров 
    worker + ##объявление что у класса может быть любое 1-n число менеджеров 
"""

instance_text = """
Organization: test organisation
    director : ivanov
    admin : petrov
    admin : sidorov
    manager : michailov

"""


class Entity:

    def __init__(self, type, valuetype):
        self.type = type
        self.valuetype = valuetype
        self.children = []

    def repr(self,old_indent = "", indent = "\t" ) :
        msg = f"{old_indent}type:<{self.type}>, valuetype:<{self.valuetype}>\n"
        child_indent = old_indent + indent
        for child in self.children:
            if isinstance(child, tuple):
                msg += f"{child_indent}{child[0]} :{child[1]}\n"
            else:
                msg+= child.repr(child_indent, indent)
        return msg

    def deep_match(self, entity):
        pass




import pprint as pp
def ylspaces(line):
    look_for_whitespaces = True
    line_index = 0
    spaces_count = 0

    while look_for_whitespaces:
        if line[line_index] == "\t":
            spaces_count += 4
        elif line[line_index] == " ":
            spaces_count +=1
        else:
            break
        line_index+=1
    return line[line_index:] , spaces_count


rootobj = dict()#Entity("root" , "root")
obj = rootobj
stack = []
old_spaces_count = 0
old_key, old_value = None, None

def multiput(d,key, value):
    if key is None:
        return
    if key not in d:
        d[key] = value
        return
    old_value = d[key]
    if isinstance(old_value,list):
        old_value.append(value)
    else:
        d[key] = [old_value, value]


for line in text.split("\n"):

    if line:
        line = line.rstrip()
        line = line.split("#",1)[0]
        line, spaces_count = ylspaces(line)
        key, value = line.split(":",1)
        print(spaces_count , key , " - - " , value)
        if spaces_count > old_spaces_count:
            #inner_entity = Entity(old_key, old_value)
            inner_dict = dict()
            #inner_dict["_type"] = old_key
            inner_dict["_name"] = old_value

            stack.append((obj,old_spaces_count))

            #obj.children.append(inner_entity)
            multiput(obj,old_key,inner_dict)
            #obj.setdefault(old_key, []).append( inner_dict)
            obj = inner_dict
            old_spaces_count = spaces_count
            old_key, old_value = key, value
        elif spaces_count < old_spaces_count:
            #if old_key:
            #    obj.setdefault(old_key, []).append( old_value)
            multiput(obj, old_key, old_value)
            obj, old_spaces_count = stack.pop()
            old_key, old_value = key, value

        else:
            #if old_key:
                #obj.children.append((old_key, old_value))
            #    obj.setdefault(old_key, []).append(old_value)
            multiput(obj, old_key, old_value)
            old_key, old_value = key, value

            #print(line, spaces_count)

#print(rootobj.repr())
pp.pprint(rootobj)


