import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#csvファイルを読み込みデータを整形する関数
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

#グラフを操作するための処理色々まとめたやつ
class Plotter:

    def __init__(self, data, title):

        self.points = []
        self.data = data

        plt.ion()
        self.fig = plt.figure(1, figsize=(16, 5))
        self.ax1 = plt.subplot(1, 1, 1)

        self.fig.suptitle(title + '\n' + 'z + right click')

        self.ax1.plot(np.sum(data[:, 1:5], axis=1), 'r')
        self.fig.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.92, wspace=0.05, hspace=0.1)

        self.ax1.grid()

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):

        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

        if event.key == 'z':
            self.points.append([int(event.xdata)])
            self.ax1.plot(event.xdata, event.ydata, 'o', color='r', markersize=5)
            self.ax1.axvline(x=event.xdata, color='r')
            self.fig.canvas.draw()

    def get_points(self):

        return self.points

    def plot_point(self, points):

        for point in points:

            self.ax1.axvline(x=point[0], color='r', linewidth=3)
            self.ax1.axvline(x=point[1], color='b', linewidth=3)

cwd=os.getcwd()  #現在のディレクトリをcwdに入れる

subject_names=['Mutsuki','Sohki','Tetsuya']    #被験者名
exercices_names=['baseball','basketball','bow','jump','kendo','panch','push up','soccer','squat','swing']   #エクササイズ名

subject_index=2   #被験者選択
exercices_index=9   #エクササイズ選択

#csvファイルのパスをpath_dataに入れる
path_data = cwd + '\\data\\' + subject_names[subject_index] + "\\" + exercices_names[exercices_index] + ".csv"

data, data_dict= get_data(path_data)     #自分で定義した関数を利用
title = "Subject: " + str(subject_names[subject_index]) + " - Exercice: " + str(exercices_names[exercices_index])
print(title)   #現在選択中の被験者名とエクササイズ名を表示



#1) Call the plotter
#2) Click the points
#3) When you have click all the points you can use point = plotter.get poinits()

plotter=Plotter(data, title=title)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# This part of the code must be use only after you have finish to click !!! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

points=plotter.get_points()

points=np.array(points)
points=points.reshape(points.shape[0] // 2, -1)


#Plot the results
plotter=Plotter(data,title=title)
plotter.plot_point(points=points)


#Save the click point
path_save = cwd + '\\Cut\\' + subject_names[subject_index] + "\\"
if not os.path.exists(path_save):
    os.makedirs(path_save)

np.save(path_save+exercices_names[exercices_index],points)   #プロットの始点と終点の記録をCutファイルとして保存


