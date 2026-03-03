import pandas as pd
import numpy as np
raw_data= {'first_name': ['Jason', np.nan, 'Tina', 'Jake', 'Amy'],
           'last_name': ['Miller', np.nan, 'Ali', 'Milner', 'Cooze'], 
           'age': [42, np.nan, 36, 24, 73], 
           'sex': ['m', np.nan, 'f', 'm', 'f'], 
           'preTestScore': [4, np.nan, np.nan, 2, 3],
           'postTestScore': [25, np.nan, np.nan, 62, 70]}
df= pd.DataFrame(raw_data, columns= ['first_name', 'last_name', 'age', 'sex', 'preTestScore', 'postTestScore'])
print(df)
df.isnull().sum() / len(df)

print("========== 결측치 처리 ==========", df.dropna())  #결측치가 있는 행 제거

df_no_missing = df.dropna()
print(df_no_missing)
df_cleaned=df.dropna(how='all')
print(df_cleaned)

#=========================특정 축의 결측치 처리=========================
df['location'] = np.nan
df.dropna(axis=1, how='all')
print(df)

df.dropna(axis=0, thresh=1)
df.dropna(thresh=5)
print(df)

df.fillna(0)
print(df)

#=========================특정 값으로 결측치 채우기=========================
df["preTestScore"].fillna(df["preTestScore"].mean(), inplace=True)
print(df)

df.groupby("sex")["postTestScore"].transform("mean")
df["postTestScore"].fillna(df.groupby("sex")["postTestScore"].transform("mean"), inplace=True)
print(df)