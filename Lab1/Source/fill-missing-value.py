from read_file import *
import sys, getopt
def main(argv):
   
    # đọc file house-prices.csv
    file_name = argv[0]
    cols, cols_name = read_csv_file(file_name)

    # lấy ra các tham số của command line
    opt_list = argv[1:]
    try:
        opts_values, args = getopt.getopt(opt_list,'m:c:o:',['method=','columns=','out='])
    except getopt.GetoptError:
        print('Command line arguments invalid. Try again!')
        sys.exit(2)
    
    for opt, value in opts_values:
        if opt == '--method':
            method = value
        elif opt == '--columns':
            columns_name_list = value.split(',')
        elif opt == '--out':
            results = value

    # kiểm tra tên cột có hợp lệ
    for item in columns_name_list:
        if item not in cols_name:
            print('%s not available! Try again!'%item)
            sys.exit(2)


    dict_cols = dict()
    len_cols_name_list = len(columns_name_list)
    for name in columns_name_list:
        # lấy ra các cột dữ liệu theo yêu cầu
        dict_cols[name] = cols[name].copy()
        # sort các cột này
        dict_cols[name].sort(reverse=True)
      
        #lấy ra các dòng có giá trị
        pos = dict_cols[name].index('')
        dict_cols[name] = dict_cols[name][:pos]
        
    
    if method == 'mean':
        for name in columns_name_list:
            for j in range(len(dict_cols[name])):
                dict_cols[name][j] = float(dict_cols[name][j])

            # tính giá trị mean của cột
            mean_value = sum(dict_cols[name]) // len(dict_cols[name])

            # thay các giá trị bị rỗng bằng giá trị mean
            for j in range(len(cols[name])):
                if cols[name][j] == '':
                    cols[name][j] = str(mean_value)
    elif method=='median':
        for i in range(len_cols_name_list):
            # lấy ra vị trí median
            median_value_pos = len(dict_cols[columns_name_list[i]]) // 2 + 1

            #lấy ra giá trị median
            median_value = dict_cols[columns_name_list[i]][median_value_pos]

            # thay các giá trị rỗng bằng giá trị median
            for j in range(len(cols[columns_name_list[i]])):
                if cols[columns_name_list[i]][j] == '':
                    cols[columns_name_list[i]][j] = str(median_value)
    elif method == 'mode':
        dict_value = dict()
        
        # duyệt qua từng cột cần xử lí
        for name in columns_name_list:
            #duyệt qua từng dòng
            for j in range(len(dict_cols[name])):
                    dict_value[dict_cols[name][j]] = dict_value.get(dict_cols[name][j],0)+1

            mode_value = max(dict_value.values())
            for key in dict_value.keys():
                if dict_value[key] == mode_value:
                    mode = key
                    break
            
            for j in range(len(cols[name])):
                if cols[name][j] == '':
                    cols[name][j] = mode
    else:
        print('Method not available. Try again!')
        sys.exit(2)

    f = open(results,'w')
    #ghi vào file tên các cột đã xử lí
    for i in range(len_cols_name_list-1):
        print(columns_name_list[i],end=',',file=f)
        
    print(columns_name_list[len_cols_name_list-1],file=f)

    #ghi các phần tử đã xử lí
    for i in range(len(cols[columns_name_list[0]])): # đi qua từng dòng
        for j in range(len_cols_name_list-1): #đi qua các phần tử cần ghi trong dòng thứ i
            print(cols[columns_name_list[j]][i], end=',',file=f)

        print(cols[columns_name_list[len_cols_name_list-1]][i],file=f)
    f.close()


if __name__ == '__main__':
    main(sys.argv[1:])