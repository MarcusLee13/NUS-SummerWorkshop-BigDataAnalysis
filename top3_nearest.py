import csv
import pandas as pd
import numpy as np
import math
import heapq

# 0 neighbourhood 1 landmark_name 2 theme 3 subtheme (longitude4,latitude5)
landmarks_list = []

# 0 id 1 neighbourhood (latitude2,longitude3) 4price
houses_list = []

# 0 neighbourhood 1 landmark_name 2 theme 3 subtheme 4 AVG_top3_Price
price_list = []

if __name__ == '__main__':
    with open(r'landmark_neighbourhood.csv') as l:
        l_csv = csv.reader(l)
        headers = next(l_csv)
        for rows in l_csv:
            landmarks_list.append(rows)

    with open(r'listings_summary_dec18.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for lines in f_csv:
            houses_list.append(lines)


    # print(landmarks_list[0][4],landmarks_list[0][5],houses_list[0][3],houses_list[0][2])
    for landmarks in landmarks_list:
        longitude, latitude = landmarks[4], landmarks[5]
        # print(longitude, latitude)
        landmark_point = np.array([longitude, latitude]).astype(float)
        # print(landmark_point)
        price_buff = []
        distance_buff = []
        price_distance_buff = []
        for houses in houses_list:
            h_x, h_y = houses[3], houses[2]
            house_point = np.array([h_x, h_y]).astype(float)
            # print(house_point)
            point_abs = landmark_point-house_point
            distance = math.hypot(point_abs[0], point_abs[1])
            distance_buff.append(distance)
            price_buff.append(houses[4])
            # price_distance_buff.append([houses[4], distance])
        # print(price_buff[100], distance_buff[100], price_distance_buff[100])

        # min_distance_index_list = map(distance_buff.index, heapq.nsmallest(3, distance_buff))
        #
        # min_distance_index_list = list(min_distance_index_list)
        # near1, near2, near3 = int(min_distance_index_list[0]), int(min_distance_index_list[1]), int(min_distance_index_list[2])
        #
        # price1 , price2 , price3 = price_buff[near1], price_buff[near2], price_buff[near3]
        # AVG_Price_3_nearest = (int(price1) + int(price2) + int(price3)) / 3

        min_distance_index_list = map(distance_buff.index, heapq.nsmallest(5, distance_buff))

        min_distance_index_list = list(min_distance_index_list)
        near1, near2, near3, near4, near5 = int(min_distance_index_list[0]), int(min_distance_index_list[1]), int(
            min_distance_index_list[2]), int(min_distance_index_list[3]), int(min_distance_index_list[4])

        price1, price2, price3, price4, price5 = price_buff[near1], price_buff[near2], price_buff[near3], price_buff[near4], price_buff[near5]
        AVG_Price_5_nearest = (int(price1) + int(price2) + int(price3) + int(price4) + int(price5)) / 5

        price_list.append([landmarks[0], landmarks[1], landmarks[2], landmarks[3], AVG_Price_5_nearest])


    column_name = ['neighbourhood', 'landmark_name', 'theme', 'subtheme', 'AVG_listing_price']

    # AVG_file = pd.DataFrame(columns=column_name, index=None, data=price_list)
    # AVG_file.to_csv('AVG_3_Nearest_Price.csv', encoding='utf-8')

    AVG_file = pd.DataFrame(columns=column_name, index=None, data=price_list)
    AVG_file.to_csv('AVG_5_Nearest_Price.csv', encoding='utf-8')
