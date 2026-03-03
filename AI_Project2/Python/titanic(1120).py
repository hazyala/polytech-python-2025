import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)

DATA_DIR = 'Python/data2_titanic' 
print(os.listdir(DATA_DIR))

DATA_DIR = 'Python/data2_titanic'
data_files = sorted([os.path.join(DATA_DIR, filename) for filename in os.listdir(DATA_DIR)] , reverse=True)
print("========== 데이터 파일 목록 ==========")
print(data_files)

# (1) 데이터프레임을각파일에서읽어온후df_list에추가
df_list = []
for filename in data_files:
    df_list.append(pd.read_csv(filename)) 
# (2) 두개의데이터프레임을하나로통합
df = pd.concat(df_list, sort=False) 
# (3) 인덱스초기화
df = df.reset_index(drop=True) 
# (4) 결과출력
print(df.head(5))

#=========================train.csv,test.csv 데이터 구분=========================
print("========== train.csv,test.csv 데이터 구분 ==========")
# (1) train.csv 데이터의 수
number_of_train_dataset = df.Survived.notnull().sum()
print("Train dataset size : ", df.Survived.notnull().sum())
 # (2) test.csv 데이터의 수
number_of_test_dataset = df.Survived.isnull().sum() 
print("Test dataset size : ",df.Survived.isnull().sum())
# (3) train.csv 데이터의 y 값 추출
y_true = df.pop("Survived")[:number_of_train_dataset]
print("y_true :\n", y_true)

#=========================데이터 요약 통계량 출력=========================
print("========== 데이터 요약 통계량 출력 ==========")
# (1) 데이터를소수점두번째자리까지출력
pd.options.display.float_format = '{:.2f}'.format
# (2) 결측치값의합을데이터의개수로나눠비율로출력
print(df.isnull().sum() / len(df) * 100)

#=========================결측치 처리=========================
df.loc[61,"Embarked"] = "S"
df.loc[829,"Embarked"] = "S"
print("========== Embarked 열 결측치 처리 ==========")
print(df)

#=========================데이터 정보 출력=========================
print("========== 데이터 정보 출력 ==========")
print(df.info())

#=========================원-핫 인코딩=========================
def merge_and_get(ldf, rdf, on, how="inner", index=None):
    if index is True:
        return pd.merge(ldf,rdf, how=how, 
left_index=True, right_index=True)
    else:
        return pd.merge(ldf,rdf, how=how, on=on)

one_hot_df = merge_and_get(df, pd.get_dummies(df["Sex"], prefix="Sex"), on=None, index=True) 
one_hot_df = merge_and_get(one_hot_df, pd.get_dummies(df["Pclass"], prefix="Pclass"), on=None, index=True) 
one_hot_df = merge_and_get(one_hot_df, pd.get_dummies(df["Embarked"], prefix="Embarked"), on=None, index=True)
print("========== 원-핫 인코딩 결과 ==========")
print(one_hot_df.head(5))

#=========================원-핫 인코딩 결과 시각화=========================
print("========== 원-핫 인코딩 결과 시각화 ==========")
temp_columns = ["Sex", "Pclass", "Embarked"]
for col_name in temp_columns:
    temp_df = pd.merge(
one_hot_df[col_name], y_true, left_index=True, right_index=True)
sns.countplot(x="Survived", hue=col_name, data=temp_df)
plt.show()

#=========================원-핫 인코딩 결과 시각화 2=========================
temp_df = pd.merge(one_hot_df[temp_columns], y_true, left_index=True, right_index=True)
g = sns.catplot(x="Embarked", hue="Pclass", col="Survived",data=temp_df, kind="count",height=4, aspect=.7)
plt.show()

temp_df = pd.merge(one_hot_df[temp_columns], y_true, left_index=True, right_index=True)
g = sns.catplot(x="Pclass", hue="Sex", col="Survived", data=temp_df, kind="count", height=4, aspect=.7)
plt.show()

temp_df = pd.merge(one_hot_df[temp_columns], y_true, left_index=True, right_index=True)
g = sns.catplot(x="Embarked", hue="Sex", col="Survived",data=temp_df, kind="count",height=4, aspect=.7)
plt.show()

#=========================상관관계 히트맵 그리기=========================
crosscheck_columns = [
    col_name 
    for col_name in one_hot_df.columns.tolist() 
    if col_name.split("_")[0] in temp_columns 
    and "_" in col_name
] 
# temp 열
temp_df= pd.merge(one_hot_df[crosscheck_columns], y_true,left_index=True, right_index=True)
corr= temp_df.corr()
sns.set()
ax = sns.heatmap(corr, annot=True, linewidths=.5, cmap="YlGnBu")
plt.show()