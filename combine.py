import csv
import pandas as pd
import numpy as np

landmark_file = r'facilities.csv'
listing_file = r'listings_summary_dec18.csv'
neighbourhood_file = r'neighbourhoods.csv'

neighbourhood_list = []
neighbourhood_points = []
extreme_points = []
landmark_points = []
landmark_info = []

# 其实只取list的neighbours也行，但是对比一下更加放心不会有杂七杂八的东西进来
def get_neighbourhoods(n_file):
    with open(n_file, errors='ignore') as f:
        f_neighbourhood = csv.reader(f)
        headers = next(f_neighbourhood)
        for row in f_neighbourhood:
            neighbourhood_list.append(row[0])
        # print(neighbourhood_list)

def locate_points_neighbourhood(list_file):
    with open(list_file, errors='ignore') as f:
        f_list_rows = csv.reader(f)
        headers = next(f_list_rows)
        for row in f_list_rows:
            # name, latitude, longitude
            neighbourhood_points.append([row[1], float(row[2]), float(row[3])])
            # print(neighbourhood_points)
        for neighbourhoods in neighbourhood_list:
            # print(neighbourhoods)
            located_points = []
            for i in range(len(neighbourhood_points)):
                if neighbourhood_points[i][0] == neighbourhoods:
                    located_points.append([neighbourhood_points[i][1], neighbourhood_points[i][2]])
            # print(located_points[0][0], located_points[0][1])
            located_points_np = np.array(located_points)

            top_row = np.argwhere(located_points_np == np.max(located_points_np[:, 0], axis=0))[0][0]

            bottom_row = np.argwhere(located_points_np == np.min(located_points_np[:, 0], axis=0))[0][0]

            right_row = np.argwhere(located_points_np == np.max(located_points_np[:, 1], axis=0))[0][0]

            left_row = np.argwhere(located_points_np == np.min(located_points_np[:, 1], axis=0))[0][0]

            # print(located_points_np[top_row], located_points_np[bottom_row])
            extreme_points.append(neighbourhoods)
            extreme_points.append(located_points_np[top_row])
            extreme_points.append(located_points_np[bottom_row])
            extreme_points.append(located_points_np[right_row])
            extreme_points.append(located_points_np[left_row])

def get_region_equation_para(left, right, bottom, top):
    k_left_top = 0
    k_left_bottom = 0
    k_right_top = 0
    k_right_bottom = 0
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0

    k_left_top = (top[0]-left[0])/(top[1]-left[1])
    k_left_bottom = (bottom[0]-left[0])/(bottom[1]-left[1])
    k_right_top = (top[0]-right[0])/(top[1]-right[1])
    k_right_bottom = (bottom[0]-right[0])/(bottom[1]-right[1])

    b1 = left[0]-k_left_top*left[1]
    b2 = left[0]-k_left_bottom*left[1]
    b3 = right[0]-k_right_top*right[1]
    b4 = right[0]-k_right_bottom*right[1]

    # print('y<' + str(k_left_top) + '*X+' + str(b1))
    # print('y>' + str(k_left_bottom) + '*X+' + str(b2))
    # print('y<' + str(k_right_top) + '*X+' + str(b3))
    # print('y>' + str(k_right_bottom) + '*X+' + str(b4))

    return k_left_top, k_left_bottom, k_right_top, k_right_bottom, b1, b2, b3, b4

neigh_landmark = []

def is_in_equation(theme, subtheme ,neigh, landmark,x,y,klt,klb,krt,krb,blt,blb,brt,brb):
    x = float(x)
    y = float(y)
    klt = float(klt)
    klb = float(klb)
    krt = float(krt)
    krb = float(krb)
    blt = float(blt)
    blb = float(blb)
    brt = float(brt)
    brb = float(brb)

    if y <= klt*x + blt and y >= klb*x + blb and y <= krt*x+brt and y>= krb*x+brb:
        # print(landmark+' is in the '+neigh)
        neigh_landmark.append([neigh, landmark, theme, subtheme, x, y])
    # else:
        # print(str(y-klt*x + blt))


# def which_region( ):
#     with open(landmark_file) as f:
#         f_landmarks = csv.reader(f)
#         headers = next(f_landmarks)
#         for row in f_landmarks:



if __name__ == '__main__':
    get_neighbourhoods(neighbourhood_file)
    locate_points_neighbourhood(listing_file)
    for i in range(len(neighbourhood_list)):
        # print(extreme_points[i*5])
        raw_data = []
        for n in range(4):
            # 4,3,2,1 left, right, bottom, top
            k = 5*i+4-n
            # print(extreme_points[k])
            raw_data.append(extreme_points[k])

        k1, k2, k3, k4, c1, c2, c3, c4 = get_region_equation_para(raw_data[0],raw_data[1],raw_data[2],raw_data[3])
        # print(raw_data[0], raw_data[1], raw_data[2], raw_data[3])
        # which_region()
        # print(k1, k2, k3, k4, c1, c2, c3, c4)
        with open(landmark_file) as f:
            f_landmark = csv.reader(f)
            heads = next(f_landmark)
            for landmarks in f_landmark:
                # print(landmarks[2], landmarks[3], landmarks[4])
                # print(extreme_points[i*5])
                is_in_equation(landmarks[0], landmarks[1], extreme_points[i*5], landmarks[2], landmarks[4], landmarks[3], k1, k2, k3, k4, c1, c2, c3, c4, )
    # print(neigh_landmark)
    column_name = ['neighbourhood', 'landmark_name', 'theme', 'subtheme', 'longitude', 'latitude']
    test = pd.DataFrame(columns=column_name, index=None, data=neigh_landmark)
    test.to_csv('landmark_neighbourhood.csv', encoding='utf-8')