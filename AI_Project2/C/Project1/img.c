#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

enum FORMAT { EMPTY, GREY, RGB, YCBCR, YCBCR420, BLOCK };

typedef struct imageType {
    unsigned int rows;          //Image height
    unsigned int cols;          //Image width
    char format;            //Image format
    unsigned long total;    // Bytes per image;
    unsigned int levels;        //Number of gray/each color levels

    short* content;
} ImageType;

typedef ImageType* Image;

Image imageAllocate(unsigned int rows, unsigned int cols, char format, unsigned int levels) {
    Image im = malloc(sizeof(ImageType));
    im->rows = rows;
    im->cols = cols;
    im->format = format;
    im->levels = levels;
    im->content = NULL;
    if (im->format == EMPTY)
        return im;

    switch (im->format) {
    case GREY:
        im->total = im->cols * im->rows;
        break;
    case RGB:
        im->total = 3 * im->cols * im->rows;
        break;
    case YCBCR:
        im->total = 3 * im->cols * im->rows;
        break;
    case YCBCR420:
        im->total = 3 * im->cols * im->rows / 2;
        break;
    default:

        break;
    }

    im->content = malloc(im->total * sizeof(short));

    //    memoryManagment[memIndex++] = im;

    return im;
}
void imageRelease(Image im) {
    im->format = EMPTY;
    if (im->content != NULL)
        free(im->content);
    im->content = NULL;
    free(im);
}
//----------------------------------------------------------------------------------------------------------------------------
Image readPBMImage(const char* filename) {
    FILE* pgmFile;
    int k;

    char signature[3];
    unsigned cols, rows, levels;

    Image im = imageAllocate(0, 0, EMPTY, 0);

    pgmFile = fopen(filename, "rb");
    if (pgmFile == NULL) {
        perror("Cannot open file to read!");
        fclose(pgmFile);
        return imageAllocate(0, 0, EMPTY, 0);
    }

    fgets(signature, sizeof(signature), pgmFile);
    if (strcmp(signature, "P5") != 0 && strcmp(signature, "P6") != 0 && strcmp(signature, "P4") != 0) {
        perror("Wrong file type!");
        fclose(pgmFile);
        return im;
    }
    //read header
    fscanf(pgmFile, "%d %d %d", &cols, &rows, &levels);
    fgetc(pgmFile);


    if (strcmp(signature, "P5") == 0 || strcmp(signature, "P4") == 0) {
        im = imageAllocate(rows, cols, GREY, levels);
        unsigned int interval = im->rows / 5;
        for (k = 0; k < im->total; ++k) {
            im->content[k] = (unsigned char)fgetc(pgmFile);            
        }
    }
    else if (strcmp(signature, "P6") == 0) {
        im = imageAllocate(rows, cols, RGB, levels);
        unsigned long gOffset = im->cols * im->rows;
        unsigned long bOffset = 2 * im->cols * im->rows;
        for (k = 0; k < im->total / 3; ++k) {
            im->content[k] = (unsigned char)fgetc(pgmFile);//원래 char 였는데 char는 음수도 포함하기 때문에 값이 이상하게 나와서 unsigend로 수정
            im->content[k + gOffset] = (unsigned char)fgetc(pgmFile);
            im->content[k + bOffset] = (unsigned char)fgetc(pgmFile);
        }
    }

    fclose(pgmFile);
    return im;
}
//----------------------------------------------------------------------------------------------------------------------------
void histogramEqualization(Image im) {

    short* pixels = im->content;
    short maxVal = pixels[0];
    short minVal = pixels[0];

    for (unsigned long k = 1; k < im->total; ++k) {
        if (pixels[k] > maxVal) {
            maxVal = pixels[k];
        }
        if (pixels[k] < minVal) {
            minVal = pixels[k];
        }
    }

    double normCoef = (double)im->levels / (double)(maxVal - minVal);

    for (unsigned long k = 0; k < im->total; ++k) {
        pixels[k] = (short)((pixels[k] - minVal) * normCoef);
    }

    printf("히스토그램 평활화 성공");
}

//----------------------------------------------------------------------------------------------------------------------------
void writePBMImage(const char* filename, const Image im) {
    FILE* pgmFile;
    int k;

    pgmFile = fopen(filename, "wb");
    if (pgmFile == NULL) {
        perror("Cannot open file to write");
        exit(-1);
    }

    if (im->format == GREY)
        fprintf(pgmFile, "%s ", "P5 ");
    else if (im->format == RGB)
        fprintf(pgmFile, "%s ", "P6 ");
    else {
        perror("Unknown file format\n");
        fclose(pgmFile);
        return;
    }

    fprintf(pgmFile, "%d %d ", im->cols, im->rows);
    fprintf(pgmFile, "%d ", im->levels);

    if (im->format == GREY) {
        for (k = 0; k < im->total; ++k)
            fputc((char)im->content[k], pgmFile);
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
//----------------------------------------------------------------------------------------------------------------------------
int main(void)
{
    Image img = 0;
    char imgPath[] = "./frog.pbm";
    img = readPBMImage(imgPath);
    histogramEqualization(img);
    writePBMImage("frog_histigramEqualization.pbm", img);
  

    free(img);

    return 0;
}