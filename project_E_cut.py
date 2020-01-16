import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from sklearn import preprocessing

cwd = os.getcwd() # Get the current working directory

subject_names=['Mutsuki','Sohki','Tetsuya']    #被験者名
exercices_names=['baseball','basketball','bow','jump','kendo','panch','push up','soccer','squat','swing']   #エクササイズ名

def get_data(path_data):
    dataflame = pd.read_csv(path_data, sep=",")  # csvファイルを読み込みdataflameとする
    dataflame = dataflame.drop(['Time (s).1'], axis=1)  # dataflameからTime (s).1を削除
    columns = list(dataflame.columns.values)  # Get a list of columns name
    time = dataflame['Time (s)'].values  # Extract columns named Time

    data = dataflame.values

    data_dict = {}

    for i, m in enumerate(columns):
        data_dict[m] = data[:, i]

    del data_dict['Time (s)']

    return data, data_dict


def spline_data(data, spline=60):

    x = np.array([x for x in range(temp.shape[0])])
    x_new = np.linspace(x.min(), x.max(), spline)
    data_spline = interp1d(x, data, kind='cubic', axis=0)(x_new)   #https://qiita.com/Ken227/items/aee6c82ec6bab92e6abf


    return data_spline

subject_index = 0
exercices_index = 0

data_cut_X = []
data_cut_Y= []
info = []

spline = 60

for subject_index in range(len(subject_names)):

    # Create a path to the data we are going to use
    path_data = cwd + '\\data\\' + subject_names[subject_index] + "\\" + exercices_names[exercices_index] + ".csv"

    data, data_dict = get_data(path_data)

    for exercices_index in range(len(exercices_names)):

        path_data = cwd + '\\data\\' + subject_names[subject_index] + "\\" + exercices_names[exercices_index] + ".csv"
        path_points = cwd +'\\Cut\\' + subject_names[subject_index] + "\\"

        # Load the data
        data, data_dict = get_data(path_data=path_data)

        #npyファイルを読み込み、pointsとする
        points = np.load(path_points + exercices_names[exercices_index] + ".npy")  #プロットした始点と終点の10セット

        # Cut the data
        for point in points:

            temp = data[point[0]:point[1]]
            # Spline all rep to the same number of time step
            temp = spline_data(temp, spline=spline)
            Acceleration_x = temp[:, 1] - temp[:, 1][0]  # tempの後ろから2列目（CoP_x)の各行の値から1行目の値を引く（スタートを0にする）
            Acceleration_y = temp[:, 2] - temp[:, 2][0]  # tempの後ろから1列目（CoP_y)の各行の値から1行目の値を引く（スタートを0にする）
            Acceleration_z = temp[:, 3] - temp[:, 3][0]
            Gyroscope_x = temp[:, 4] - temp[:, 4][0]
            Gyroscope_y = temp[:, 5] - temp[:, 5][0]
            Gyroscope_z = temp[:, 6] - temp[:, 6][0]

            temp = np.concatenate([Acceleration_x[:, np.newaxis], Acceleration_y[:, np.newaxis], Acceleration_z[:, np.newaxis]
                                   ,Gyroscope_x[:, np.newaxis], Gyroscope_y[:, np.newaxis], Gyroscope_z[:, np.newaxis]], axis=1)[np.newaxis]  # CoP_xとCoP_yを合体

            data_cut_X.append(temp)
            print(temp.shape)

            temp = str(subject_index) + "_" + str(exercices_index)

            info.append(temp)

        temp = np.array([exercices_index for i in range(len(points))])
        data_cut_Y.append(temp)
        print(temp.shape)


# Create database
database_X = np.concatenate([d for d in data_cut_X], axis=0)  #np.concatenateについて　　http://python-remrin.hatenadiary.jp/entry/concatenate
database_Y = np.concatenate([d for d in data_cut_Y], axis=0)
database_X_std = np.empty(shape=database_X.shape)    #np.emptyについて  https://deepage.net/features/numpy-empty.html

# Standardize the data
for i in range(database_X.shape[2]):

    mean = np.mean(database_X[:, :, i])
    std = np.std(database_X[:, :, i])
    database_X_std[:, :, i] = (database_X[:, :, i] - mean) / std

database_X_std = database_X_std.reshape(database_X_std.shape[0], -1)

path_save = cwd + '\\Database\\'

if not os.path.exists(path_save):
    os.makedirs(path_save)

np.save(path_save + "DB_X.npy", database_X_std)
np.save(path_save + "DB_Y.npy", database_Y)
np.save(path_save + "info.npy", info)

