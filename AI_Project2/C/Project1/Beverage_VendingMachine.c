#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 음료 정보를 담는 구조체
typedef struct {
    char name[32];
    int price;
    int stock;
    int sold;
} Drink;

// 전역 변수: 음료 목록 및 개수
Drink* drinks = NULL;
int drinkCount = 0;
const char* FILENAME = "Bevarage_VendingMachine.txt";

// 함수 선언
void saveData();
void loadData();
void addDrink(const char* name, int price, int stock, int sold);
int user_input();
void listDrinksForUser();
void listDrinks();

// 데이터를 파일에 저장하는 함수
void saveData() {
    FILE* file = fopen(FILENAME, "w");
    if (file == NULL) {
        printf("오류: 데이터를 파일에 저장할 수 없습니다.\n");
        return;
    }

    for (int i = 0; i < drinkCount; i++) {
        fprintf(file, "%d %d %d %s\n", drinks[i].price, drinks[i].stock, drinks[i].sold, drinks[i].name);
    }
    fclose(file);
}

// 파일로부터 데이터를 불러오는 함수 
void loadData() {
    FILE* file = fopen(FILENAME, "r");
    if (file == NULL) {
        // 파일이 없으면 기본 음료 설정
        addDrink("콜라", 1000, 5, 0);
        addDrink("사이다", 1000, 5, 0);
        addDrink("포카리 스웨트", 2000, 5, 0);
        addDrink("오렌지 주스", 2000, 5, 0);
        addDrink("포도 주스", 2000, 5, 0);
        addDrink("생수", 800, 5, 0);
        saveData();
        return;
    }

    char line[128];
    while (fgets(line, sizeof(line), file) != NULL) {
        int price, stock, sold;
        char name[32] = { 0 };


        if (sscanf(line, " %d %d %d %[^\n]", &price, &stock, &sold, name ) == 4) {
            addDrink(name, price, stock, sold);
        }
    }
    fclose(file);
}

// 음료 추가 함수
void addDrink(const char* name, int price, int stock, int sold) {
    drinks = realloc(drinks, (drinkCount + 1) * sizeof(Drink));
    if (drinks == NULL) {
        printf("메모리 할당 오류!\n");
        exit(1);
    }
    strcpy(drinks[drinkCount].name, name);
    drinks[drinkCount].price = price;
    drinks[drinkCount].stock = stock;
    drinks[drinkCount].sold = sold;
    drinkCount++;
}

// 음료 삭제 함수
void removeDrink(int index) {
    if (index < 0 || index >= drinkCount) return;
    for (int i = index; i < drinkCount - 1; i++) {
        drinks[i] = drinks[i + 1];
    }
    drinkCount--;
    drinks = realloc(drinks, drinkCount * sizeof(Drink));
    if (drinkCount > 0 && drinks == NULL) {
        printf("메모리 재할당 오류!\n");
        exit(1);
    }
}

// (관리자용) 모든 음료 정보를 출력
void listDrinks() {
    printf("\n--- 음료 목록 (관리자) ---\n");
    for (int i = 0; i < drinkCount; i++) {
        printf("%d)  \x1b[32m%s\x1b[0m | %d원 | 재고:%d | 판매:%d\n",
            i + 1, drinks[i].name, drinks[i].price, drinks[i].stock, drinks[i].sold);
    }
    if (drinkCount == 0) printf("(등록된 음료가 없습니다.)\n");
}

// (사용자용) 재고와 판매량을 제외한 음료 목록 출력
void listDrinksForUser() {
    printf("\n--- 메뉴 선택 ---\n");
    for (int i = 0; i < drinkCount; i++) {
        printf("%d) \x1b[32m%s\x1b[0m | %d원", i + 1, drinks[i].name, drinks[i].price);
        if (drinks[i].stock == 0) {
            printf(" (품절)");
        }
        printf("\n");
    }
    if (drinkCount == 0) printf("(판매중인 음료가 없습니다.)\n");
}

// 사용자 입력 오류 예외처리
int user_input() {
    int value;
    char buffer[100];

    while (1) {

        if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
            if (sscanf(buffer, "%d", &value) == 1) {
                return value;
            }
        }
        printf("잘못된 입력입니다. 숫자를 입력해주세요: ");
    }
}

// 문자열을 입력받는 함수 
void get_string_input(char* buffer, int size) {
    if (fgets(buffer, size, stdin) != NULL) {

        buffer[strcspn(buffer, "\n")] = 0;
    }
}


