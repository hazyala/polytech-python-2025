import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("========== Scores ==========")
df = pd.read_csv('Python/data/ch2_scores_em.csv', index_col='student number')

en_scores = np.array(df['english'])[:10]
ma_scores = np.array(df['mathematics'])[:10]

scores_df = pd.DataFrame({'english': en_scores, 'mathematics': ma_scores}, index=pd.Index(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], name='student'))
print(scores_df)

#=========================공분산 구하기=========================
print("\n========== Covariance ==========")
summery_df = scores_df.copy()
summery_df['english_deviation'] = summery_df['english'] - summery_df['english'].mean()
summery_df['mathematics_deviation'] = summery_df['mathematics'] - summery_df['mathematics'].mean()
summery_df['product of deviation'] = summery_df['english_deviation'] * summery_df['mathematics_deviation']
print(summery_df)
print("전체 면적별 평균 : ",summery_df['product of deviation'].mean()) 

#======================Numpy로 공분산 구하기=====================
cov_mat = np.cov(en_scores, ma_scores, ddof=0) 
print("Numpy 공분산 행렬 \n", cov_mat)

#=========================상관계수 구하기=========================
print("========== Pandas 상관계수 행렬 ========== \n",scores_df.corr())
print("========== Numpy 상관계수 행렬 ========== \n", np.corrcoef(en_scores, ma_scores))  

#=========================산점도 그리기=========================
english_socers = np.array(df['english'])
mathematics_scores = np.array(df['mathematics'])
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.scatter(english_socers, mathematics_scores)
ax.set_xlabel('English Scores')
ax.set_ylabel('Mathematics Scores')
plt.show()

#=========================회귀직선 그리기=========================
print("========== 함수형 회귀선 구하기 ==========")
poly_fit = np.polyfit(english_socers, mathematics_scores, 1)
poly_1d = np.poly1d(poly_fit)
xs = np.linspace(english_socers.min(), english_socers.max())
ys = poly_1d(xs)
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.scatter(english_socers, mathematics_scores, label='Scores')
ax.plot(xs, ys, color='gray', label=f'{poly_fit[1]:.2f}x + {poly_fit[0]:.2f}')
ax.set_xlabel('English Scores')
ax.set_ylabel('Mathematics Scores')
ax.legend(loc='upper left')
plt.show()

print("========== 직접 수식 계산형 회귀선 구하기 ==========")
slope, intercept = np.polyfit(english_socers, mathematics_scores, 1)
print(f"기울기: {slope}, 절편: {intercept}")
regression_line = slope * english_socers + intercept
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.scatter(english_socers, mathematics_scores, label='Data Points')
ax.plot(english_socers, regression_line, color='red', label='Regression Line')
ax.set_xlabel('English Scores')
ax.set_ylabel('Mathematics Scores')
ax.legend()
plt.show()

#=========================히트맵 그리기=========================
print("========== 히트맵 그리기 ==========")
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
c = ax.hist2d(english_socers, mathematics_scores, bins=[9,8], range=[(35,80), (55,95)])
ax.set_xlabel('English Scores')
ax.set_ylabel('Mathematics Scores')
ax.set_xticks(c[1])
ax.set_yticks(c[2])
fig.colorbar(c[3], ax=ax)
plt.show()


