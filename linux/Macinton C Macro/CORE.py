import sys, os

def string_arrray_sum(array:list[str]):
    out = ''
    for element in array:
        out += element
    return out

if len(sys.argv) > 2:
    with open('MACINTONCMACRO.mcs') as reader:
        lines = reader.readlines()[1:]
    with open(sys.argv[1]) as reader:
        lines += reader.readlines()
    with open('out.mcs', 'w') as create: pass
    with open('out.mcs', 'a') as append:
        append.write(f'@ : init : {sys.argv[2]} :\n')
        for line in lines:
            append.write(line)
        append.write('\n#}')
    os.system('./MacintonC out.mcs rm')