int main(void) {
    int state = 0;
    int money = 0;

    loadData();

    while (1) {
        switch (state) {

        case 0: // 모드 선택
        {
            printf("\x1b[33m\n=== 음료 자판기 === (잔액:%d)\n\x1b[0m", money);
            printf("\x1b[31m1. 관리자 모드\n\x1b[0m");
            printf("\x1b[34m2. 판매 시작\n\x1b[0m");
            printf("선택: ");
            int choice = user_input();

            if (choice == 1) state = 1;
            else if (choice == 2) state = 2;
            else printf("잘못된 입력입니다.\n");
            break;
        }

        case 1: // 관리자 모드
        {
            printf("\x1b[31m\n--- 관리자 모드 ---\n\x1b[0m");
            printf("0. 모드 선택으로 돌아가기\n");
            printf("1. 판매 현황 보기\n");
            printf("2. 음료 추가\n");
            printf("3. 음료 삭제\n");
            printf("4. 음료 수정\n");
            printf("선택: ");
            int choice = user_input();

            if (choice == 1) {
                int total = 0;
                printf("\n[판매 현황]\n");
                listDrinks();
                for (int i = 0; i < drinkCount; i++) {
                    total += drinks[i].sold * drinks[i].price;
                }
                printf("총 매출: %d원\n", total);
            }
            else if (choice == 2) { // 음료 추가
                char name[32]; int price, stock;
                printf("추가할 음료 이름: ");
                get_string_input(name, sizeof(name));

                printf("가격: "); price = user_input();
                printf("재고: "); stock = user_input();
                addDrink(name, price, stock, 0);
                saveData();
                printf("추가 완료!\n");
            }
            else if (choice == 3) { // 음료 삭제
                if (drinkCount == 0) { printf("삭제할 음료가 없습니다.\n"); break; }
                listDrinks();
                printf("삭제할 번호: ");
                int idx = user_input();
                if (idx < 1 || idx > drinkCount) { printf("잘못된 번호입니다.\n"); break; }
                removeDrink(idx - 1);
                saveData();
                printf("삭제 완료!\n");
            }
            else if (choice == 4) { // 음료 수정
                if (drinkCount == 0) { printf("수정할 음료가 없습니다.\n"); break; }
                listDrinks();
                printf("수정할 번호: ");
                int idx = user_input();
                if (idx < 1 || idx > drinkCount) { printf("잘못된 번호입니다.\n"); break; }
                idx--;

                printf("새 이름: ");
                get_string_input(drinks[idx].name, sizeof(drinks[idx].name));

                printf("새 가격: "); drinks[idx].price = user_input();
                printf("새 재고: "); drinks[idx].stock = user_input();
                saveData();
                printf("수정 완료!\n");
            }
            else if (choice == 0) state = 0;
            break;
        }

        case 2: // 판매 시작 (돈 투입)
        {
            printf("\x1b[34m\n--- 판매 시작 ---\n\x1b[0m");
            printf("\n동전을 넣어주세요(원). 0 입력 시 메뉴 선택: ");
            int coin = user_input();
            if (coin < 0) { printf("잘못된 입력입니다. \n"); break; }
            money += coin;
            if (coin == 0 && money == 0) state = 0; // 돈이 없을 때 0원 넣으면 메뉴로
            else state = 4;
            break;
        }

        case 4: // 메뉴 고르기
        {
            listDrinksForUser(); // 사용자용 메뉴 호출
            printf("잔액:%d | 구매 번호(1~%d), 9=추가투입, 0=거스름돈 반환: ", money, drinkCount);
            int choice = user_input();

            if (choice == 0) { state = 6; break; }
            if (choice == 9) { state = 2; break; }
            if (choice < 1 || choice > drinkCount) { printf("잘못된 선택입니다.\n"); break; }

            int i = choice - 1;
            if (drinks[i].stock <= 0) { printf("재고가 없어 구매할 수 없습니다.\n"); break; }
            if (money < drinks[i].price) { printf("잔액이 부족합니다.\n"); break; }

            money -= drinks[i].price;
            drinks[i].stock--;
            drinks[i].sold++;
            saveData();
            printf("[%s]가 나왔습니다! 남은 잔액:%d원\n", drinks[i].name, money);
            state = 5;
            break;
        }

        case 5: // 구매 후 선택
        {
            if (money > 0) {
                printf("계속 구매하시겠습니까? (1=예, 0=거스름돈 반환): ");
                int choice = user_input();
                state = (choice == 1) ? 4 : 6;
            }
            else {
                printf("잔액이 모두 소진되었습니다.\n");
                state = 0;
            }
            break;
        }

        case 6: // 거스름돈 반환
        {
            if (money > 0) {
                printf("거스름돈 %d원을 받으세요.\n", money);
                money = 0;
            }
            printf("이용해주셔서 감사합니다.\n");
            state = 0;
            break;
        }

        default:
            printf("알 수 없는 상태입니다. 초기화면으로 돌아갑니다.\n");
            state = 0;
            break;
        }
    }

    free(drinks);
    return 0;
}

