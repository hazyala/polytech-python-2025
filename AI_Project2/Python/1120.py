import pandas as pd
import numpy as np

anscombe_data = np.load ('Python/data/ch3_anscombe.npy')

#=========================그래프 데이터프레임 만들기=========================
print("========== 그래프 데이터프레임 만들기 ==========")
edges = pd.DataFrame({'source': [0, 1, 2], 
'target': [2, 2, 3],
 'weight': [3, 4, 5],
 'color': ['red', 'blue', 'blue']})
print(edges)

print("========== 데이터 타입 ===========")
print(edges.dtypes)

print("========== 원-핫 인코딩 ==========")
print(pd.get_dummies(edges))

print("========== 특정 열 원-핫 인코딩 ==========")
print(pd.get_dummies(edges, columns=["color"]))

#=========================맵핑으로 원-핫 인코딩=========================
print("========== 맵핑으로 원-핫 인코딩 ==========")
weight_dict = {3:"M", 4:"L", 5:"XL"}
edges["weight_sign"] = edges["weight"].map(weight_dict)
weight_sign = pd.get_dummies(edges["weight_sign"])
print(weight_sign)
#=========================원-핫 인코딩 결과 합치기=========================
print("========== 원-핫 인코딩 결과 합치기 ==========")
print(pd.concat([edges, weight_sign], axis=1))

#========================= 데이터프레임 만들기 =========================
raw_data= {
            'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'],
            'company': ['1st', '1st', '2nd', '2nd', '1st', '1st', '2nd', '2nd','1st', '1st', '2nd', '2nd'],
            'name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze', 'Jacon', 'Ryaner', 'Sone', 'Sloan', 'Piger', 'Riani', 'Ali'],
            'preTestScore': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
            'postTestScore': [25, 94, 57, 62, 70, 25, 94, 57, 62, 70, 62, 70]
           }

df= pd.DataFrame(raw_data, columns= ['regiment', 'company', 'name', 'preTestScore', 'postTestScore'])
print("========== 원본 데이터 ==========")
print(df)

#=========================구간 나누기=========================
print("========== 구간 나누기 ==========")
bins = [0, 25, 50, 75, 100] # bins 정의(0-25, 25-50, 60-75, 75-100)
group_names = ['Low', 'Okay', 'Good', 'Great']
categories = pd.cut(
df['postTestScore'], bins, labels=group_names)
print(categories)

#=========================구간 나누기 결과 합치기=========================
print("========== 구간 나누기 결과 합치기 ==========")
df['categories'] = categories
print(df)

#=========================데이터프레임 만들기 2 =========================
df = pd.DataFrame({'A':[14.00,90.20,90.95,96.27,91.21],'B':[103.02,107.26,110.35,114.23,114.68], 'C':['big','small','big','small','small']})
print("========== 원본 데이터 2 ==========")
print(df)

#=========================정규화와 표준화=========================
df["A"] - df["A"].min()
(df["A"] - df["A"].min()) / (df["A"].max() - df["A"].min())
(df["B"] - df["B"].mean()) / (df["B"].std())
print("========== 정규화와 표준화 결과 ==========")
df["A_normalized"] = (df["A"] - df["A"].min())
df["A_normalized"] = df["A_normalized"] / (df["A"].max() - df["A"].min())
df["B_standardized"] = (df["B"] - df["B"].mean())
df["B_standardized"] = df["B_standardized"] / (df["B"].std())
print(df)