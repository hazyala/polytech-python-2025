#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h> 
#include <string.h> 

#define MAX_LINE_LEN 1024
#define NUM_PEOPLE 2      
#define NUM_SUBJECTS 4    

int scores[NUM_PEOPLE][NUM_SUBJECTS];

void calculate_and_print_averages() {
    double hong_sum = 0.0;
    double seong_sum = 0.0;

    // 2. 개인별 평균 점수 계산
    for (int j = 0; j < NUM_SUBJECTS; j++) {
        hong_sum += scores[0][j];
        seong_sum += scores[1][j];
    }

    printf("\n--- 개인별 평균 점수 ---\n");
    // 소수점 첫째 자리까지만 출력하도록함
    printf("홍길동 평균 점수: %.1lf\n", hong_sum / NUM_SUBJECTS);
    printf("성춘향 평균 점수: %.1lf\n", seong_sum / NUM_SUBJECTS);

    // 3. 각 과목별 평균 점수 계산
    printf("\n--- 과목별 평균 점수 ---\n");
    // 소수점 첫째 자리까지만 출력하도록 "%.1lf"로 수정
    printf("국어 평균: %.1lf\n", ((double)scores[0][0] + scores[1][0]) / NUM_PEOPLE);
    printf("영어 평균: %.1lf\n", ((double)scores[0][1] + scores[1][1]) / NUM_PEOPLE);
    printf("수학 평균: %.1lf\n", ((double)scores[0][2] + scores[1][2]) / NUM_PEOPLE);
    printf("과학 평균: %.1lf\n", ((double)scores[0][3] + scores[1][3]) / NUM_PEOPLE);
}


int main(int argc, char* argv[]) {

    char str_tmp[MAX_LINE_LEN];
    FILE* pFile = NULL;
    int line_count = 0;

    pFile = fopen("simple.csv", "r");
    if (pFile == NULL) {
        printf("simple.csv 파일을 열 수 없습니다.\n");
        return 1;
    }

    // 파일 읽기 및 데이터 저장 (strtok 사용)
    while (line_count < NUM_PEOPLE && (fgets(str_tmp, MAX_LINE_LEN, pFile)) != NULL) {

        char* p;
        int subject_index = 0;

        // 개행 문자 제거
        str_tmp[strcspn(str_tmp, "\n")] = 0;

        // 콤마(,) 기준으로 값 분리
        p = strtok(str_tmp, ",");

        // 숫자로 변환하여 scores 배열에 저장
        while (p != NULL && subject_index < NUM_SUBJECTS) {
            scores[line_count][subject_index] = atoi(p);
            subject_index++;
            p = strtok(NULL, ",");
        }

        line_count++;
    }

    fclose(pFile);

    // 평균 계산 함수 호출
    if (line_count == NUM_PEOPLE) {
        calculate_and_print_averages();
    }
    else {
        printf("ERROR");
    }

    return 0;
}