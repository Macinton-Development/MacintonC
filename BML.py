def array_of_strings_sum(array:list, parse=''):
    out = ''
    for element in array:
        out += element + parse
    return out

def parse(line:str):
    out = []
    to_append = []
    is_string = 0
    for element in line:
        if element == '"':
            is_string = not is_string 
            to_append.append(element)
        else:
            if element == ';':
                if len(to_append) > 0:
                    if to_append[0] == ' ' and to_append[-1] == ' ':
                        out.append(array_of_strings_sum(to_append[1:-1]).replace('\n', ''))
                    elif to_append == ' ' and to_append[-1] != ' ':
                        out.append(array_of_strings_sum(to_append[1:]).replace('\n', ''))
                    else:
                        out.append(array_of_strings_sum(to_append).replace('\n', ''))
                to_append = []
            else:
                to_append.append(element)
    return out

def get_contents(path:str) -> dict:
    with open(path, newline='', encoding='utf-8') as reader:
        contents = reader.readlines()
    out = {}
    for element in contents:
        data = parse(element)
        out[data[0]] = data[1:]
    return out

def add(path:str, add:str): 
    with open(path, 'a') as adder:
        adder.write(add + '\n')
    
def add_to_var(path:str, name:str, add:list):
    contents = get_contents(path)
    if name not in  contents:
        contents[name] = []
    for element in add:
        contents[name].append(element)
    with open(path, 'w', encoding='utf-8') as writer:
        for element in contents:
            writer.write(element + ';' + array_of_strings_sum(contents[element], parse=';') + '\n')
