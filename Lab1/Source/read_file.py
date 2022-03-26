def read_csv_file(file_name):
    f = open(file_name,'r')
    cols_name = f.readline().rstrip().split(',')

    cols = dict()

    for col_name in cols_name:
        cols[col_name] = []

    for line in f:
        line_val = line.rstrip().split(',')
        for i in range(len(line_val)):
            cols[cols_name[i]].append(line_val[i])

    f.close()
    return cols, cols_name