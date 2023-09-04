text = """
Organization: Model: @Organization.Apla
    Cardinality: 1 ## может быть создан только 1 индивид
    Role: director
        Cardinality: 1
        Required: 1

    Role: admin
        Cardinality: 3
        Required: 1
    Role: manager
        Cardinality: 0
"""

"""
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


rootobj = Entity("root" , "root")
obj = rootobj
stack = []
old_spaces_count = 0
old_key, old_value = None, None
for line in text.split("\n"):

    if line:
        line = line.rstrip()
        line = line.split("#",1)[0]
        line, spaces_count = ylspaces(line)
        key, value = line.split(":",1)
        print(spaces_count , key , " - - " , value)
        if spaces_count > old_spaces_count:
            inner_entity = Entity(old_key, old_value)

            stack.append((obj,old_spaces_count))

            obj.children.append(inner_entity)
            obj = inner_entity
            old_spaces_count = spaces_count
            old_key, old_value = key, value
        elif spaces_count < old_spaces_count:
            if old_key:
                obj.children.append((old_key, old_value))
            obj, old_spaces_count = stack.pop()
            old_key, old_value = key, value

        else:
            if old_key:
                obj.children.append((old_key, old_value))
            old_key, old_value = key, value

            #print(line, spaces_count)

print(rootobj.repr())


