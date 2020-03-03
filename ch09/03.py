# encoding: utf-8

import tensorflow as tf
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, Sequential, optimizers, losses, metrics, regularizers
from tensorflow.keras.layers import Dense
from pandas import *
from mpl_toolkits.mplot3d import Axes3D

N_SAMPLES = 1000  # 采样点数
# N_Epochs = 300  # 网络层数
# N_Epochs = 500  # dropout
N_Epochs = 300  # 正则化
TEST_SIZE = 0.3  # 测试数量比率
# weight_values = [[1,2,3,4],[2,3,4,1],[3,4,1,2],[4,1,2,3],[1,4,3,2]]  # 测试用
weight_values = []
OUTPUT_DIR = r'F:/DeepLearning_All/Deep-Learning-with-TensorFlow-book-master/ch09/03.py'
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# 产生一个简单的样本数据集，半环形图，类似的有make_circles,环形数据
X, y = make_moons(n_samples=N_SAMPLES, noise=0.25, random_state=100)  # (1000, 2),(1000, 1)
# 将矩阵随机划分训练集和测试集 (700,2),(300,2),(700,1),(300,1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=42)
print(X.shape, y.shape)


def make_plot(X, y, plot_name, file_name, XX=None, YY=None, preds=None):
    plt.figure()
    axes = plt.gca()
    x_min = X[:, 0].min() - 1
    x_max = X[:, 0].max() + 1
    y_min = X[:, 1].min() - 1
    y_max = X[:, 1].max() + 1
    axes.set_xlim([x_min, x_max])
    axes.set_ylim([y_min, y_max])
    axes.set(xlabel="$x_l$", ylabel="$x_2$")

    # 根据网络输出绘制预测曲面
     # markers = ['o' if i == 1 else 's' for i in y.ravel()]
     # plt.scatter(X[:, 0], X[:, 1], c=y.ravel(), s=20, cmap=plt.cm.Spectral, edgecolors='none', m=markers)
    if XX is None and YY is None and preds is None:
        yr = y.ravel()
        for step in range(X[:, 0].size):
            if yr[step] == 1:
                plt.scatter(X[step, 0], X[step, 1], c='b', s=20, cmap=plt.cm.Spectral, edgecolors='none', marker='o')
            else:
                plt.scatter(X[step, 0], X[step, 1], c='r', s=20, cmap=plt.cm.Spectral, edgecolors='none', marker='s')
        plt.savefig(OUTPUT_DIR+'/'+file_name)
        # plt.show()
    else:
        plt.contour(XX, YY, preds, cmap=plt.cm.autumn, alpha=0.8)
        plt.scatter(X[:, 0], X[:, 1], c=y, s=20, cmap=plt.cm.autumn, edgecolors='k')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt.title乱码的问题
        plt.rcParams['axes.unicode_minus'] = False
        plt.title(plot_name)
        plt.savefig(OUTPUT_DIR+'/'+file_name)
        # plt.show()


# make_plot(X, y, None, "exam7_dataset.svg")


# 正则化影响 5层神经网络
def build_model_with_reglarization(_lambda):
    # 创建带正则化的神经网络
    model = Sequential()
    model.add(Dense(8, input_dim=2, activation='relu'))  # 不带正则化
    model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(_lambda)))  # 带L2正则化
    model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(_lambda)))  # 带L2正则化
    model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(_lambda)))  # 带L2正则化
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def draw_weights_table(weights):
    cols_label = ['regularizer lambda', 'W Min', 'W Max', 'W Mean']
    fig = plt.figure(figsize=(9, 4))
    ax = fig.add_subplot(111, frameon=True, xticks=[], yticks=[])
    the_table = plt.table(cellText=weights, colWidths=[0.1]*4, colLabels=cols_label, loc='center', cellLoc='center')
    the_table.set_fontsize(35)  # 改变不了字体大小
    the_table.scale(2.5, 2.58)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt.title乱码的问题
    plt.rcParams['axes.unicode_minus'] = False
    plt.title("权值信息表", fontsize=30)
    plt.savefig(OUTPUT_DIR + '/' + "权值信息表.png")
    plt.show()


def plot_weights_matrix(model, layer_index, plot_title, file_name, _lambda):
    para = model.trainable_variables
    weights = para[2*layer_index].numpy()
    w_min = weights.min()
    w_max = weights.max()
    w_mean = np.mean(weights)
    values = np.array([_lambda, w_min, w_max, w_mean], dtype=np.float64)
    values = values.reshape(1, 4)
    weight_values.append(values)
    x = np.arange(0, 256, 1)
    y = np.arange(0, 256, 1)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(X, Y, weights, rstride=1, cstride=1, cmap=plt.cm.jet)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt.title乱码的问题
    plt.rcParams['axes.unicode_minus'] = False
    plt.title(plot_title)
    plt.savefig(OUTPUT_DIR + '/' + file_name)
    # plt.show()


for _lambda in [1e-5, 1e-3, 1e-1, 0.12, 0.13]:
    model = build_model_with_reglarization(_lambda)
    history = model.fit(X_train, y_train, epochs=N_Epochs, verbose=1)
    # 绘制权值范围
    layer_index = 2  # 选取第二层的权值
    plot_title = "正则化-[lambda = {}]".format(str(_lambda))
    file_name = "正则化-权值%f.png" % _lambda
    # 绘制网络权值范围图
    plot_weights_matrix(model, layer_index, plot_title, file_name, _lambda)
     # 绘制不同层数的网络决策边界曲线
    x_min = X[:, 0].min() - 1
    x_max = X[:, 0].max() + 1
    y_min = X[:, 1].min() - 1
    y_max = X[:, 1].max() + 1
    # XX(477, 600), YY(477, 600)
    XX, YY = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))  # 创建网格
    Z = model.predict_classes(np.c_[XX.ravel(), YY.ravel()])  # (286200, 1) [0 or 1]
    preds = Z.reshape(XX.shape)
    title = "正则化({})".format(_lambda)
    file = "正则化%f.png" % _lambda
    make_plot(X_train, y_train, title, file, XX, YY, preds)

draw_weights_table(weight_values)