import sys, os


#Macinton C
#Extension: mcs
#mcs -> c -> executable

c_commands = []
macinton_c_commands = []
modules_c = []
modules_dir = ''
watchers = []
watching = {}

def get_args(line:str):
    global watchers, watching
    out = []
    to_append = []
    is_string = 0
    for element in line:
        if element == '"':
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

    if out[0][1:-1] in watchers:
        return [out[1:], 1]
    return [out[1:]]

def replace_with_args(line:str, args:list):
    global macinton_c_commands, c_commands
    was_args = 0
    line_array = list(c_commands[macinton_c_commands.index(line.split(' : ')[0].replace('\n', ''))])
    for i in range(len(line_array)):
        if line_array[i] == '%':
            line_array[i] = args[was_args]
            was_args += 1
    return string_array_sum(line_array)

def block_launch(name:str):
    with open('out.c', 'a') as append_block_launch:
        append_block_launch.write(name + '()\n')

def string_array_sum(array:list):
    out = ''
    for element in array:
        out += element
    return out

def module_load(path_to_module_script:str, modules_dir:str, _is_header=False):
    global c_commands, macinton_c_commands, modules_c, watchers, watching
    with open(modules_dir + path_to_module_script) as module_script_reader:
        lines = module_script_reader.readlines()
    for line in lines:
        if line[0] == '#' and ((module := line[1:].replace('\n', '')) not in modules_c or not _is_header):
            if not _is_header:
                modules_c.append(module)
            with open('out.c', 'a') as append_include:
                if not _is_header:
                    append_include.write('#include <' + module + '>\n')
        elif line[0] == ';':
            watchers.append(line[1:].replace('\n', ''))
        else:
            if not _is_header:
                line = line.split(' = ')
                macinton_c_commands.append(line[0].replace('\n', ''))
                with open(modules_dir + line[1].replace('\n', '')) as command_c:
                    c_commands.append(string_array_sum(command_c.readlines()) + '\n')    

def define_macinton_h_header(path:str):
    name = path[:-3] + 'h'
    with open(name, 'w') as create:
        pass
    compilation(path, name, False)
    return name
    

def compilation(file_path:str, out_file:str, creation:bool):
    global c_commands, macinton_c_commands, modules_dir, watching
    is_commented = 0
    is_block = 0
    current_block = ''
    c_code = 0
    if creation:
        with open(out_file, 'w') as out_creation:
            pass
    with open(file_path) as script_reader:
        with open(out_file, 'a') as append_to_out:
            for line in script_reader.readlines():
                if not is_commented and line.replace('\n', '').replace(' ', '') != '':
                    if line[0] == '@':
                        args = get_args(line.replace('\n', ''))[0]
                        module_load(args[0], args[1])
                    elif line[0] == '*':
                        c_code = not c_code
                    elif line[0] == '(':
                        about = get_args(line[1:])[0]
                        if about[0] not in watching:
                            watching[about[0]] = [about[1], about[2]]
                    elif line[0] == ')':
                        if line[1:].replace('\n', '') in watching:
                            watching.pop(line[1:].replace('\n', ''))
                    elif c_code:
                        append_to_out.write(line)
                    elif line[0] == '#' and not c_code:
                        append_to_out.write(line[1:])
                    elif line[:2] == '->' and not is_block:
                        is_block = 1
                        append_to_out.write('void ' + line[2:] + '(void){\n')
                    elif line[:2] == '<-' and is_block:
                        is_block = 0
                        append_to_out.write('}\n')
                    elif line[0] == '?':
                        args = get_args(line)
                        append_to_out.write('if(' + args[0] + '){\n' + args[1].replace('\n', '') + '();\n}\n')
                    elif line[0] == '$':
                        args = get_args(line)
                        append_to_out.write(replace_with_args(line[1:], args[0]))
                        if len(args) - 1 and args[0][0] in watching:
                            append_to_out.write('if(' + args[0][0] + ' == ' + watching[args[0][0]][0] + '){\n' + watching[args[0][0]][1] + '();\n}\n')
                    elif line[0] == '!':
                        append_to_out.write(f'#define {get_args(line)[0][0]} {get_args(line)[0][1]}\n')
                    elif line[0] == '~':
                        append_to_out.write(f'#undef {line[1:]}\n')
                    elif line[0] == '%':
                        append_to_out.write(f'#include "' + define_macinton_h_header(line[1:].replace('\n', '')) + '"\n')
                    elif line[0] == '&':
                        append_to_out.write(f'#ifdef {line[1:].replace('\n', '')}\n')
                    elif line[0] == '^':
                        append_to_out.write(f'#else\n')
                    elif line[0] == ';':
                        append_to_out.write(f'#endif\n')
                    elif line[0] == '/':
                        append_to_out.write(f'ifndef {line[1:].replace('\n', '')}\n')
                    elif line[:2] == '//':
                        pass
                    elif line[0] == '[':
                        is_commented = 1
                    elif line[:2] != '//':
                        pass
                    else:
                        pass
                elif is_commented and not is_block:
                    if line[0] == ']':
                        is_commented = 0
                else:
                    if line[:2] == '<-':
                        is_block = 0
                        append_to_out.write('}\n')

if len(sys.argv) > 1:
    if sys.argv[1].lower() != '--help':
        compilation(sys.argv[1], 'out.c', True)
        if os.path.getsize('out.c') > 0:
            name = string_array_sum(sys.argv[1].split('.')[:-1])
            if len(sys.argv) >= 3:
                if sys.argv[2] == '?':
                    name = sys.argv[3]
            if sys.platform == 'win32':
                os.system('gcc -o ' + name + '.exe ' + 'out.c')
            else:
                os.system('gcc -o' + name + ' out.c')
            if len(sys.argv) >= 3 and sys.argv[-1].lower() == 'rm':
                os.remove('out.c')
                print("No out.c's 0^o?")
            else:
                print('# #  ###\n# #  # #\n #   # #\n #   ### check the c code in out.c')
    else:
        print('MacintonC 1.3 / Macinton 12\nAdded:\n1.Macroses:\n\t& - #ifdef\n\t^ - #else\n\t; - #endif\n\t/ - #ifndef\n2.Watchers:\n\tAdd - ( : name : value : todo :\n\t\t*todo - equals to ?\n\tDecline - )Name\n3.Headers:\n\tInclude %path/to/header/name.mch\n4.New arguments:\n\t? - out name(without .exe/.app!!!)\n03/04/2024 - Moscow\nMM/DD/YYYY\nThanks for using, check new versions on our github!')
    
