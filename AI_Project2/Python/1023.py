import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Python/data/ch2_scores_em.csv', index_col='student number')
scores = np.array(df['english'])[:10]
scores_df = pd.DataFrame({'scores': scores}, index=pd.Index(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], name='student'))
z = (scores_df - scores_df.mean()) / scores_df.std()
print(z)

print(np.mean(z))
print(np.std(z, ddof=0))

z=50+10*(scores - np.mean(scores))/np.std(scores)
print(z)

#도수분포표
english_scores = np.array(df['english'])
print(pd.Series(english_scores).describe())

freq,_ = np.histogram(english_scores, bins=10, range=(0,100))
print(freq)

freq_class = [f'{i}~{i+10}' for i in range(0,100,10)]
freq_dist_df = pd.DataFrame({'frequency': freq}, index=pd.Index(freq_class, name='class'))
print("데이터 시각화 (도수분포표) : ", freq_dist_df)

class_value = [(i+i+10)//2 for i in range(0,100,10)]
print("계급값 : ",class_value)

rel_freq = freq / freq.sum()
print("상대도수 : ", rel_freq)

cum_rel_freq = np.cumsum(rel_freq)
print("누적상대도수 : ",cum_rel_freq)

freq_dist_df['class value'] = class_value
freq_dist_df['relative frequency'] = rel_freq
freq_dist_df['cumulative relative frequency'] = cum_rel_freq
freq_dist_df = freq_dist_df[['class value', 'frequency', 'relative frequency', 'cumulative relative frequency']]
print("==도수분포표에 계급값, 상대도수, 누적도수 추가== \n", freq_dist_df)

freq_dist_df.loc[freq_dist_df['frequency'].idxmax(), 'class value']
print("최빈값 :", freq_dist_df.loc[freq_dist_df['frequency'].idxmax(), 'class value'])

freq_4, bins_4 = np.histogram(english_scores, bins=np.arange(0, 101, 4))
freq_class_4 = [f'{i}~{i+4}' for i in range(0,100,4)]
freq_dist_df_4 = pd.DataFrame({'frequency': freq_4}, index=pd.Index(freq_class_4, name='class'))
freq_dist_df_4['class value'] = [(i+i+4)//2 for i in range(0,100,4)]
rel_freq_4 = freq_4 / freq_4.sum()
cum_rel_freq_4 = np.cumsum(rel_freq_4)
freq_dist_df_4['relative frequency'] = rel_freq_4
freq_dist_df_4['cumulative relative frequency'] = cum_rel_freq_4
freq_dist_df_4 = freq_dist_df_4[['class value', 'frequency', 'relative frequency', 'cumulative relative frequency']]
print("==도수분포표(계급간격 4) 에 계급값, 상대도수, 누적도수 추가== \n", freq_dist_df_4)       
print("최빈값(계급간격 4) :", freq_dist_df_4.loc[freq_dist_df_4['frequency'].idxmax(), 'class value'])

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(1,1,1)
freq,_,_ = ax.hist(english_scores, bins=10, range=(0,100))
ax.set_xlabel('Scores')
ax.set_ylabel('person umber')
ax.set_xticks(np.linspace(0,100,10+1))
ax.set_yticks(np.arange(0, freq.max()+1))
plt.show()

fig = plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(1,1,1)
ax2 = ax1.twinx()
weights = np.ones_like(english_scores) / len(english_scores)
rel_freq,_, _ = ax1.hist(english_scores, bins=25, range=(0,100), weights=weights)
cum_rel_freq = np.cumsum(rel_freq)
class_value = [(i+(i+4))//2 for i in range(0,100,4)]
ax2.plot(class_value, cum_rel_freq, ls='--', color='gray', marker='o')
ax1.set_xlabel('Scores')
ax1.set_ylabel('relative frequency')
ax2.set_ylabel('cumulative relative frequency')
ax1.set_xticks(np.linspace(0,100,25+1))
plt.show()

fig = plt.figure(figsize=(5,6))
ax = fig.add_subplot(1,1,1)
ax.boxplot(english_scores,label=['english'])
plt.show()

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

x = range (0, 100)
y = [v*v for v in x]

ax1.plot(x,y)
ax2.bar(x,y)

plt.show()