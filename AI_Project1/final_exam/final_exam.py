import os
import pathlib
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from tensorflow.keras.utils import image_dataset_from_directory

# ===========================================================================
# 1. 경로 및 환경 설정
# ===========================================================================
# 현재 작업 경로 기준 설정
BASE_DIR = pathlib.Path("/workspace/final_exam")
DATA_DIR = BASE_DIR / "MNIST248"

# 저장 디렉토리 생성
MODEL_DIR = BASE_DIR / "models"
VIS_DIR = BASE_DIR / "visualization"
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(VIS_DIR, exist_ok=True)

# 보고서 파일 경로
REPORT_PATH = BASE_DIR / "Report.txt"

# 학습 상수 설정
IMG_SIZE = (300, 300)
BATCH_SIZE = 32
EPOCHS = 100 

print(f"📂 작업 경로: {BASE_DIR}")
print(f"   - 모델 저장: {MODEL_DIR}")
print(f"   - 그래프 저장: {VIS_DIR}")
print(f"   - 보고서: {REPORT_PATH}")

# ===========================================================================
# 2. 데이터셋 로드
# ===========================================================================
print("\n📦 데이터셋 로드 중...")

train_ds = image_dataset_from_directory(
    DATA_DIR / "training", image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode='categorical', shuffle=True)
val_ds = image_dataset_from_directory(
    DATA_DIR / "validation", image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode='categorical', shuffle=False)
test_ds = image_dataset_from_directory(
    DATA_DIR / "testing", image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode='categorical', shuffle=False)

# [중요] 메모리 최적화: .cache() 제거하여 OOM 방지
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

# ===========================================================================
# 3. 실험 실행 함수
# ===========================================================================
def run_experiment(exp_id, exp_name, use_aug, use_dropout, use_l2):
    # 실험 고유 이름 생성
    full_name = f"{exp_id}_{exp_name}"
    print(f"\n🚀 [실험 {full_name}] 시작... (증강:{use_aug}, Drop:{use_dropout}, L2:{use_l2})")
    
    # --- 모델 구성 (VGG16 기반) ---
    conv_base = keras.applications.vgg16.VGG16(
        weights="imagenet", include_top=False, input_shape=(300, 300, 3))
    conv_base.trainable = False

    inputs = keras.Input(shape=(300, 300, 3))
    x = inputs

    # 1. 데이터 증강 (Augmentation)
    if use_aug:
        x = keras.Sequential([
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
            layers.RandomTranslation(0.1, 0.1)
        ])(x)
    
    x = keras.applications.vgg16.preprocess_input(x)
    x = conv_base(x)
    x = layers.Flatten()(x)

    # 2. L2 규제 (Regularization)
    if use_l2:
        x = layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001))(x)
    else:
        x = layers.Dense(256, activation='relu')(x)

    # 3. 드롭아웃 (Dropout)
    if use_dropout:
        x = layers.Dropout(0.5)(x)

    outputs = layers.Dense(3, activation="softmax")(x)
    model = keras.Model(inputs, outputs)

    model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    # --- 콜백 설정 ---
    model_path = os.path.join(MODEL_DIR, f"{full_name}.h5")
    
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=model_path,    # 위에서 정의한 경로 사용
            save_best_only=True,                
            monitor="val_loss"                  
        )
    ]
    
    # --- 모델 학습 ---
    history = model.fit(
        train_ds, epochs=EPOCHS, 
        validation_data=val_ds, callbacks=callbacks, verbose=2
    )

    # --- 결과 시각화 및 저장 ---
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(1, len(acc) + 1)

    # 정확도 그래프
    plt.figure()
    plt.plot(epochs_range, acc, label='Training Acc')
    plt.plot(epochs_range, val_acc, label='Validation Acc')
    plt.title(f'{full_name} Accuracy')
    plt.legend()
    plt.savefig(os.path.join(VIS_DIR, f"{full_name}_acc.png"))
    plt.close()

    # 손실 그래프
    plt.figure()
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.title(f'{full_name} Loss')
    plt.legend()
    plt.savefig(os.path.join(VIS_DIR, f"{full_name}_loss.png"))
    plt.close()

    # --- 최종 평가 및 결과 기록 ---
    # 저장된 최고 성능 모델 로드 (.h5)
    best_model = keras.models.load_model(model_path)
    test_loss, test_acc = best_model.evaluate(test_ds, verbose=0)
    
    result_msg = (f"[{full_name}] Test Acc: {test_acc:.4f} / Loss: {test_loss:.4f} "
                  f"(Aug:{use_aug}, Drop:{use_dropout}, L2:{use_l2})")
    print(f"✅ 완료: {result_msg}")

    # 리포트에 결과 추가
    with open(REPORT_PATH, "a", encoding="utf-8") as f:
        f.write(result_msg + "\n")

# ===========================================================================
# 4. 실험 자동화 리스트
# ===========================================================================

# (번호, 이름, 증강O/X, DropoutO/X, L2O/X)
experiments_list = [
    ("01", "Baseline",   False, False, False), # 1. 기본
    ("02", "AugOnly",    True,  False, False), # 2. 증강만
    ("03", "Reg_Drop",   False, True,  False), # 3. 규제(Dropout)만
    ("04", "Reg_L2",     False, False, True),  # 4. 규제(L2)만
    ("05", "Reg_DropL2", False, True,  True),  # 5. 규제(Dropout+L2)만
    ("06", "Total_Drop", True,  True,  False), # 6. 증강+Dropout
    ("07", "Total_L2",   True,  False, True),  # 7. 증강+L2
    ("08", "Total_ALL",  True,  True,  True),  # 8. 전부 다 (규제 + Dropout+L2)
] 

# 보고서 초기화
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("=== MNIST 2,4,8 Final Experiment Report ===\n")
    f.write(f"Total Epochs per Model: {EPOCHS}\n\n")

print(f"\n⚡ 총 {len(experiments_list)}개의 실험을 시작합니다. 굿나잇! ⚡")

# 실험 순차 실행
for exp_config in experiments_list:
    try:
        run_experiment(*exp_config)
    except Exception as e:
        print(f"❌ [Error] {exp_config[1]} 실험 실패: {e}")
        with open(REPORT_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{exp_config[0]}_{exp_config[1]}] FAILED: {e}\n")

print("\n🎉 모든 실험 종료! 결과 파일을 확인하세요.")