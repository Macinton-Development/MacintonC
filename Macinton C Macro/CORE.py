import sys, os

def string_arrray_sum(array:list[str]):
    out = ''
    for element in array:
        out += element
    return out

if len(sys.argv) > 1:
    with open('MACINTONCMACRO.mcs') as reader:
        lines = reader.readlines()
    with open(sys.argv[1]) as reader:
        lines += reader.readlines()
    with open('out.mcs', 'w') as create: pass
    with open('out.mcs', 'a') as append:
        for line in lines:
            append.write(line)
        append.write('\n#}')
    os.system('macintonc out.mcs rm')
