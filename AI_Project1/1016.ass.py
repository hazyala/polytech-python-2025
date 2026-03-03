import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from keras import callbacks
import os

# === 1. 설정 및 데이터 전처리 ===

# 하이퍼파라미터
NUM_WORDS = 1000
EPOCHS = 200
BATCH_SIZE = 512

# 모델 저장 디렉토리 생성
if not os.path.exists('best_models'):
    os.makedirs('best_models')

# 데이터 로드
(train_data, train_labels), (test_data, test_labels) = keras.datasets.imdb.load_data(num_words=NUM_WORDS)

# 전처리 함수: Multi-hot 인코딩
def multi_hot_sequences(sequences, dimension):
    results = np.zeros((len(sequences), dimension))
    for i, word_indices in enumerate(sequences):
        results[i, word_indices] = 1.0
    return results

# 데이터 전처리 적용
train_data = multi_hot_sequences(train_data, dimension=NUM_WORDS)
test_data = multi_hot_sequences(test_data, dimension=NUM_WORDS)
train_labels = np.reshape(train_labels, (-1, 1))
test_labels = np.reshape(test_labels, (-1, 1))


# === 2. 모델 정의 ===

# 6개의 비교 모델 정의
models = {
    'baseline': keras.Sequential([
        keras.layers.Dense(16, activation='relu', input_shape=(NUM_WORDS,)),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ]),
    'smaller': keras.Sequential([
        keras.layers.Dense(4, activation='relu', input_shape=(NUM_WORDS,)),
        keras.layers.Dense(4, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ]),
    'bigger': keras.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(NUM_WORDS,)),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ]),
    'l2': keras.Sequential([
        keras.layers.Dense(16, kernel_regularizer=keras.regularizers.l2(0.001), activation='relu', input_shape=(NUM_WORDS,)),
        keras.layers.Dense(16, kernel_regularizer=keras.regularizers.l2(0.001), activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ]),
    'dropout': keras.Sequential([
        keras.layers.Dense(16, activation='relu', input_shape=(NUM_WORDS,)),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(1, activation='sigmoid')
    ]),
    'L2+Dropout': keras.Sequential([
        keras.layers.Dense(16, kernel_regularizer=keras.regularizers.l2(0.001), activation='relu', input_shape=(NUM_WORDS,)),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(16, kernel_regularizer=keras.regularizers.l2(0.001), activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(1, activation='sigmoid')
    ])
}

histories = {}
best_model_info = {'name': '', 'accuracy': -1, 'path': ''}

# === 3. 모델 학습 및 Callback 적용 ===

for name, model in models.items():
    # 모델 컴파일
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy', 'binary_crossentropy'])

    model_file_path = f'best_models/best_{name}_model.h5'
    
    # 콜백 1: ModelCheckpoint (최고 성능 모델 저장)
    checkpoint = callbacks.ModelCheckpoint(filepath=model_file_path,
                                 monitor='val_accuracy',
                                 save_best_only=True,
                                 mode='max',
                                 verbose=0)

    # 콜백 2: EarlyStopping (조기 종료 및 최고 가중치 복원)
    early_stopping = callbacks.EarlyStopping(monitor='val_accuracy',
                                   patience=20,
                                   mode='max',
                                   verbose=1,
                                   restore_best_weights=True) # 최고 성능 가중치로 복원

    print(f"\n--- [{name.title()}] 모델 학습 시작 ---")
    
    # 모델 학습
    history = model.fit(train_data, train_labels,
                        epochs=EPOCHS,
                        batch_size=BATCH_SIZE,
                        validation_data=(test_data, test_labels),
                        callbacks=[checkpoint, early_stopping],
                        verbose=2)

    histories[name] = history

    # 각 모델의 최고 성능(정확도) 출력
    best_val_acc = max(history.history['val_accuracy'])
    print(f"[{name.title()}] 최고 검증 정확도: {best_val_acc:.4f}")

    # 전체 중 최고 모델 정보 업데이트
    if best_val_acc > best_model_info['accuracy']:
        best_model_info.update({'name': name, 'accuracy': best_val_acc, 'path': model_file_path})


# === 4. 최고 모델 불러오기 (Load) 및 평가 ===

print("\n" + "="*50)
print(f"전체 모델 중 최고 모델: {best_model_info['name'].title()}")
print(f"최고 검증 정확도: {best_model_info['accuracy']:.4f}")
print(f"저장 경로: {best_model_info['path']}")

try:
    # 최고 모델 로드
    loaded_best_model = tf.keras.models.load_model(best_model_info['path'])
    print(f"\n'{best_model_info['path']}'에서 모델을 성공적으로 불러왔습니다.")
    
    # 불러온 모델 성능 재확인
    loss, acc, _ = loaded_best_model.evaluate(test_data, test_labels, verbose=0)
    print(f"불러온 모델의 검증 정확도: {acc:.4f}")
except Exception as e:
    print(f"\n모델을 불러오는 중 오류 발생: {e}")
print("="*50)


# === 5. 결과 그래프 출력 ===

# 그래프 출력 함수
def plot_history(histories, key='binary_crossentropy'):
    plt.figure(figsize=(16,10))

    for name, history in histories:
        val = plt.plot(history.epoch, history.history['val_'+key],
                       '--', label=name.title()+' Val')
        plt.plot(history.epoch, history.history[key], color=val[0].get_color(),
                 label=name.title()+' Train')

    plt.xlabel('Epochs')
    plt.ylabel(key.replace('_',' ').title())
    plt.legend()
    # 조기 종료로 epoch 수가 다를 수 있으므로, 가장 긴 epoch 기준으로 xlim 설정
    max_epoch = max([len(h.epoch) for _, h in histories]) - 1
    plt.xlim([0, max_epoch])
    plt.grid(True)
    plt.title(f'Model Comparison: {key.replace("_"," ").title()}', fontsize=16)
    plt.show()


# 손실(Loss) 그래프
plot_history([(name, histories[name]) for name in histories])


# 정확도(Accuracy) 그래프
plot_history([(name, histories[name]) for name in histories], key='accuracy')