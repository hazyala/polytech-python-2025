import tkinter as tk
from tkinter import messagebox

# CalculatorApp 클래스는 계산기 GUI를 생성하고 이벤트를 처리합니다.
class CalculatorApp:
    # 생성자 (Constructor): 클래스 객체가 생성될 때 초기 설정을 합니다.
    def __init__(self, master):
        # Master는 Tkinter 윈도우 객체입니다.
        self.master = master
        # 윈도우 제목을 설정합니다.
        master.title("KOPO 계산기, 2501110202, 김해민")
        # 윈도우 크기 변경을 비활성화하여 계산기 모양을 유지합니다.
        master.resizable(False, False)

        # 윈도우의 전체 배경색을 설정합니다.
        master.configure(bg='#FFF8E1')

        # 현재 입력된 수식 문자열을 저장하는 지역 변수입니다.
        self.current_expression = ""

        # 결과가 표시될 입력 위젯을 생성합니다. (결과 표시 영역)
        self.entry_result = tk.Entry(master, width=20, font=('Arial', 24, 'bold'), 
                                     bg='white', fg='#5D4037', bd=5, relief='flat', justify='right')
        
        # grid를 사용하여 윈도우 상단에 배치합니다.
        self.entry_result.grid(row=0, column=0, columnspan=4, padx=15, pady=20, ipady=10)
        
        # 초기 값은 "0"으로 설정합니다.
        self.entry_result.insert(0, "0")

        # 계산기 버튼 배열을 정의합니다. 
        self.button_list = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['C'] # 'C' 버튼은 별도 행으로 처리합니다.
        ]

        # 버튼을 생성하고 배치하는 메서드를 호출합니다.
        self.create_buttons()

    # 버튼을 생성하고 Grid 레이아웃에 배치하는 메서드입니다.
    def create_buttons(self):
        # 버튼 배열(button_list)을 순회하며 버튼을 생성하고 배치합니다.
        # r_idx는 행 인덱스, row는 해당 행의 버튼 텍스트 리스트입니다.
        for r_idx, row in enumerate(self.button_list):
            # c_idx는 열 인덱스, btn_text는 버튼에 표시될 문자열입니다.
            for c_idx, btn_text in enumerate(row):
                
                # 버튼의 종류에 따라 배경색을 다르게 설정합니다.
                if btn_text in ['=', '+', '-', '*', '/']:
                    bg_color = '#FFCC80' 
                    active_bg = '#FFA726' 
                elif btn_text == 'C':
                    bg_color = '#FFAB91' 
                    active_bg = '#FF7043' 
                else:
                    bg_color = 'white'   
                    active_bg = '#FFE0B2'

                # tk.Button 위젯을 생성합니다.
                button = tk.Button(self.master, text=btn_text, font=('Arial', 18, 'bold'), 
                                   bg=bg_color, fg='#5D4037', relief='groove', bd=2,
                                   activebackground=active_bg,
                                   command=lambda text=btn_text: self.button_click(text))

                # 'C' (Clear) 버튼은 전체 열을 차지하도록 별도로 배치합니다.
                if btn_text == 'C':
                    # columnspan=4를 사용하여 4개 열을 병합합니다.
                    button.grid(row=r_idx + 1, column=0, columnspan=4, sticky='nsew', 
                                padx=10, pady=10, ipadx=10, ipady=10)
                else:
                    # 일반 버튼은 4x4 그리드에 배치합니다.
                    button.grid(row=r_idx + 1, column=c_idx, sticky='nsew', 
                                padx=5, pady=5, ipadx=10, ipady=15)
                    
                    # 4x4 버튼 그리드의 크기를 윈도우 크기에 따라 균일하게 조정합니다.
                    self.master.grid_columnconfigure(c_idx, weight=1)

    # 버튼 클릭 이벤트를 처리하는 메서드입니다.
    def button_click(self, text):
        # 'C' (Clear) 버튼이 눌렸을 경우
        if text == 'C':
            # 현재 입력된 수식 문자열을 초기화합니다.
            self.current_expression = ""
            # 화면에 "0"을 표시합니다.
            self.update_display("0")
        
        # '=' (Equal) 버튼이 눌렸을 경우
        elif text == '=':
            try:
                # eval() 함수를 사용하여 현재 표현식(문자열)을 계산합니다.
                # 계산 결과를 문자열로 변환합니다.
                result = str(eval(self.current_expression))
                # 계산 결과를 화면에 표시합니다.
                self.update_display(result)
                # 현재 표현식을 계산 결과로 업데이트하여 연속 계산이 가능하도록 합니다.
                self.current_expression = result
            except (ZeroDivisionError, SyntaxError):
                # 0으로 나누는 오류 또는 잘못된 수식 입력 오류 발생 시 처리합니다.
                messagebox.showerror("오류 발생", "잘못된 수식이거나 0으로 나눌 수 없습니다.")
                # 오류 발생 시 초기화합니다.
                self.current_expression = ""
                self.update_display("0")
        
        # 기타 버튼 (숫자 또는 연산자)이 눌렸을 경우
        else:
            # 현재 표현식 문자열에 버튼 텍스트를 추가합니다.
            self.current_expression += text
            # 화면에 현재 표현식을 표시합니다.
            self.update_display(self.current_expression)

    # Entry 위젯의 내용을 업데이트하는 메서드입니다.
    # value는 Entry에 새로 표시할 값(문자열)입니다.
    def update_display(self, value):
        # 기존 Entry 위젯의 내용을 모두 삭제합니다.
        self.entry_result.delete(0, tk.END)
        # 새로운 값을 삽입합니다.
        self.entry_result.insert(0, value)


# 메인 함수: 프로그램의 진입점입니다.
if __name__ == '__main__':
    # Tkinter 윈도우 객체(최상위 컨테이너)를 생성합니다.
    root = tk.Tk()
    # CalculatorApp 클래스의 인스턴스를 생성하여 계산기 GUI를 시작합니다.
    app = CalculatorApp(root)
    # 이벤트 루프를 시작하여 윈도우가 닫힐 때까지 사용자 입력을 기다립니다.
    root.mainloop()