from read_file import *
import sys
def main(argv):
    file_name = argv[0]
    cols, cols_name = read_csv_file(file_name)
    
    # print(cols)
    print('---Columns that have missing values---')
    for col_name in cols_name:
        if '' in cols[col_name]:
            print(col_name)


if __name__ == '__main__':
    main(sys.argv[1:])