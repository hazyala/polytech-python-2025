#include <stdio.h>

void Test(int a[])
{
	*(a+1) = 1;
}

int main(void) {
	
	int num[] = { 0, 129, 2, 3 };
	printf("%d\n", num[1]);
	Test(num);
	printf("%d\n", num[1]);

	int num1 = 0x00FFFF;
	num1 = 0x000FF00;
	char* pnum = &num1;
	
	printf("%d\n", num1);
	printf("%d", *pnum);
	*pnum = 0;
	printf("%d\n", num1);
	return 0;
}