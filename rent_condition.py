import csv
import pandas as pd

if __name__ == '__main__':
    with open(r'calendar_dec18.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        data_row = []
        for row in f_csv:
            # print(row[0])
            with open(r'neighbour.csv') as f_n:
                f_neigh = csv.reader(f_n)
                heads = next(f_neigh)
                for rows in f_neigh:
                    # print(rows[0])
                    if rows[0] == row[0]:
                        data_row.append([row[0], row[1], row[2], rows[1], rows[2]])
                    else:
                        pass
        print(data_row)

        column_name = ['id', 'date', 'available', 'neighbourhood', 'price']
        test = pd.DataFrame(columns=column_name, index=None, data=data_row)
        test.to_csv('calender_neighbour_price.csv', encoding='utf-8')
