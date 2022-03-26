from read_file import *
import sys, getopt
from math import sqrt 
def main(argv):
   
    # đọc file house-prices.csv
    file_name = argv[0]
    cols, cols_name = read_csv_file(file_name)

    # lấy ra các tham số của command line
    opt_list = argv[1:]
    try:
        opts_values, args = getopt.getopt(opt_list,'m:c:o:',['method=','column=','out='])
    except getopt.GetoptError:
        print('Command line arguments invalid. Try again!')
        sys.exit(2)
    
    for opt, value in opts_values:
        if opt == '--method':
            method = value
        elif opt == '--column':
            col_name = value
        elif opt == '--out':
            results = value

    
    cols_copy = dict()
    # lấy ra cột dữ liệu theo yêu cầu
    cols_copy[col_name] = cols[col_name].copy()


    if '' in cols_copy[col_name]:
        # điền các giá trị bị thiếu

        # sort các cột này
        cols_copy[col_name].sort(reverse=True)
        
        #lấy ra các dòng có giá trị
        pos = cols_copy[col_name].index('')
        cols_copy[col_name] = cols_copy[col_name][:pos]

        for j in range(len(cols_copy[col_name])):
            cols_copy[col_name][j] = float(cols_copy[col_name][j])

        # tính giá trị mean của cột
        mean_value_before = sum(cols_copy[col_name]) // len(cols_copy[col_name])
        print('Mean value before filling: ', mean_value_before)
        # thay các giá trị bị rỗng bằng giá trị mean
        for j in range(len(cols[col_name])):
            if cols[col_name][j] == '':
                cols[col_name][j] = mean_value_before
    
    # tính mean, sd cho cho thuộc tính sau khi đã điền các giá trị thiếu
    for i in range(len(cols[col_name])):
        cols[col_name][i] = float(cols[col_name][i])
    sum_squared = 0
    mean_value_after = sum(cols[col_name]) / len(cols[col_name])
    for i in range(len(cols[col_name])):
        sum_squared += (cols[col_name][i] - mean_value_after)**2
    
    sd = sqrt(sum_squared / len(cols[col_name]))

    if method == 'minmax':
        print('-----MinMax Normalization-----')
        range_col = max(cols[col_name]) - min(cols[col_name])
        min_val = min(cols[col_name])
        print('Range: ',range_col)
        print('Min: ', min_val)
        print('Mean: ',mean_value_after)
        for i in range(len(cols[col_name])):
            cols[col_name][i] = round((float(cols[col_name][i]) - min_val) / range_col,3)
    elif method == 'zscore':
        print('-----Z-score Normalization-----')
        print('Mean: ',mean_value_after)
        print('Sd: ',sd)
        for i in range(len(cols[col_name])):
            cols[col_name][i] = round((float(cols[col_name][i]) - mean_value_after) / sd,3)
    else:
        print('Method not available. Try again!')
        sys.exit(2)

    #ghi vào file tên các cột đã xử lí
    f = open(results,'w')
    print(col_name,file=f)

    #ghi các phần tử đã xử lí
    for i in range(len(cols[col_name])): # đi qua từng dòng
        print(cols[col_name][i],file=f)
    f.close()

if __name__ == '__main__':
    main(sys.argv[1:])