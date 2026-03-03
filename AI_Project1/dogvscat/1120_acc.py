import os, shutil, pathlib
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import image_dataset_from_directory

# 데이터셋 준비 
original_dir = pathlib.Path("train")
new_base_dir = pathlib.Path("cats_vs_dogs_small")

def make_subset(subset_name, start_index, end_index):
    for category in ("cat", "dog"):
        dir = new_base_dir / subset_name / category
        os.makedirs(dir, exist_ok=True)
        fnames = [f"{category}.{i}.jpg" for i in range(start_index, end_index)]
        for fname in fnames:
            src = original_dir / fname
            if os.path.exists(src):
                shutil.copyfile(src, dir / fname)

# 이미 분리되어 있다면 주석 처리
# make_subset("train", start_index=0, end_index=1000)
# make_subset("validation", start_index=1000, end_index=1500)
# make_subset("test", start_index=1500, end_index=2500)

# 이미지 데이터셋 로드
train_dataset = image_dataset_from_directory(
    new_base_dir / "train", image_size=(180,180), batch_size=32)
validation_dataset = image_dataset_from_directory(
    new_base_dir / "validation", image_size=(180,180), batch_size=32)
test_dataset = image_dataset_from_directory(
    new_base_dir / "test", image_size=(180,180), batch_size=32)

### -------- 1. 증강 전 모델 --------
inputs = keras.Input(shape=(180,180,3))
x = layers.Rescaling(1./255)(inputs)
x = layers.Conv2D(32, 3, activation="relu")(x)
x = layers.MaxPooling2D(2)(x)
x = layers.Conv2D(64, 3, activation="relu")(x)
x = layers.MaxPooling2D(2)(x)
x = layers.Conv2D(128, 3, activation="relu")(x)
x = layers.MaxPooling2D(2)(x)
x = layers.Conv2D(256, 3, activation="relu")(x)
x = layers.MaxPooling2D(2)(x)
x = layers.Conv2D(256, 3, activation="relu")(x)
x = layers.Flatten()(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model_no_aug = keras.Model(inputs=inputs, outputs=outputs)

model_no_aug.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

# [추가] 최고의 모델을 저장하는 콜백
callbacks_no_aug = [
    keras.callbacks.ModelCheckpoint(
        filepath="best_model_no_aug.keras",
        save_best_only=True,
        monitor="val_loss"
    )
]

history_no_aug = model_no_aug.fit(
    train_dataset,
    epochs=100,
    validation_data=validation_dataset,
    callbacks=callbacks_no_aug # 콜백 적용
)

# ---- 증강 전 그래프 저장 ----
epochs_range = range(1, len(history_no_aug.history["accuracy"]) + 1)
plt.figure()
plt.plot(epochs_range, history_no_aug.history["accuracy"], "bo", label="Train Acc")
plt.plot(epochs_range, history_no_aug.history["val_accuracy"], "r", label="Val Acc")
plt.title("Training and Validation Accuracy (No Augmentation)")
plt.legend()
plt.savefig("1_accuracy.jpg", bbox_inches="tight", dpi=200) # 그래프 저장
plt.show()

plt.figure()
plt.plot(epochs_range, history_no_aug.history["loss"], "bo", label="Train Loss")
plt.plot(epochs_range, history_no_aug.history["val_loss"], "r", label="Val Loss")
plt.title("Training and Validation Loss (No Augmentation)")
plt.legend()
plt.savefig("1_loss.jpg", bbox_inches="tight", dpi=200) # 그래프 저장
plt.show()

# 저장된 최고의 모델을 불러와 테스트
best_model_no_aug = keras.models.load_model("best_model_no_aug.keras")
test_loss, test_acc = best_model_no_aug.evaluate(test_dataset)
print(f"증강 전 모델 테스트 정확도: {test_acc:.3f}")


### -------- 2. 증강 후 모델 --------
inputs2 = keras.Input(shape=(180,180,3))
x2 = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.2)
])(inputs2)
x2 = layers.Rescaling(1./255)(x2)
x2 = layers.Conv2D(32, 3, activation="relu")(x2)
x2 = layers.MaxPooling2D(2)(x2)
x2 = layers.Conv2D(64, 3, activation="relu")(x2)
x2 = layers.MaxPooling2D(2)(x2)
x2 = layers.Conv2D(128, 3, activation="relu")(x2)
x2 = layers.MaxPooling2D(2)(x2)
x2 = layers.Conv2D(256, 3, activation="relu")(x2)
x2 = layers.MaxPooling2D(2)(x2)
x2 = layers.Conv2D(256, 3, activation="relu")(x2)
x2 = layers.Flatten()(x2)
x2 = layers.Dropout(0.5)(x2)
outputs2 = layers.Dense(1, activation="sigmoid")(x2)
model_aug = keras.Model(inputs=inputs2, outputs=outputs2)

model_aug.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

# 최고의 모델을 저장하는 콜백
callbacks_aug = [
    keras.callbacks.ModelCheckpoint(
        filepath="best_model_aug.keras",
        save_best_only=True,
        monitor="val_loss"
    )
]

history_aug = model_aug.fit(
    train_dataset,
    epochs=100,
    validation_data=validation_dataset,
    callbacks=callbacks_aug # 콜백 적용
)

# ---- 증강 후 그래프 저장 ----
epochs_range_aug = range(1, len(history_aug.history["accuracy"]) + 1)
plt.figure()
plt.plot(epochs_range_aug, history_aug.history["accuracy"], "bo", label="Train Acc")
plt.plot(epochs_range_aug, history_aug.history["val_accuracy"], "r", label="Val Acc")
plt.title("Training and Validation Accuracy (With Augmentation)")
plt.legend()
plt.savefig("2_augmentation_accuracy.jpg", bbox_inches="tight", dpi=200) # 그래프 저장
plt.show()

plt.figure()
plt.plot(epochs_range_aug, history_aug.history["loss"], "bo", label="Train Loss")
plt.plot(epochs_range_aug, history_aug.history["val_loss"], "r", label="Val Loss")
plt.title("Training and Validation Loss (With Augmentation)")
plt.legend()
plt.savefig("2_augmentation_loss.jpg", bbox_inches="tight", dpi=200) # 그래프 저장
plt.show()

# 저장된 최고의 모델을 불러와 테스트
best_model_aug = keras.models.load_model("best_model_aug.keras")
test_loss, test_acc = best_model_aug.evaluate(test_dataset)
print(f"증강 후 모델 테스트 정확도: {test_acc:.3f}")