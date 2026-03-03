#define _CRT_SECURE_NO_WARNINGS

#define MIN(x,y) ((x) < (y) ? (x) : (y))
#define MAX(x,y) ((x) > (y) ? (x) : (y))

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Windows.h>
#include <math.h>


// PGM 이미지 파일을 읽고 통계를 계산하여 숫자를 구별하는 프로그램

enum FORMAT { EMPTY, GREY, RGB, YCBCR, YCBCR420, BLOCK };

typedef struct { // 이미지 데이터 구조체
    unsigned int rows;
    unsigned int cols;
    char format;
    unsigned long total; // Bytes per image (픽셀 수)
    unsigned int levels; // 최대 레벨 (e.g., 255)
    short* content; // 픽셀 값 (short 사용)
} ImageType;
typedef ImageType* Image;

// 이미지 메모리 할당
Image imageAllocate(unsigned int rows, unsigned int cols, char format, unsigned int levels) {
    Image im = (Image)malloc(sizeof(ImageType));
    if (!im) {
        perror("Memory allocation failed for ImageType");
        return NULL;
    }
    im->rows = rows;
    im->cols = cols;
    im->format = format;
    im->levels = levels;
    im->content = NULL;
    if (im->format == EMPTY) return im;

    switch (im->format) {
    case GREY:
        im->total = im->cols * im->rows;
        break;
    case RGB:
        im->total = 3 * im->cols * im->rows;
        break;
    default:
        im->total = 0; // 기타 형식 처리
        break;
    }

    if (im->total > 0) {
        im->content = (short*)malloc(im->total * sizeof(short));
        if (!im->content) {
            perror("Memory allocation failed for image content");
            free(im);
            return NULL;
        }
    }
    return im;
}

// PGM 이미지 파일 읽기 (P5: GREY, P6: RGB 지원)
Image readPBMImage(const char* filename) {
    FILE* pgmFile;
    int k;

    char signature[3];
    unsigned int cols = 0, rows = 0, levels = 0;

    Image im = imageAllocate(0, 0, EMPTY, 0);

    pgmFile = fopen(filename, "rb");
    if (pgmFile == NULL) {
        perror("Cannot open file to read");
        return im;
    }

    // 파일 시그니처 읽기
    if (fgets(signature, sizeof(signature), pgmFile) == NULL) {
        perror("Failed to read signature");
        fclose(pgmFile);
        return im;
    }

    if (strcmp(signature, "P5") != 0 && strcmp(signature, "P6") != 0) {
        perror("Wrong file type (Only P5/P6 supported)");
        fclose(pgmFile);
        return im;
    }

    // 헤더 정보 읽기 (cols, rows, levels)
    if (fscanf(pgmFile, "%d %d %d", &cols, &rows, &levels) != 3) {
        perror("Failed to read header info");
        fclose(pgmFile);
        return im;
    }
    fgetc(pgmFile); // 개행 문자 (또는 공백) 건너뛰기

    if (strcmp(signature, "P5") == 0) {
        // GREY (흑백) 이미지 처리
        Image new_im = imageAllocate(rows, cols, GREY, levels);
        if (new_im->content == NULL) { fclose(pgmFile); return im; }

        for (k = 0; k < new_im->total; ++k) {
            new_im->content[k] = (unsigned char)fgetc(pgmFile);
        }
        free(im);
        im = new_im;
    }
    else if (strcmp(signature, "P6") == 0) {
        // RGB 이미지 처리 (현재 과제는 흑백 이미지의 통계만 사용하므로 RGB 지원은 일반적이지 않으나, 기존 코드를 유지)
        Image new_im = imageAllocate(rows, cols, RGB, levels);
        if (new_im->content == NULL) { fclose(pgmFile); return im; }

        unsigned long gOffset = new_im->cols * new_im->rows;
        unsigned long bOffset = 2 * new_im->cols * new_im->rows;
        for (k = 0; k < new_im->total / 3; ++k) {
            new_im->content[k] = (unsigned char)fgetc(pgmFile);
            new_im->content[k + gOffset] = (unsigned char)fgetc(pgmFile);
            new_im->content[k + bOffset] = (unsigned char)fgetc(pgmFile);
        }
        free(im);
        im = new_im;
    }

    fclose(pgmFile);
    return im;
}

// 가로(X축) 위치 평균 및 분산 계산
void calculateHorizontalStats(Image im, float* averageHorizontal, float* varianceHorizontal) {
    long long sum_x_pos = 0;
    float sum_x_sq = 0.0f;
    int darkPixelCount = 0;

    // 1. 어두운 픽셀 (값 < 10)의 X 위치 합계 및 개수 계산
    for (int y = 0; y < im->rows; y++) {
        for (int x = 0; x < im->cols; x++) {
            // PGM/PPM 포맷은 흑백/RGB 순차 저장. GREY 포맷으로 가정하고 첫 번째 채널만 사용.
            if (im->content[y * im->cols + x] < 10) {
                sum_x_pos += x;
                darkPixelCount++;
            }
        }
    }

    // 예외 처리: 어두운 픽셀이 없는 경우
    if (darkPixelCount == 0) {
        *averageHorizontal = 0.0f;
        *varianceHorizontal = 0.0f;
        return;
    }

    // 2. 평균 계산
    *averageHorizontal = (float)sum_x_pos / darkPixelCount;

    // 3. 분산 계산
    for (int y = 0; y < im->rows; y++) {
        for (int x = 0; x < im->cols; x++) {
            if (im->content[y * im->cols + x] < 10) {
                float diff = (float)x - *averageHorizontal;
                sum_x_sq += diff * diff;
            }
        }
    }
    *varianceHorizontal = sum_x_sq / darkPixelCount;
}

