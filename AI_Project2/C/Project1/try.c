#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

enum FORMAT { EMPTY, GREY, RGB };

typedef struct {
    unsigned int rows;
    unsigned int cols;
    char format;
    unsigned long total;
    unsigned int levels;
    short* content;
} ImageType;
typedef ImageType* Image;

// 이미지 메모리 할당
Image imageAllocate(unsigned int rows, unsigned int cols, char format, unsigned int levels) {
    Image im = (Image)malloc(sizeof(ImageType));
    if (!im) return NULL;
    im->rows = rows;
    im->cols = cols;
    im->format = format;
    im->levels = levels;
    im->content = NULL;
    if (format == EMPTY) return im;

    im->total = (format == GREY) ? cols * rows : 3 * cols * rows;
    if (im->total > 0) {
        im->content = (short*)malloc(im->total * sizeof(short));
        if (!im->content) { free(im); return NULL; }
    }
    return im;
}

// PGM 파일 읽기 (P5)
Image readPBMImage(const char* filename) {
    FILE* pgmFile = fopen(filename, "rb");
    if (!pgmFile) return NULL;

    char signature[3];
    fscanf(pgmFile, "%2s", signature);
    if (strcmp(signature, "P5") != 0) { fclose(pgmFile); return NULL; }

    int cols, rows, levels;
    fscanf(pgmFile, "%d %d %d", &cols, &rows, &levels);
    fgetc(pgmFile);

    Image im = imageAllocate(rows, cols, GREY, levels);
    if (!im) { fclose(pgmFile); return NULL; }

    for (unsigned long k = 0; k < im->total; ++k)
        im->content[k] = (unsigned char)fgetc(pgmFile);

    fclose(pgmFile);
    return im;
}

// 픽셀의 x위치 평균과 분산
void calculateHorizontalStats(Image im, float* average, float* variance) {
    long long sum_x = 0;
    float sum_sq = 0.0f;
    int count = 0;
    for (int y = 0; y < im->rows; y++)
        for (int x = 0; x < im->cols; x++)
            if (im->content[y * im->cols + x] < 10) {
                sum_x += x;
                count++;
            }
    *average = (count == 0) ? 0 : (float)sum_x / count;

    for (int y = 0; y < im->rows; y++)
        for (int x = 0; x < im->cols; x++)
            if (im->content[y * im->cols + x] < 10)
                sum_sq += ((float)x - *average) * ((float)x - *average);

    *variance = (count == 0) ? 0 : sum_sq / count;
}

// 픽셀의 y위치 평균과 분산
void calculateVerticalStats(Image im, float* average, float* variance) {
    long long sum_y = 0;
    float sum_sq = 0.0f;
    int count = 0;
    for (int y = 0; y < im->rows; y++)
        for (int x = 0; x < im->cols; x++)
            if (im->content[y * im->cols + x] < 10) {
                sum_y += y;
                count++;
            }
    *average = (count == 0) ? 0 : (float)sum_y / count;

    for (int y = 0; y < im->rows; y++)
        for (int x = 0; x < im->cols; x++)
            if (im->content[y * im->cols + x] < 10)
                sum_sq += ((float)y - *average) * ((float)y - *average);

    *variance = (count == 0) ? 0 : sum_sq / count;
}

int main(void) {
    Image img = NULL;
    float averageHorizontal[10][3], varianceHorizontal[10][3];
    float averageVertical[10][3], varianceVertical[10][3];

    // 1. 통계 값 추출
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 3; j++) {
            char imgPath[32];
            sprintf(imgPath, "./pgm/no%d-%d.pgm", i, j + 1);
            img = readPBMImage(imgPath);

            if (!img || !img->content) {
                averageHorizontal[i][j] = varianceHorizontal[i][j] = 0.0f;
                averageVertical[i][j] = varianceVertical[i][j] = 0.0f;
                if (img) { free(img); }
                continue;
            }

            calculateHorizontalStats(img, &averageHorizontal[i][j], &varianceHorizontal[i][j]);
            calculateVerticalStats(img, &averageVertical[i][j], &varianceVertical[i][j]);
            free(img->content); free(img);
        }
    }

    // 2. 최근접 이웃 분류
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 3; j++) {
            float minDifference = 999999.0f;
            int closestNum = -1, closestFont = -1;

            for (int k = 0; k < 10; k++) {
                for (int l = 0; l < 3; l++) {
                    if (i == k && j == l) continue;
                    float difference =
                        fabs(averageHorizontal[i][j] - averageHorizontal[k][l]) +
                        fabs(varianceHorizontal[i][j] - varianceHorizontal[k][l]) +
                        fabs(averageVertical[i][j] - averageVertical[k][l]) +
                        fabs(varianceVertical[i][j] - varianceVertical[k][l]);
                    if (difference < minDifference) {
                        minDifference = difference;
                        closestNum = k;
                        closestFont = l;
                    }
                }
            }
            char imgPath[32];
            sprintf(imgPath, "no%d-%d.pgm", i, j + 1);
            printf("- %s : 예측 = %d / 실제 = %d / 가장 가까운 이웃: no%d-%d.pgm (차이: %.4f)",
                imgPath, closestNum, i, closestNum, closestFont + 1, minDifference);
            if (closestNum == i)
                printf(" → 판정 성공\n");
            else
                printf(" → 판정 실패\n");
        }
    }
    return 0;
}
