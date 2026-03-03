import numpy as np
import pandas as pd

df = pd.read_csv('Python/data/ch2_scores_em.csv', index_col='student number')
# print(df.head())

scores = np.array(df['english'])[:10]

scores_df = pd.DataFrame({'scores': scores}, index=pd.Index(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], name='student'))
print(scores_df)

#=========================평균 구하기=========================
print("========== Average ==========")
print(sum(scores) / len(scores))
print(np.mean(scores))
print(scores_df.mean()) # DataFrame에 대한 평균

#=========================중앙값 구하기=========================
print("========== Median ==========")
print(np.median(scores))
print(scores_df.median()) # DataFrame에 대한 중앙값

#=========================최빈값 구하기=========================
print("========== Mode ==========")
series = pd.Series([1,1,1,2,2,3])
print(series.mode()) 

print("\n")

series = pd.Series([1,2,3,4,5])
print(series.mode()) 

#========================= 산포도 - 분산 구하기=========================
print("========== Variance ==========")

myData = [1, 2, 3, 4]
ndData = np.array(myData)
print("모분산:", ndData.var())
print("표준분산:", np.var(scores)) 
print("dataFrame에 대한 불편분산:",scores_df.var())

#==================================================
summary_df = scores_df.copy()
summary_df['deviation'] = summary_df - summary_df.mean()
print("=====편차=====", summary_df)

summary_df['squared deviation'] = summary_df['deviation'] ** 2
print("=====편차제곱=====",summary_df)

print("=====종합 통계량=====", scores_df.describe())