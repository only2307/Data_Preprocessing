from read_file import *
import sys
def main(argv):
    file_name = argv[0]
    cols, cols_name = read_csv_file(file_name)
    
    # print(cols)
    print('---Rows that have attributes with missing values---')
    for col_name in cols_name:
        count = 0
        for i in range(len(cols[col_name])):
            if cols[col_name][i] == '':
                count = count + 1
        if (count > 0):
            print(col_name, end=': ')
            print(count)

if __name__ == '__main__':
    main(sys.argv[1:])