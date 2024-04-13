import sys, os, bml


#Macinton C
#Extension: mcs
#mcs -> c -> executable

c_commands = []
macinton_c_commands = []
modules_c = []
modules_dir = ''
watchers = []
watching = {}
cur_line = ''

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
            if element == ':' and not is_string:
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
    global c_commands, macinton_c_commands, modules_dir, watching, cur_line
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
                cur_line = line
                if not is_commented and line.replace('\n', '').replace(' ', '') != '':
                    if line[0] == '@':
                        args = get_args(line.replace('\n', ''))[0]
                        module_load(args[0], args[1])
                    elif line[:5] == 'C_MODE':
                        c_code = not c_code
                    elif line[:5] == 'WATCH':
                        about = get_args(line[5:])[0]
                        if about[0] not in watching:
                            watching[about[0]] = []
                        watching[about[0]].append([about[1], about[2]])
                    elif line[:5] == 'CLOSE':
                        if line[5:].replace('\n', '') in watching:
                            watching.pop(line[5:].replace('\n', ''))
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
                            for element in watching[args[0][0]]:
                                append_to_out.write('if(' + args[0][0] + ' == ' + element[0] + '){\n' + element[1] + '();\n}\n')
                    elif line[:3] == 'DEF':
                        append_to_out.write('#define ' + get_args(line)[0][0] + ' ' + get_args(line)[0][1] + '\n')
                    elif line[:3] == 'DEL':
                        append_to_out.write('#undef ' + line[4:] + '\n')
                    elif line[0] == '%':
                        append_to_out.write(f'#include "' + define_macinton_h_header(line[1:].replace("\n", "")) + '"\n')
                    elif line[:4] == 'IDEF':
                        append_to_out.write('#ifdef ' + line[5:].replace("\n", "\n") + '\n')
                    elif line[:3] == 'NOT':
                        append_to_out.write('#else\n')
                    elif line[:2] == 'FI':
                        append_to_out.write('#endif\n')
                    elif line[:5] == 'INDEF':
                        append_to_out.write('ifndef ' + line[6:].replace("\n", "") + '\n')
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
        try:
            compilation(sys.argv[1], 'out.c', True)
            args = bml.get_contents(sys.argv[2])
            if os.path.getsize('out.c') > 0:
                os.system(f'gcc -o {args["NAME"][0]} out.c')
                if args['RM'][0] == 'TRUE':
                    os.remove('out.c')
                    print("No out.c's 0^o?")
                else:
                    print('# #  ###\n# #  # #\n #   # #\n #   ### check the c code in out.c')                    
        except:
            print(f'COMPILATION ERROR: {cur_line}')
