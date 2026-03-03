import tkinter as tk
from tkinter import messagebox
import os
# 이미지 처리를 돕는 Pillow(PIL) 라이브러리를 가져옵니다.
from PIL import Image, ImageTk 

# KioskApp 클래스는 주스 키오스크 GUI를 생성하고 이벤트를 처리합니다.
class KioskApp:
    # 생성자 (Constructor): 클래스 객체가 생성될 때 초기 설정을 합니다.
    def __init__(self, master):
        # Master는 Tkinter 윈도우 객체입니다.
        self.master = master
        # 윈도우 제목을 설정합니다.
        master.title("주스 키오스크, 2501110202, 김해민")
        # 깔끔한 레이아웃 유지를 위해 윈도우 크기 변경 비활성화
        master.resizable(False, False)

        # 윈도우의 전체 배경색을 설정합니다. 
        master.configure(bg='#FFF8E1')

        # 현재 실행 중인 파이썬 파일의 경로를 알아냅니다.
        current_dir = os.path.dirname(__file__)
        # 현재 위치의 상위 폴더(..)에 있는 assets 폴더 경로를 설정합니다.
        # 이렇게 하면 어느 컴퓨터에서 실행하든 이미지를 찾을 수 있습니다.
        self.assets_dir = os.path.join(current_dir, '..', 'assets')

        # 초기 선택값 설정
        self.selected_fruit = "" 
        self.selected_size = "기본 컵" 
        
        # 8가지 메뉴의 가격 정보를 담은 딕셔너리입니다.
        self.fruit_prices = {
            "트리플 시트러스": 5500, "클래식 그린 디톡스": 6300, 
            "루비 자몽 허니": 5000, "순수 망고 스무디": 6500, 
            "프리미엄 딸기": 5800, "민트 레모네이드": 4500,
            "베리 퍼플": 6200, "바나나 프로틴": 6000
        }

        # 컵 사이즈별 추가 요금을 담은 딕셔너리입니다.
        self.size_fees = {
            "기본 컵": 0, "중간 컵": 1000, "대": 2000
        }
        
        # 이미지 객체 참조 유지를 위한 리스트입니다.
        self.fruit_images = []
        self.size_images = []

        # GUI 구성 및 가격 계산 메서드를 호출합니다.
        self.setup_gui()
        self.calculate_total_price()

    # GUI의 모든 Widget을 설정하고 배치하는 메서드입니다.
    def setup_gui(self):
        
        # === 1. 과일 선택 섹션 ===
        # Label 위젯으로 안내 문구를 표시합니다. 배경색을 윈도우와 통일합니다.
        tk.Label(self.master, text="주스를 선택해주세요", 
                 font=('맑은 고딕', 20, 'bold'), bg='#FFF8E1', fg='#FF6F00').pack(pady=20)
        
        # 과일 버튼들을 배치할 Frame를 생성합니다.
        self.fruit_frame = tk.Frame(self.master, bg='#FFF8E1')
        self.fruit_frame.pack(padx=10, pady=5)
        
        # 메뉴 이름과 이미지 파일명을 리스트에 정의합니다.
        fruit_info = [
            ("트리플 시트러스", "citrus_mix.jpg"),
            ("클래식 그린 디톡스", "green_detox.jpg"),
            ("루비 자몽 허니", "grapefruit_honey.jpg"),
            ("순수 망고 스무디", "mango_smoothie.jpg"),
            ("프리미엄 딸기", "strawberry_premium.jpg"),
            ("민트 레모네이드", "lemon_mint.jpg"),
            ("베리 퍼플", "berry_purple.jpg"),
            ("바나나 프로틴", "banana_protein.jpg")
        ]

        # 반복문을 통해 과일 버튼들을 생성하고 배치합니다.
        for idx, (name, filename) in enumerate(fruit_info):
            # 2행 4열 그리드 레이아웃을 위해 행과 열 인덱스를 계산합니다.
            row_idx = idx // 4 
            col_idx = idx % 4      
            
            # 이미지 파일의 전체 경로를 생성합니다.
            full_path = os.path.join(self.assets_dir, filename)

            if os.path.exists(full_path):
                try:
                    # Pillow 라이브러리로 이미지를 열고 크기를 조정합니다.
                    image = Image.open(full_path)
                    image = image.resize((110, 130))
                    # Tkinter에서 사용할 수 있는 이미지 객체로 변환합니다.
                    img = ImageTk.PhotoImage(image)
                    self.fruit_images.append(img)
                    
                    # 버튼에 표시할 텍스트를 생성합니다. (이름과 가격)
                    display_text = f"{name}\n{self.fruit_prices[name]:,}원"
                    
                    # 이미지와 텍스트가 포함된 버튼을 생성합니다.
                    button = tk.Button(self.fruit_frame, image=img, text=display_text, compound='top', 
                                       font=('맑은 고딕', 10, 'bold'), bg='white', relief='groove', bd=2,
                                       activebackground='#FFE0B2', width=130,
                                       command=lambda fruit=name: self.fruit_select(fruit))
                    
                    # 버튼을 그리드에 배치합니다.
                    button.grid(row=row_idx, column=col_idx, padx=10, pady=10, ipadx=5, ipady=5)

                except Exception:
                    # 이미지 로드 실패 시 대체 텍스트 버튼을 생성합니다.
                    self._create_text_button(name, row_idx, col_idx, is_fruit=True)
            else:
                # 파일이 없을 경우 대체 텍스트 버튼을 생성합니다.
                self._create_text_button(name, row_idx, col_idx, is_fruit=True)
        
        # === 2. 컵 사이즈 선택 섹션 ===
        tk.Label(self.master, text="사이즈를 골라주세요", 
                 font=('맑은 고딕', 16, 'bold'), bg='#FFF8E1', fg='#5D4037').pack(pady=15)
        
        self.size_frame = tk.Frame(self.master, bg='#FFF8E1')
        self.size_frame.pack(padx=10, pady=5)

        size_info = [
            ("기본 컵", "small.jpg"),
            ("중간 컵", "medium.jpg"),
            ("대", "large.jpg")
        ]
        
        for idx, (name, filename) in enumerate(size_info):
            full_path = os.path.join(self.assets_dir, filename)
            
            if os.path.exists(full_path):
                try:
                    image = Image.open(full_path)
                    image = image.resize((80, 100))
                    img = ImageTk.PhotoImage(image)
                    self.size_images.append(img)
                    
                    # 추가 요금이 있는 경우 텍스트에 포함시킵니다.
                    if self.size_fees[name] > 0:
                         display_text = f"{name}\n(+{self.size_fees[name]:,}원)"
                    else:
                         display_text = name

                    button = tk.Button(self.size_frame, image=img, text=display_text, compound='top', 
                                       font=('맑은 고딕', 10), bg='white', relief='groove', bd=2,
                                       activebackground='#FFE0B2', width=100, 
                                       command=lambda size=name: self.size_select(size))
                    button.grid(row=0, column=idx, padx=10, pady=5, ipadx=5, ipady=5)

                except Exception:
                    self._create_text_button(name, 0, idx, is_fruit=False)
            else:
                self._create_text_button(name, 0, idx, is_fruit=False)

        # === 3. 결과 표시 섹션 ===
        # 하단에 결과를 보여줄 프레임을 생성합니다. 
        self.result_frame = tk.Frame(self.master, bg='#FFCC80', bd=2, relief='sunken')
        self.result_frame.pack(fill='x', side='bottom', pady=0)

        # 결과 텍스트를 동적으로 변경하기 위해 StringVar를 사용합니다.
        self.result_text = tk.StringVar()
        self.total_price_label = tk.Label(self.result_frame, textvariable=self.result_text, 
                                          font=('맑은 고딕', 18, 'bold'), bg='#FFCC80', fg='#E65100')
        self.total_price_label.pack(pady=20)

    # 이미지 로드 실패 시 대체 텍스트 버튼을 생성하는 내부 메서드입니다.
    def _create_text_button(self, name, row_idx, col_idx, is_fruit):
        if is_fruit:
            text_content = f"{name}\n{self.fruit_prices[name]:,}원"
            frame = self.fruit_frame
            cmd = lambda fruit=name: self.fruit_select(fruit)
        else:
            text_content = name
            frame = self.size_frame
            cmd = lambda size=name: self.size_select(size)
            
        tk.Button(frame, text=text_content, font=('맑은 고딕', 10, 'bold'), 
                  bg='white', relief='groove', bd=2, width=15, height=5,
                  command=cmd).grid(row=row_idx, column=col_idx, padx=10, pady=10)

    # 과일 버튼 클릭 시 호출되는 이벤트 핸들러입니다.
    def fruit_select(self, fruit_name):
        self.selected_fruit = fruit_name
        # 가격을 다시 계산하여 화면을 업데이트합니다.
        self.calculate_total_price()

    # 사이즈 버튼 클릭 시 호출되는 이벤트 핸들러입니다.
    def size_select(self, size_name):
        self.selected_size = size_name
        self.calculate_total_price()

    # 총 금액을 계산하고 결과 화면을 업데이트하는 메서드입니다.
    def calculate_total_price(self):
        try:
            # 딕셔너리에서 가격 정보를 가져옵니다. 
            fruit_base_price = self.fruit_prices.get(self.selected_fruit, 0)
            size_extra_fee = self.size_fees.get(self.selected_size, 0)
            
            # 총 합계를 계산합니다.
            total_amount = fruit_base_price + size_extra_fee

            # 화면에 표시할 문자열을 포맷팅합니다. 
            display_text = (
                f"주문 내역: {self.selected_fruit} ({self.selected_size})\n"
                f"결제 금액: {total_amount:,}원"
            )
            self.result_text.set(display_text)

        except Exception as e:
            # 오류 발생 시 메시지 박스를 띄웁니다.
            self.result_text.set("오류 발생")
            messagebox.showerror("오류", str(e))

# 메인 함수: 프로그램의 진입점입니다.
if __name__ == '__main__':
    root = tk.Tk()
    app = KioskApp(root)
    root.mainloop()