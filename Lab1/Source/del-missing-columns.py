from read_file import *
import sys, getopt
def main(argv):
   
    # đọc file house-prices.csv
    file_name = argv[0]
    cols, cols_name = read_csv_file(file_name)

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
    cols_name_copy = cols_name.copy()
    # duyệt từng cột
    for key in cols_name:
        missing_percent = cols[key].count('') / len(cols[key])
        if missing_percent > lim:
            cols.pop(key)
            cols_name_copy.remove(key)

    #ghi file sau khi xử lí
    len_cols_name = len(cols_name_copy)
    f = open(results,'w')
    for item in cols_name_copy[0:len_cols_name-1]:
        print(item,end=',',file=f)
    print(cols_name_copy[len_cols_name-1],file=f)

    for i in range (len(cols['Id'])):
        for j in range(len_cols_name-1):
            print(cols[cols_name_copy[j]][i], end=',',file=f)
        print(cols[cols_name_copy[len_cols_name-1]][i],file=f)
    f.close()

if __name__ == '__main__':
    main(sys.argv[1:])
