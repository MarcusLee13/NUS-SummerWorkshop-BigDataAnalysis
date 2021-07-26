import csv
import pandas as pd

def is_contain_messycodes(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            # print(check_str)
            return True

def remove_lines(filename):
    with open(filename, errors='ignore') as f:
        f_csv = csv.reader(f)
        useless_rows_count = 0
        usefull_rows_count = 0
        headers = next(f_csv)
        row_data = []
        for rows in f_csv:
            if is_contain_messycodes(rows[5]) == True:
                useless_rows_count += 1
                print(useless_rows_count)
            elif is_contain_messycodes(rows[4]) == True:
                useless_rows_count +=1
                print(useless_rows_count)
            else:
                row_data.append(rows)
                # with open('cleaned_reviews_dec18.csv', 'w', encoding='utf-8') as f_new:
                    # f_new = open('cleaned_reviews_dec18.csv', 'w', encoding='utf-8')
                    # csv_writer = csv.writer(f_new)
                    # print(rows)
                    # csv_writer.writerow(rows)
                    # usefull_rows_count += 1
                    # print(usefull_rows_count)

        print(row_data)
        column_name = ['listing_id', 'id', 'date', 'reviewer_id', 'reviewer_name', 'comments']
        test = pd.DataFrame(columns=column_name, index=None, data=row_data)
        test.to_csv('cleaned_reviews_dec18.csv',encoding='utf-8')

if __name__ == '__main__':
    file_name = r'reviews_dec18.csv'
    remove_lines(file_name)
