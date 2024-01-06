import sys, os


#Macinton C
#Extension: mcs
#mcs -> c -> executable

c_commands = []
macinton_c_commands = []
modules_dir = ''

def get_args(line:str):
    out = []
    to_append = []
    is_string = 0
    for element in line:
        if element == '"' or element == "'":
            is_string = not is_string 
            to_append.append(element)
        else:
            if element == ':':
                if len(to_append) > 0:
                    if to_append[0] == ' ' and to_append[-1] == ' ':
                        out.append(string_array_sum(to_append[1:-1]))
                    elif to_append == ' ' and to_append[-1] != ' ':
                        out.append(string_array_sum(to_append[1:]))
                    else:
                        out.append(string_array_sum(to_append))
                to_append = []
            else:
                to_append.append(element)
    return out[1:]

def replace_with_args(line:str, args:list):
    global macinton_c_commands, c_commands
    was_args = 0
    line_array = list(c_commands[macinton_c_commands.index(line.split(' : ')[0].replace('\n', ''))])
    for i in range(len(line_array)):
        if line_array[i] == '%':
            line_array[i] = args[was_args]
            was_args += 1
    return string_array_sum(line_array)

def string_array_sum(array:list):
    out = ''
    for element in array:
        out += element
    return out

def module_load(path_to_module_script:str, modules_dir:str):
    global c_commands, macinton_c_commands
    with open(modules_dir + path_to_module_script) as module_script_reader:
        lines = module_script_reader.readlines()
    for line in lines:
        if line[0] == '#':
            with open('out.c', 'a') as append_include:
                append_include.write('#include <' + line[1:].replace('\n', '') + '>\n')
        else:
            line = line.split(' = ')
            macinton_c_commands.append(line[0].replace('\n', ''))
            with open(modules_dir + line[1].replace('\n', '')) as command_c:
                c_commands.append(string_array_sum(command_c.readlines()) + '\n')    
    
             
def compilation(file_path:str):
    global c_commands, macinton_c_commands, modules_dir
    is_commented = 0
    c_code = 0
    with open('out.c', 'w') as out_creation:
        pass
    with open(file_path) as script_reader:
        for line in script_reader.readlines():
            if not is_commented and line.replace('\n', '').replace(' ', '') != '':
                if line[0] == '@':
                    args = get_args(line.replace('\n', ''))
                    module_load(args[0], args[1])
                elif line[0] == '*':
                    c_code = not c_code
                elif c_code:
                    with open('out.c', 'a') as append_to_out:
                        append_to_out.write(line)  
                elif line[0] == '#' and not c_code:
                    with open('out.c', 'a') as append_to_out:
                        append_to_out.write(line[1:])
                elif line[0] == '$':
                    with open('out.c', 'a') as append_to_out:
                        append_to_out.write(replace_with_args(line[1:], get_args(line)))
                elif line[:2] == '//':
                    pass
                elif line[0] == '[':
                    is_commented = 1
                elif line[:2] != '//':
                    pass
                else:
                    pass
            else:
                if line[0] == ']':
                    is_commented = 0
    
if len(sys.argv) == 2:
    compilation(sys.argv[1])
    if os.path.getsize('out.c') > 0:
        if sys.platform == 'win32':
            os.system('gcc -o ' + string_array_sum(sys.argv[1].split('.')[:-1]) + '.exe ' + 'out.c')
        else:
            os.system('gcc -o' + string_array_sum(sys.argv[1].split('.')[:-1]) + ' out.c')
