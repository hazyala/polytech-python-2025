#include <stdio.h>
#define _CRT_SECURE_NO_WARNINGS

void main(){
	FILE * fp = fopen("data.txt", "wt");
	if (fp == NULL) {
		puts("파일 오픈 실패 !");
		return -1; //비정상적 종료를 의미하기 위해 -1 반환
	}

	fputc('A', fp);
	fputc('B', fp);
	fputc('C', fp);
	fclose(fp); //스트림의 종료
	return 0;
}

