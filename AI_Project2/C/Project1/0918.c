#define _CRT_SECURE_NO_WARNINGS

#define MIN(x,y) x < y ? x: y
#define MAX(x,y) x > y ? x: y

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Windows.h>



HWND hwnd;   // handle window (윈도우 다루기)
HDC hdc;

// pbm 파일 읽어와서 복사하는 프로그램

enum FORMAT { EMPTY, GREY, RGB, YCBCR, YCBCR420, BLOCK };

typedef struct {      // 총 21 byte
    unsigned int rows;
    unsigned int cols;
    char format;
    unsigned long total;   // Bytes per image
    unsigned int levels;   // Number of gray/each color levels
    short* content;
} ImageType;
typedef ImageType* Image;

// 숫자 이미지를 표시하는 함수
void DrawImage(Image im) {
    hwnd = GetForegroundWindow();
    hdc = GetWindowDC(hwnd);
    for (int i = 0; i < im->rows; ++i) {
        for (int j = 0; j < im->cols; j++) {
            SetPixel(hdc, 250 + i, 250 + j, RGB(
                im->content[j * im->cols + i],
                im->content[j * im->cols + i],
                im->content[j * im->cols + i]
            ));
        }
    }
}

// 히스토그램을 표시하는 함수
void DrawHistogram(Image im) {
    // 가로/세로를 담을 배열 생성 후 초기화
    short* horizontal = (short*)malloc(sizeof(short) * im->cols);
    short* vertical = (short*)malloc(sizeof(short) * im->rows);

    for (int i = 0; i < im->cols; i++) horizontal[i] = 0;
    for (int i = 0; i < im->rows; i++) vertical[i] = 0;

    // 이미지를 가로/세로로 순회하며 기준보다 어두운 색의 수를 기록
    for (int y = 0; y < im->rows; ++y)
        for (int x = 0; x < im->cols; x++) {
            if (im->content[y * im->cols + x] < 10) horizontal[x]++;
        }
    for (int x = 0; x < im->cols; ++x) {
        for (int y = 0; y < im->rows; y++) {
            if (im->content[y * im->cols + x] < 10) vertical[y]++;
        }
    }

    hwnd = GetForegroundWindow();
    hdc = GetWindowDC(hwnd);

    // 가로/세로로 나아가며 히스토그램을 기록
    for (int i = 0; i < im->cols; i++) {
        for (int j = 0; j < horizontal[i] * 5; j++)
            SetPixel(hdc, 250 + i, 250 - j, RGB(0, 255, 0));
    }
    for (int i = 0; i < im->rows; i++) {
        for (int j = 0; j < vertical[i] * 5; j++)
            SetPixel(hdc, 250 - j, 250 + i, RGB(0, 255, 0));
    }

    free(horizontal);
    free(vertical);
}

// 히스토그램 평활화를 적용하는 함수
void equalize(Image im) {
    int minVal[3] = { 255,255,255 };
    int maxVal[3] = { 0,0,0 };
    float normCoef[3];

    if (im->format == GREY) {
        for (int i = 0; i < im->total; i++) {
            minVal[0] = MIN(im->content[i], minVal[0]);
            maxVal[0] = MAX(im->content[i], maxVal[0]);
        }
    }
    else if (im->format == RGB) {
        for (int i = 0; i < im->total; i += 3) {
            minVal[0] = MIN(im->content[i], minVal[0]);
            maxVal[0] = MAX(im->content[i], maxVal[0]);
            minVal[1] = MIN(im->content[i + 1], minVal[1]);
            maxVal[1] = MAX(im->content[i + 1], maxVal[1]);
            minVal[2] = MIN(im->content[i + 2], minVal[2]);
            maxVal[2] = MAX(im->content[i + 2], maxVal[2]);
        }
    }

    if (im->format == GREY) {
        normCoef[0] = (float)im->levels / (maxVal[0] - minVal[0]);
        for (int i = 0; i < im->total; i++)
            im->content[i] = (im->content[i] - minVal[0]) * normCoef[0];
    }
    else if (im->format == RGB) {
        normCoef[0] = (float)im->levels / (maxVal[0] - minVal[0]);
        normCoef[1] = (float)im->levels / (maxVal[1] - minVal[1]);
        normCoef[2] = (float)im->levels / (maxVal[2] - minVal[2]);
        for (int i = 0; i < im->total; i += 3) {
            im->content[i] = (im->content[i] - minVal[0]) * normCoef[0];
            im->content[i + 1] = (im->content[i + 1] - minVal[1]) * normCoef[1];
            im->content[i + 2] = (im->content[i + 2] - minVal[2]) * normCoef[2];
        }
    }
}

