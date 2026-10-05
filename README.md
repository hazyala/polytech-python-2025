# Python GUI와 ML 수업 기록

Tkinter 계산기·주스 키오스크 과제와 TensorFlow/Keras·scikit-learn 실습을 보관한 2025년 수업 저장소.

## 먼저 실행할 GUI 과제

[계산기와 주스 키오스크](Python_2025_2_final_exam/README.md)는 독립적인 데스크톱 예제다. 계산기는 수식 입력·결과·오류를 처리하고, 키오스크는 메뉴와 컵 크기로 가격을 계산한다.

![계산기](Python_2025_2_final_exam/README/calculator.png)

## ML 자료 위치

| 폴더 | 내용 |
|---|---|
| `AI_Project1/` | Keras 학습, 모델 비교·regularization, 이미지 분류 실습 |
| `AI_Project2/` | Python·scikit-learn 분류 실습, 노트북과 데이터 |
| `Python_2025_2_final_exam/` | Tkinter GUI 두 개와 메뉴 asset |

ML 스크립트는 날짜별 실험이며 공통 pipeline이나 requirements가 없다. 각 파일의 import, 데이터 경로, 모델 저장 경로를 확인한다. 데이터·이미지 파일이 저장소 대부분을 차지하므로 파일 수를 프로젝트 코드 규모로 해석하지 않는다. 정확도나 모델 비교 결과를 새로 측정한 것처럼 추가하지 않는다.

GUI 실행은 하위 README를 따른다. ML은 TensorFlow/Keras·NumPy·Matplotlib 또는 scikit-learn 등의 파일별 의존성과 dataset이 필요하며 하나의 설치 명령으로 모두 재현된다고 안내하지 않는다.
