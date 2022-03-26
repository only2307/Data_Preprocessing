import sys, getopt
def main(argv):
   
    # đọc file house-prices.csv
    file_name = argv[0]
    f = open(file_name,'r')
    lines  = f.readlines()
    col_names = lines.pop(0)
    f.close()
    len_col_names = len(col_names.split(','))
    # lấy ra các tham số của command line
    opt_list = argv[1:]
    try:
        opts_values, args = getopt.getopt(opt_list,'l:o:',['lim=','out='])
    except getopt.GetoptError:
        print('Command line arguments invalid. Try again!')
        sys.exit(2)
    
    for opt, value in opts_values:
        if opt == '--lim':
            lim = float(value)
        elif opt == '--out':
            results = value
    # đọc từng dòng
    for line in lines:
        list_line = line.split(',')
        # đếm số phần tử bị thiếu trong dòng
        missing_percent = list_line.count('') / len_col_names
        # kiểm tra theo lim và xóa nếu thỏa điều kiện
        if missing_percent > lim:
            lines.remove(line)

    # ghi file sau khi đã xử lí
    f = open(results,'w')
    print(col_names,file=f,end='')

    for line in lines:
        print(line,file=f,end='')
    f.close()

if __name__ == '__main__':
    main(sys.argv[1:])