Image imageAllocate(unsigned int rows, unsigned int cols, char format, unsigned int levels) {
    Image im = (Image)malloc(sizeof(ImageType));
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
        break;
    }

    im->content = (short*)malloc(im->total * sizeof(short));
    return im;
}

Image readPBMImage(const char* filename) {
    FILE* pgmFile;
    int k;

    char signature[3];
    unsigned int cols, rows, levels;

    Image im = imageAllocate(0, 0, EMPTY, 0);

    pgmFile = fopen(filename, "rb");
    if (pgmFile == NULL) {
        perror("Cannot open file to read!");
        fclose(pgmFile);
        return imageAllocate(0, 0, EMPTY, 0);
    }

    fgets(signature, sizeof(signature), pgmFile);
    if (strcmp(signature, "P5") != 0 && strcmp(signature, "P6") != 0) {
        perror("Wrong file type!");
        fclose(pgmFile);
        return im;
    }

    // read header
    fscanf(pgmFile, "%d %d %d", &cols, &rows, &levels);
    fgetc(pgmFile);

    if (strcmp(signature, "P5") == 0) {
        im = imageAllocate(rows, cols, GREY, levels);
        for (k = 0; k < im->total; ++k) {
            im->content[k] = (unsigned char)fgetc(pgmFile);
        }
    }
    else if (strcmp(signature, "P6") == 0) {
        im = imageAllocate(rows, cols, RGB, levels);
        unsigned long gOffset = im->cols * im->rows;
        unsigned long bOffset = 2 * im->cols * im->rows;
        for (k = 0; k < im->total / 3; ++k) {
            im->content[k] = (unsigned char)fgetc(pgmFile);
            im->content[k + gOffset] = (unsigned char)fgetc(pgmFile);
            im->content[k + bOffset] = (unsigned char)fgetc(pgmFile);
        }
    }

    fclose(pgmFile);
    return im;
}

void writePBMImage(const char* filename, const Image im) {
    FILE* pgmFile;
    int k;

    pgmFile = fopen(filename, "wb");
    if (pgmFile == NULL) {
        perror("Cannot open file to write");
        exit(EXIT_FAILURE);
    }

    if (im->format == GREY) fprintf(pgmFile, "%s ", "P5");
    else if (im->format == RGB) fprintf(pgmFile, "%s", "P6");

    fprintf(pgmFile, "%d %d ", im->cols, im->rows);
    fprintf(pgmFile, "%d ", im->levels);

    if (im->format == GREY) {
        for (k = 0; k < im->total; ++k) {
            fputc((unsigned char)im->content[k], pgmFile);
        }
    }
    else if (im->format == RGB) {
        unsigned long gOffset = im->cols * im->rows;
        unsigned long bOffset = 2 * im->cols * im->rows;
        for (k = 0; k < im->total / 3; ++k) {
            fputc((unsigned char)im->content[k], pgmFile);
            fputc((unsigned char)im->content[k + gOffset], pgmFile);
            fputc((unsigned char)im->content[k + bOffset], pgmFile);
        }
    }

    fclose(pgmFile);
}

int main(void) {
    Image img = 0;

    while (1) {
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 3; j++) {
                system("cls");
                char imgPath[] = "./pgm/no0-1.pgm";
                imgPath[8] = '0' + i;
                imgPath[10] = '1' + j;
                img = readPBMImage(imgPath);
                DrawImage(img);
                DrawHistogram(img);
                Sleep(1000);
            }
        }
    }
    return 0;
}