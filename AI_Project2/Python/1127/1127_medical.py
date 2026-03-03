import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os  # 경로 설정을 위해 이 녀석만 하나 추가했사옵니다

#========================= 저장 경로 설정 (추가됨) =========================
# 시각화 저장 경로 설정
save_dir = 'Python/1127/medical_visualization.png'

#=========================의료 데이터 불러오기 및 기초 정보 확인=========================
pd.set_option('display.max_columns', None)
df= pd.read_csv('Python/1127/medical.csv') 
print(df.head())

#=========================컬럼명 확인=========================
print(df.columns)

# 컬럼명 오타 수정
df.rename(columns={'Hipertension':'Hypertension', 'Handcap':'Handicap'}, inplace=True)
print(df.columns)

#========================= 데이터 정보 확인=========================
print(df.info())

#=========================결측치 확인=========================
print(df.isnull().any(axis=1))
print(df.isnull().any(axis=0))

#=========================기초 통계량 확인=========================
print(df.describe())

#=========================이상치 확인 후 제거=========================
df = df[df.Age >= 0]
print(df.Age.min())
df = df[(df.Handicap==0) | (df.Handicap==1)]
print(df['Handicap'].value_counts())

#=========================범주형 변수 확인=========================
df['No-show'] = df['No-show'].map({'Yes':1, 'No': 0})
print(df['No-show'].value_counts())

#=========================데이터 타입 변환 (Datatime으로)=========================
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
df.info()

#=========================새로운 칼럼 생성 (예약일과 내원일의 차이 (대기일)) =========================
df['waiting_day'] = df['AppointmentDay'].dt.dayofyear- df['ScheduledDay'].dt.dayofyear
print(df.info())
print(df.describe())

#=========================대기일이 음수인 이상치 제거=========================
# 대기일이 음수인 데이터는 예약일이 내원일보다 이후인 이상치이므로 제거
df = df[df.waiting_day>=0]
print(df['waiting_day'].min())
#Age 열의 이상치 확인
print(df.Age.unique())
#Age 열의 이상치 제거
df=df[df.Age<=110]
plt.figure(figsize=(16,2))
sns.boxplot(x=df.Age)
plt.savefig(os.path.join(save_dir, "대기일이 음수인 이상치 시각화.png"))
plt.show()

#================================= 목적에 적합한 변수 추출 (예약 취소율 줄이고 예약 취소 여부와 관련된 칼럼은 무엇인가 확인 목적)=================================
# waiting_day(대기일), No-show(예약 취소 여부) 칼럼에서 당일예약과 예약취소의 관련성 확인
a = df[df.waiting_day==0]['waiting_day'].value_counts()
b = df[(df['waiting_day']==0) & (df['No-show']==1)]['waiting_day'].value_counts()
print(b/a)

#10일 이내 대기한 예약과 예약 취소의 관련성 확인
no_show = df[df['No-show']==1]
show = df[df['No-show']==0]
no_show[no_show['waiting_day'] <= 10]['waiting_day'].hist(alpha=0.7, label='no_show')
show[show['waiting_day'] <= 10]['waiting_day'].hist(alpha=0.3, label='show')
plt.legend()
plt.savefig(os.path.join(save_dir, "10일 이내 대기한 예약과 예약 취소의 관련성 시각화.png"))
plt.show()

#ScheduledDay/AppointmentDay와 No-show의 관계 시각화
# ScheduledDay와 No-show의 관계
no_show['ScheduledDay'].hist(alpha=0.7, label='no_show')
show['ScheduledDay'].hist(alpha=0.3, label='show')
plt.legend()
plt.savefig(os.path.join(save_dir, "ScheduledDay와 No-show의 관계 시각화.png"))
plt.show()
no_show['AppointmentDay'].hist(alpha=0.7, label='no_show')
show['AppointmentDay'].hist(alpha=0.3, label='show')
plt.legend()
plt.savefig(os.path.join(save_dir, "AppointmentDay와 No-show의 관계 시각화.png"))
plt.show()

#================= 재방문환자와No-Show 관계 확인 =================
#재방문 환자 확인
print(df.PatientId.value_counts().iloc[0:10])
# PatientId와 waiting_day
data = df[(df['waiting_day']>=50) & (df['No-show']==1)].PatientId.value_counts().iloc[0:10]
print(data)
#SMS_received, wating_day와 No-Show 관계 확인
sns.barplot(y='waiting_day', x='SMS_received', hue='No-show', data=df)
plt.savefig(os.path.join(save_dir, "SMS_received, wating_day와 No-Show 관계 시각화.png"))
plt.show()
# 상관관계 히트맵 시각화
tmp=df[['waiting_day', 'SMS_received', 'No-show']].corr()
sns.heatmap(tmp, annot= True)
plt.savefig(os.path.join(save_dir, "SMS_received, wating_day와 No-Show 관계 히트맵 시각화.png"))
plt.show()

