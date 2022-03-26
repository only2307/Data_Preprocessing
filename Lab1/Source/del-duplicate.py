from read_file import *
import sys
def main(argv):
    file_name = argv[0]
    file_out = argv[1]
    f = open(file_name,'r')
    lines = f.readlines()
    f.close()
    len_lines = len(lines)
    i = 0
    while i < len_lines:
        count = lines.count(lines[i])
        if  count > 1:
            line = lines[i]
            for i in range(count-1):
                lines.remove(line)
        i += 1
        len_lines=len(lines)
    f= open(file_out,'w')
    for line in lines:
        print(line,file=f,end='')
if __name__ == '__main__':
    main(sys.argv[1:])

