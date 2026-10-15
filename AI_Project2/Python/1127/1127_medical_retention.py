import os
import pandas as pd

#========================= 경로 설정 =========================
# 어디서 실행해도 같은 csv를 읽도록 파일 위치 기준으로 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir, 'medical.csv'))
print('원본 예약 수 :', len(df))

#========================= 전처리 (1127_medical.py와 같은 기준) =========================
# 컬럼명 오타 수정
df.rename(columns={'Hipertension':'Hypertension', 'Handcap':'Handicap'}, inplace=True)

# 나이 음수, 장애 여부 0/1 이외 값 제거
df = df[df.Age >= 0]
df = df[(df.Handicap==0) | (df.Handicap==1)]

# 노쇼 여부 숫자로 변환 (Yes=1, No=0)
df['No-show'] = df['No-show'].map({'Yes':1, 'No':0})

# 날짜 타입 변환
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])

# 대기일 = 진료일 - 예약일
df['waiting_day'] = df['AppointmentDay'].dt.dayofyear - df['ScheduledDay'].dt.dayofyear

# 대기일 음수(예약일이 진료일보다 뒤인 경우), 나이 110 초과 제거
df = df[df.waiting_day >= 0]
df = df[df.Age <= 110]
print('분석 대상 예약 수 :', len(df))
print('진료일 범위 :', df['AppointmentDay'].min().date(), '~', df['AppointmentDay'].max().date())
print('전체 노쇼율 :', round(df['No-show'].mean()*100, 1), '%')

#========================= 01. 이탈 시점 : 대기 기간별 노쇼율 =========================
# 당일 / 1~7일 / 8~30일 / 31일 이상으로 나눠서 비교
df['wait_group'] = pd.cut(df['waiting_day'], bins=[-1, 0, 7, 30, 1000],
                          labels=['당일', '1-7일', '8-30일', '31일+'])
wait = df.groupby('wait_group', observed=True)['No-show'].agg(['mean', 'size'])
wait['mean'] = (wait['mean']*100).round(1)
print('\n[01] 대기 기간별 노쇼율(%)과 예약 수')
print(wait)

#========================= 02. 효과 검증 : 문자 수신 여부 =========================
# 전체로만 보면 문자 받은 쪽 노쇼가 더 높게 나옴
sms = (df.groupby('SMS_received')['No-show'].mean()*100).round(1)
print('\n[02] 문자 수신 여부별 노쇼율(%) - 전체')
print(sms)

# 문자가 어떤 예약에 갔는지 확인 -> 대기 기간별 문자 수신 비율
sms_share = (df.groupby('wait_group', observed=True)['SMS_received'].mean()*100).round(0)
print('\n[02] 대기 기간별 문자 수신 비율(%)')
print(sms_share)

# 같은 대기 기간끼리 비교하면 결과가 반대로 나오는지 확인
sms_wait = (df.groupby(['wait_group', 'SMS_received'], observed=True)['No-show'].mean()*100).round(1).unstack()
print('\n[02] 대기 기간 x 문자 수신 노쇼율(%)  (0=미수신, 1=수신)')
print(sms_wait)

#========================= 03. 세그먼트 : 직전 예약에 안 온 환자는 또 안 올까? =========================
# 환자별로 진료일 순서대로 정렬해서 직전 예약의 노쇼 여부를 붙임
d = df.sort_values(['PatientId', 'AppointmentDay', 'ScheduledDay']).copy()
d['prev_no_show'] = d.groupby('PatientId')['No-show'].shift()

# 직전 예약이 있는 경우만 비교 (첫 예약은 제외)
prev = d.dropna(subset=['prev_no_show'])
prev_rate = (prev.groupby('prev_no_show')['No-show'].mean()*100).round(1)
print('\n[03] 직전 예약 노쇼 여부별 다음 예약 노쇼율(%)  (0=방문, 1=노쇼)')
print(prev_rate)

# 노쇼가 일부 환자에게 몰려 있는지 확인
patient = df.groupby('PatientId')['No-show'].sum()
repeat = patient[patient >= 2]
print('\n[03] 노쇼 2회 이상 환자 비율 :', round(len(repeat)/len(patient)*100, 1), '%')
print('[03] 이 환자들이 전체 노쇼에서 차지하는 비율 :', round(repeat.sum()/patient.sum()*100, 1), '%')

#========================= 03. 나이대 / 요일별 노쇼율 =========================
df['age_group'] = pd.cut(df['Age'], bins=[-1, 12, 19, 29, 39, 49, 59, 69, 120],
                         labels=['0-12', '10대', '20대', '30대', '40대', '50대', '60대', '70대+'])
age = (df.groupby('age_group', observed=True)['No-show'].mean()*100).round(1)
print('\n[03] 나이대별 노쇼율(%)')
print(age)

# 토요일은 예약이 39건뿐이라 평일만 비교
df['weekday'] = df['AppointmentDay'].dt.dayofweek
weekday = df[df['weekday'] < 5].groupby('weekday')['No-show'].mean()*100
weekday.index = ['월', '화', '수', '목', '금']
print('\n[03] 요일별 노쇼율(%) - 평일')
print(weekday.round(1))

#========================= 04. 우선순위 근거 =========================
# 8일 이상 대기한 예약의 노쇼율
print('\n[04] 8일 이상 대기 예약 노쇼율 :', round(df[df['waiting_day'] >= 8]['No-show'].mean()*100, 1), '%')
print('[04] 요일별 노쇼율 차이(최대-최소) :', round(weekday.max()-weekday.min(), 1), '%p')