#================= 다양한 변수와 No-Show 관계 확인 =================
#예약을 잡은 날과 실제 병원 방문 날의 차이가 많이 나면 노쇼가 발생하는가?
sns.countplot(x='No-show', data=df)
plt.savefig(os.path.join(save_dir, "예약을 잡은 날과 실제 병원 방문 날의 차이가 많이 나면 노쇼가 발생하는가 시각화.png"))
plt.show()

#4월말 5월 초의 예약의 경우 노쇼가 많이 발생하는가?
df['AppointmentMonth'] = df['AppointmentDay'].dt.month
sns.countplot(x='AppointmentMonth', hue='No-show', data=df)
plt.savefig(os.path.join(save_dir, "4월말 5월 초의 예약의 경우 노쇼가 많이 발생하는가 시각화.png"))
plt.show()
#Wating 기간이 길면 노쇼가 많은가?
sns.histplot(data=df, x='waiting_day', hue='No-show', multiple='stack')
plt.savefig(os.path.join(save_dir, "Wating 기간이 길면 노쇼가 많은가 시각화.png"))
plt.show()


#Wating 기간이 길고 문자 수신을 하지 않은 경우 노쇼가 많은가?
g = sns.displot(data=df, x='waiting_day', hue='No-show', multiple='stack', col='SMS_received', kind='hist')
g.savefig(os.path.join(save_dir, "Wating 기간이 길고 문자 수신을 하지 않은 경우 노쇼가 많은가 시각화.png"))
plt.show()

#=============== 다른 영향의 특성 찾기 전처리 및 시각화 =================
#얼마나 많은 환자가 예정된 약속에 오지 않았는가?
sns.countplot(x='No-show', data=df)
plt.savefig(os.path.join(save_dir, "얼마나 많은 환자가 예정된 약속에 오지 않았는가 시각화.png"))
plt.show()

#성별에 따른 노쇼여부 차이
sns.countplot(x='Gender',hue='No-show', data=df)
plt.savefig(os.path.join(save_dir, "성별에 따른 노쇼여부 차이 시각화.png"))
plt.show()
#일반화 우려에 대한 노쇼의 여성과 남성비율 확인
F = df[(df['Gender']=='F') & (df['No-show']==1)]['Gender'].value_counts()
M= df[(df['Gender']=='M') & (df['No-show']==1)]['Gender'].value_counts()
total_F = df[df['Gender']=='F']['Gender'].value_counts()
total_M = df[df['Gender']=='M']['Gender'].value_counts()
print(F/total_F)
print(M/total_M)

#재정지원 여부에 따른 노쇼 차이
sns.countplot(x='Scholarship', hue='No-show', data=df)
plt.savefig(os.path.join(save_dir, "재정지원 여부에 따른 노쇼 차이 시각화.png"))
plt.show()
#재정지원 여부에 따른 노쇼 비율
scholarship_no_show = df[(df['Scholarship']==1) & (df['No-show']==1)]['Scholarship'].value_counts()
scholarship_total = df[df['Scholarship']==1]['Scholarship'].value_counts()
no_scholarship_no_show = df[(df['Scholarship']==0) & (df['No-show']==1)]['Scholarship'].value_counts()
no_scholarship_total = df[df['Scholarship']==0]['Scholarship'].value_counts()
print(scholarship_no_show/scholarship_total)
print(no_scholarship_no_show/no_scholarship_total)
#알콜중독 여부에 따른 노쇼 차이
sns.countplot(x='Alcoholism', hue='No-show', data=df)
plt.savefig(os.path.join(save_dir, "알콜중독 여부에 따른 노쇼 차이 시각화.png"))
plt.show()
#알콜중독 여부에 따른 노쇼 비율
alcoholism_no_show = df[(df['Alcoholism']==1) & (df['No-show']==1)]['Alcoholism'].value_counts()
alcoholism_total = df[df['Alcoholism']==1]['Alcoholism'].value_counts()
no_alcoholism_no_show = df[(df['Alcoholism']==0) & (df['No-show']==1)]['Alcoholism'].value_counts()
no_alcoholism_total = df[df['Alcoholism']==0]['Alcoholism'].value_counts()
print(alcoholism_no_show/alcoholism_total)
print(no_alcoholism_no_show/no_alcoholism_total)
#고혈합 여부에 따른 노쇼 발생 비교
sns.countplot(x='Hypertension', hue='No-show', data=df)
plt.savefig(os.path.join(save_dir, "고혈합 여부에 따른 노쇼 발생 비교 시각화.png"))
plt.show()
#고혈압 여부에 따른 노쇼 비율
hypertension_no_show = df[(df['Hypertension']==1) & (df['No-show']==1)]['Hypertension'].value_counts()
hypertension_total = df[df['Hypertension']==1]['Hypertension'].value_counts()
no_hypertension_no_show = df[(df['Hypertension']==0) & (df['No-show']==1)]['Hypertension'].value_counts()
no_hypertension_total = df[df['Hypertension']==0]['Hypertension'].value_counts()
print(hypertension_no_show/hypertension_total)
print(no_hypertension_no_show/no_hypertension_total)