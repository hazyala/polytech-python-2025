import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

anscombe_data = np.load ('Python/data/ch3_anscombe.npy')
print("========== Anscombe Data shape ==========")
print(anscombe_data.shape) # (4, 11, 2)는 11개의 점, 4개의 그룹, 각 점은 (x, y) 좌표를 가진다는 의미로, 2는 영어와 수학, 11은 학생수, 4는 학급 수 라고 생각할 수 있음.
print(anscombe_data[0])

stats_df = pd.DataFrame(index=['X_mean', 'Y_mean', 'X_variance', 'Y_variance', 'X&Y_Correlation', 'X&Y_regression line'])
for i, data in enumerate(anscombe_data):
    dataX = data[:, 0]
    dataY = data[:, 1]
    poly_fit = np.polyfit(dataX, dataY, 1)
    stats_df[f'data{i+1}'] =\
        [f'{np.mean(dataX):.2f}',
         f'{np.var(dataX):.2f}',
         f'{np.mean(dataY):.2f}',
         f'{np.var(dataY):.2f}',
         f'{np.corrcoef(dataX, dataY)[0, 1]:.2f}',
         f'{poly_fit[1]:.2f} + {poly_fit[0]:.2f}x'
         ]
print(stats_df)

#위 데이터 수치의 오류를 증명하기 위한 시각화
print("========== 산점도와 회귀선 그리기 ==========")
fig,axes = plt.subplots(nrows=2, ncols=2, figsize=(10,10),
                        sharex=True, sharey=True)
xs = np.linspace(0, 30, 100)
for i, data in enumerate(anscombe_data):
    poly_fit = np.polyfit(data[:,0], data[:,1], 1)
    poly_1d = np.poly1d(poly_fit)
    ys=poly_1d(xs)
    #그리는 영역을 선택
    ax = axes[i//2, i%2]
    ax.set_xlim([4, 20])
    ax.set_ylim([3, 13])
    #타이틀 설정
    ax.set_title(f'data{i+1}')
    ax.scatter(data[:, 0], data[:,1])
    ax.plot(xs, ys, color='gray')
 #그래프 사이의 간격 좁힘
plt.tight_layout()
plt.show()

#데이터 히트맵
print("========== 히트맵 그리기 ==========")
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 12),sharex=True, sharey=True)

x_min, x_max = 4, 20
y_min, y_max = 3, 13
bins_count = 5 

mesh = None

for i, data in enumerate(anscombe_data):
    ax = axes[i // 2, i % 2]

    dataX = data[:, 0]
    dataY = data[:, 1]

    # 히스토그램 생성
    _, _, _, mesh = ax.hist2d(dataX, dataY, bins=(bins_count, bins_count), range=[[x_min, x_max], [y_min, y_max]],cmap='viridis')

    # 타이틀 및 축 설정
    ax.set_title(f'Data {i+1} Heatmap', fontsize=14)
    ax.set_xlabel('X Value', fontsize=12)
    ax.set_ylabel('Y Value', fontsize=12)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    
if mesh is not None:
    cbar = fig.colorbar(mesh, ax=axes.ravel().tolist())
    cbar.ax.set_ylabel('Point Count (Density)', rotation=270, labelpad=20, fontsize=12)

plt.show()