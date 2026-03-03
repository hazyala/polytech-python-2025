from tensorflow import keras
from tensorflow.keras import layers     
import numpy as np

# 전체 포괄 학습 =================================================================================

# vocabulary_size = 10000
# num_tags = 100
# num_departments = 4

# tittle = keras.Input(shape=(vocabulary_size,), name='title')
# text_body = keras.Input(shape=(vocabulary_size,), name='text_body')
# tags = keras.Input(shape=(num_tags,), name='tags')

# feature = layers.concatenate([tittle, text_body, tags])
# feature = layers.Dense(64, activation='relu')(feature)

# priority = layers.Dense(1, activation='sigmoid', name='priority')(feature)
# department = layers.Dense(num_departments, activation='softmax', name='department')(feature)

# num_samples = 1280
# tittle_data = np.random.randint(0,2, size=(num_samples, vocabulary_size))
# text_body_data = np.random.randint(0,2, size=(num_samples, vocabulary_size))
# tags_data = np.random.randint(0,2, size=(num_samples, num_tags))

# priority_data = np.random.random(size=(num_samples, 1))
# department_data = np.random.randint(0,2, size=(num_samples, num_departments))

# model = keras.Model(inputs=[tittle, text_body, tags], outputs=[priority, department])

# model.compile(optimizer='rmsprop', loss=["mean_squared_error", "categorical_crossentropy"],metrics=[["mean_absolute_error"], ["accuracy"]])
# model.fit ([tittle_data, text_body_data, tags_data],[priority_data, department_data],epochs=1)
# model.evaluate([tittle_data, text_body_data, tags_data],[priority_data, department_data])
# priority_preds, department_preds = model.predict([tittle_data, text_body_data, tags_data])
# keras.utils.plot_model(model, "ticket_classifier1.png")

# 배치 사이즈 지정 학습 ============================================================================

# vocabulary_size = 10000
# num_tags = 100
# num_departments = 4

# title = keras.Input(shape=(vocabulary_size,), name='title')
# text_body = keras.Input(shape=(vocabulary_size,), name='text_body')
# tags = keras.Input(shape=(num_tags,), name='tags')

# title_feature = layers.Dense(128, activation='relu')(title)
# text_body_feature = layers.Dense(128, activation='relu')(text_body)
# tags_feature = tags

# features = layers.Concatenate()([title_feature, text_body_feature, tags_feature])
# features = layers.Dense(1024, activation='relu')(features)


# priority = layers.Dense(128, activation="sigmoid", name='priority')(features)
# priority = layers.Dense(1, activation='sigmoid')(priority)


# department_1 = layers.Dense(128, activation='relu')(features)
# department_2 = layers.Dense(128, activation='relu')(department_1)
# department = layers.Dense(num_departments, activation="softmax", name='department')(department_2)


# model = keras.Model(inputs=[title, text_body, tags], outputs=[priority, department])

# num_samples = 1280

# title_data = np.random.randint(0, 2, size=(num_samples, vocabulary_size))
# text_body_data = np.random.randint(0, 2, size=(num_samples, vocabulary_size))
# tags_data = np.random.randint(0, 2, size=(num_samples, num_tags))

# priority_data = np.random.randint(0, 2, size=(num_samples, 1))
# department_data = np.random.randint(0, 2, size=(num_samples, num_departments))


# model.compile(optimizer='rmsprop',loss=["mean_squared_error", "categorical_crossentropy"], metrics=[["mean_absolute_error"], ["accuracy"]])
# model.fit([title_data, text_body_data, tags_data],[priority_data, department_data],epochs=1,)
# print(model.evaluate([title_data, text_body_data, tags_data],[priority_data, department_data]))
# priority_preds, department_preds = model.predict([title_data, text_body_data, tags_data])
# print(priority_preds, department_preds)
# keras.utils.plot_model(model, "ticket_classifier2.png")

# 배치 사이즈 지정 학습 최종 과제 ==============================================================================================

# 1. 파라미터 정의 
vocabulary_size = 10000
num_tags = 100
num_departments = 4

# 2. Input Layer 3개 정의 
title = keras.Input(shape=(vocabulary_size,), name='title')
text_body = keras.Input(shape=(vocabulary_size,), name='text_body')
tags = keras.Input(shape=(num_tags,), name='tags')

# 3. 각 Input의 개별 처리 
title_feature = layers.Dense(128, activation='relu')(title)
text_body_feature = layers.Dense(128, activation='relu')(text_body)
tags_feature = tags

# 4. Concatenate (세 개의 개별 특징을 하나의 벡터로 결합)
features = layers.Concatenate()([title_feature, text_body_feature, tags_feature])

# 5. 결합 후 공통 Dense Layer의 결합된 특징을 다음 Dense 레이어로 전달
shared_features = layers.Dense(1024, activation='relu')(features)

# 6. Priority 출력 경로 
priority_path = layers.Dense(128, activation="relu")(shared_features)
priority = layers.Dense(1, activation='sigmoid', name='priority')(priority_path)

# 7. Department 출력 경로 
department_path_1 = layers.Dense(128, activation='relu')(shared_features)
department_path_2 = layers.Dense(128, activation='relu')(department_path_1)
department = layers.Dense(num_departments, activation="softmax", name='department')(department_path_2)

# 8. Model 생성
model = keras.Model(inputs=[title, text_body, tags], outputs=[priority, department])

num_samples = 1280
title_data = np.random.randint(0, 2, size=(num_samples, vocabulary_size))
text_body_data = np.random.randint(0, 2, size=(num_samples, vocabulary_size))
tags_data = np.random.randint(0, 2, size=(num_samples, num_tags))

priority_data = np.random.random(size=(num_samples, 1)) 
department_data = np.random.randint(0, 2, size=(num_samples, num_departments))

model.compile(optimizer='rmsprop',loss=["mean_squared_error", "categorical_crossentropy"],metrics=[["mean_absolute_error"], ["accuracy"]])

# 9. 학습 및 평가
model.fit([title_data, text_body_data, tags_data],[priority_data, department_data],epochs=1,)
print(model.evaluate([title_data, text_body_data, tags_data],[priority_data, department_data]))
priority_preds, department_preds = model.predict([title_data, text_body_data, tags_data])

# 10. 그림 저장
keras.utils.plot_model(model, "ticket_classifier3.png", show_shapes=True)