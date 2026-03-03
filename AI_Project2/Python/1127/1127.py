import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#=========데이터 타입 확인 =========
d = pd.DataFrame({
 'date': ['2019-01-03', '2021-11-22', '2023-01-05'],
 'name':['J','Y','O'],
 'value':['123','456','789']
 })

t1 = pd.to_datetime(d.date, format='%Y-%m-%d')
t2 = pd.to_numeric(d.value)

print("날짜 데이터 추출 : ", t1)
print("데이터 확인 :", t2)

#=========결측치 처리 =========
df= pd.DataFrame( np.random.randn(8, 3),columns=['C1', 'C2', 'C3'])
df.loc[2, 'C2'] = np.nan
df.loc[3, 'C2'] = np.nan
print("평균\n",df)

df = df.fillna(0)
print("결측치 0으로 대체\n",df)

df= df.fillna(df.mean())
print("결측치\n",df)

# #========= 결측치 확인 =========
# print("결측치 확인\n",df.isnull().sum())

# #========== 컬럼별 결측치 ==========
# df2= pd.DataFrame({
#     'A':[1, 2, np.nan, 4],
#     'B':[np.nan, 2, np.nan, 4],
#     'C':[1, 2, 3, 4]
# })
# print("컬럼별 결측치\n", df2.isnull().sum())
# #========= 행별 결측치 ==========
# print("행별 결측치\n", df2.isnull().sum(axis=1))

# #========= 평균별 결측치 대체 =========
# df2= df2.fillna(df2.mean())
# print("평균별 결측치 대체\n", df2)

df = pd.DataFrame(
np.random.randn(8, 3),columns=['C1', 'C2', 'C3'])
df.loc[2, 'C2'] = np.nan
df.loc[3, 'C2'] = np.nan
df['location'] = ['서울','서울','경기','인천', '강원', '경기','서울','경기']
df.loc[3, 'location'] = np.nan
df.loc[7, 'location'] = np.nan
print("지역열 추가",df)
df3 = df['location'].fillna(df['location'].mode()[0])
print("지역만 보기",df3)


df= pd.DataFrame(np.random.randn(8, 3),columns=['C1', 'C2', 'C3'])
df.loc[2, 'C2'] = np.nan
df.loc[3, 'C2'] = np.nan
print(df)
df= df.dropna()
print(df)

a= ['A','B','A','C','C','A','B','A','D','D','A','D']
a= pd.Series(a)
a_dict= {'A':1, 'B':2, 'C':3, 'D':4}
b= a.map(a_dict)
p= pd.DataFrame({'변환전': a, '변환후':b})
print(p)

#========= 이상치 처리 =========
df = pd.DataFrame(np.random.randn(8, 3), columns=['C1', 'C2', 'C3'])
df.loc[1, 'C1'] = 11
df.loc[3, 'C2'] = -10
plt.boxplot([df['C1'], df['C3']])
plt.show() #이상치가 있는데, 이상치가 박스플롯에 표시됨
# 목적 자체가 이상치를 확인하는 것이라면 이상치 제거를 하지 않음 이상한게 소중한 데이터일 수 있음

#========== 목적에 맞는 변수 추출 및 히트맵 시각화 =========
df = pd.DataFrame(np.random.randn(8, 3),columns=['C1', 'C2', 'C3'])
df.loc[1, 'C1'] = 11
df.loc[3, 'C3'] = -10
sns.heatmap(df.corr(), annot=True)
plt.show()