// 세로(Y축) 위치 평균 및 분산 계산
void calculateVerticalStats(Image im, float* averageVertical, float* varianceVertical) {
    long long sum_y_pos = 0;
    float sum_y_sq = 0.0f;
    int darkPixelCount = 0;

    // 1. 어두운 픽셀 (값 < 10)의 Y 위치 합계 및 개수 계산
    for (int y = 0; y < im->rows; y++) {
        for (int x = 0; x < im->cols; x++) {
            if (im->content[y * im->cols + x] < 10) {
                sum_y_pos += y;
                darkPixelCount++;
            }
        }
    }

    // 예외 처리: 어두운 픽셀이 없는 경우
    if (darkPixelCount == 0) {
        *averageVertical = 0.0f;
        *varianceVertical = 0.0f;
        return;
    }

    // 2. 평균 계산
    *averageVertical = (float)sum_y_pos / darkPixelCount;

    // 3. 분산 계산
    for (int y = 0; y < im->rows; y++) {
        for (int x = 0; x < im->cols; x++) {
            if (im->content[y * im->cols + x] < 10) {
                float diff = (float)y - *averageVertical;
                sum_y_sq += diff * diff;
            }
        }
    }
    *varianceVertical = sum_y_sq / darkPixelCount;
}


int main(void) {
    // 윈도우 환경에서 한글 출력을 위한 설정 (없으면 콘솔에서 한글 깨짐)
    // SetConsoleCP(CP_UTF8);
    // SetConsoleOutputCP(CP_UTF8);
    // 주석 처리: Canvas 환경에서 불필요하거나 오류를 유발할 수 있음.

    Image img = NULL;

    // 30개 (10개 숫자 * 3개 폰트)의 통계 저장 배열
    float averageHorizontal[10][3];
    float varianceHorizontal[10][3];
    float averageVertical[10][3];
    float varianceVertical[10][3];

    // 1. 모든 이미지의 특징 (4가지 통계 데이터) 계산 후 저장
    for (int i = 0; i < 10; i++) { // 숫자 (0 ~ 9)
        for (int j = 0; j < 3; j++) { // 폰트 (1 ~ 3)
            char imgPath[20];
            // 파일 경로 생성 예: "./pgm/no5-3.pgm"
            sprintf(imgPath, "./pgm/no%d-%d.pgm", i, j + 1);

            img = readPBMImage(imgPath);

            // 이미지 읽기에 실패했거나 유효하지 않으면 0으로 설정
            if (img == NULL || img->format == EMPTY) {
                fprintf(stderr, "Warning: Failed to read or process image %s. Setting stats to 0.\n", imgPath);
                averageHorizontal[i][j] = 0.0f;
                varianceHorizontal[i][j] = 0.0f;
                averageVertical[i][j] = 0.0f;
                varianceVertical[i][j] = 0.0f;
                // 메모리 정리
                if (img) { if (img->content) free(img->content); free(img); }
                continue;
            }

            calculateHorizontalStats(img, &averageHorizontal[i][j], &varianceHorizontal[i][j]);
            calculateVerticalStats(img, &averageVertical[i][j], &varianceVertical[i][j]);

            // 메모리 정리
            if (img->content) free(img->content);
            free(img);
        }
    }

    // 2. 모든 이미지에 대해 고유성 판별 후 출력
    for (int i = 0; i < 10; i++) { // 기준 숫자 (0 ~ 9)
        for (int j = 0; j < 3; j++) { // 기준 폰트 (1 ~ 3)
            float minDifference = 999999.0f; // 가장 가까운 이미지와의 최소 차이
            int closestNum = -1, closestFont = -1;
            // secondMinDifference 관련 변수/로직은 공주마마의 명에 따라 제거됨.

            // 자기 자신을 제외한 모든 이미지와 비교 (총 29회 비교)
            for (int k = 0; k < 10; k++) {
                for (int l = 0; l < 3; l++) {
                    // 동일한 이미지일 경우 건너뛰기
                    if (i == k && j == l) continue;

                    // 4가지 특징의 절대값 차이를 합산하여 하나의 차이(difference) 도출 (공주마마의 로직)
                    float difference = fabs(averageHorizontal[i][j] - averageHorizontal[k][l]) +
                        fabs(varianceHorizontal[i][j] - varianceHorizontal[k][l]) +
                        fabs(averageVertical[i][j] - averageVertical[k][l]) +
                        fabs(varianceVertical[i][j] - varianceVertical[k][l]);

                    // 가장 작은 차이(minDifference) 기록 및 갱신
                    if (difference < minDifference) {
                        minDifference = difference;
                        closestNum = k;
                        closestFont = l;
                    }
                }
            }

            char imgPath[20];
            sprintf(imgPath, "no%d-%d.pgm", i, j + 1);

            // 최종 출력 형식에 맞추어 판정 및 출력
            float finalresult = 0.002f; // 임계값 (Threshold)

            // minDifference가 임계값보다 크거나 같으면 (가장 가까운 대상까지도 충분히 멀리 떨어져 있음 = 고유성 확보)
            if (minDifference >= finalresult) {
                // 판정 성공으로 처리하고, 원래 정답(i)을 판정값에 출력.
                printf("- %s : %d [성공] / 가장 유사한 이미지 : no%d-%d.pgm (차이: %.4f)\n",
                    imgPath, i, closestNum, closestFont + 1, minDifference);
            }
            // minDifference가 임계값보다 작으면 (너무 가까운 유사체가 존재함 = 고유성 부족)
            else {
                // 판정 불가 처리.
                printf("- %s : 판정 불가 / 가장 유사한 이미지 : no%d-%d.pgm (차이: %.4f)\n",
                    imgPath, closestNum, closestFont + 1, minDifference);
            }
        }
    }

    return 0;
}
