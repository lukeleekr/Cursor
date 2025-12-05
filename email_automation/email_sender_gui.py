"""
축산물 발송 안내 메일 자동 발송 GUI 프로그램
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import threading
import time

# .env 파일 로드
load_dotenv()

# 테마 설정
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class EmailSenderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 윈도우 설정
        self.title("📧 팜앤푸드 메일 발송 시스템")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # 데이터 저장 변수
        self.df = None
        self.selected_row = None
        
        # Gmail 설정
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "lukeleekr@gmail.com"
        self.receiver_email = "lukeleekr@gmail.com"  # 테스트용
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")
        
        # UI 구성
        self.create_widgets()
        
    def create_widgets(self):
        """UI 위젯 생성"""
        
        # 메인 컨테이너
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ===== 상단 영역: 파일 선택 =====
        self.create_file_section()
        
        # ===== 중간 영역: 데이터 테이블 + 미리보기 =====
        self.create_middle_section()
        
        # ===== 하단 영역: 발송 설정 및 로그 =====
        self.create_bottom_section()
        
    def create_file_section(self):
        """파일 선택 섹션"""
        file_frame = ctk.CTkFrame(self.main_container)
        file_frame.pack(fill="x", pady=(0, 10))
        
        # 타이틀
        title_label = ctk.CTkLabel(
            file_frame, 
            text="🥩 팜앤푸드 메일 발송 시스템",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # 파일 선택 영역
        file_select_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_select_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.file_path_var = ctk.StringVar(value="엑셀 파일을 선택하세요...")
        
        self.file_entry = ctk.CTkEntry(
            file_select_frame,
            textvariable=self.file_path_var,
            width=600,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.file_entry.pack(side="left", padx=(0, 10))
        
        self.browse_btn = ctk.CTkButton(
            file_select_frame,
            text="📂 파일 선택",
            command=self.browse_file,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.browse_btn.pack(side="left", padx=(0, 10))
        
        self.load_btn = ctk.CTkButton(
            file_select_frame,
            text="📥 불러오기",
            command=self.load_excel,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        self.load_btn.pack(side="left")
        
    def create_middle_section(self):
        """중간 섹션: 테이블 + 미리보기"""
        middle_frame = ctk.CTkFrame(self.main_container)
        middle_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # 좌측: 데이터 테이블
        left_frame = ctk.CTkFrame(middle_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        table_label = ctk.CTkLabel(
            left_frame,
            text="📋 고객 목록",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        table_label.pack(pady=10)
        
        # Treeview 스타일 설정
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       rowheight=30,
                       font=('맑은 고딕', 10))
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       font=('맑은 고딕', 11, 'bold'))
        style.map("Treeview", background=[("selected", "#1f538d")])
        
        # 테이블 프레임
        table_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Treeview
        columns = ("번호", "고객번호", "고객명", "주문상품", "수량", "발송일")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # 컬럼 설정
        col_widths = [50, 80, 80, 100, 70, 100]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 행 선택 이벤트
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        
        # 우측: 메일 미리보기
        right_frame = ctk.CTkFrame(middle_frame, width=400)
        right_frame.pack(side="right", fill="both", padx=(5, 0))
        right_frame.pack_propagate(False)
        
        preview_label = ctk.CTkLabel(
            right_frame,
            text="📧 메일 미리보기",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_label.pack(pady=10)
        
        # 미리보기 정보
        info_frame = ctk.CTkFrame(right_frame)
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # 고객명
        self.preview_customer = ctk.CTkLabel(
            info_frame,
            text="고객명: -",
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        self.preview_customer.pack(fill="x", padx=10, pady=5)
        
        # 제목
        self.preview_subject = ctk.CTkLabel(
            info_frame,
            text="제목: -",
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        self.preview_subject.pack(fill="x", padx=10, pady=5)
        
        # 메일 내용
        content_label = ctk.CTkLabel(
            right_frame,
            text="내용:",
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        content_label.pack(fill="x", padx=10)
        
        self.preview_content = ctk.CTkTextbox(
            right_frame,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.preview_content.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
    def create_bottom_section(self):
        """하단 섹션: 발송 설정 및 로그"""
        bottom_frame = ctk.CTkFrame(self.main_container)
        bottom_frame.pack(fill="x")
        
        # 발송 설정
        settings_frame = ctk.CTkFrame(bottom_frame)
        settings_frame.pack(fill="x", pady=(0, 10))
        
        # 발송 개수 설정
        count_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        count_frame.pack(side="left", padx=20, pady=15)
        
        count_label = ctk.CTkLabel(
            count_frame,
            text="발송 개수:",
            font=ctk.CTkFont(size=14)
        )
        count_label.pack(side="left", padx=(0, 10))
        
        self.count_var = ctk.StringVar(value="10")
        self.count_entry = ctk.CTkEntry(
            count_frame,
            textvariable=self.count_var,
            width=80,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.count_entry.pack(side="left", padx=(0, 10))
        
        self.total_label = ctk.CTkLabel(
            count_frame,
            text="/ 총 0건",
            font=ctk.CTkFont(size=14)
        )
        self.total_label.pack(side="left")
        
        # 진행률 표시
        progress_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        progress_frame.pack(side="left", fill="x", expand=True, padx=20)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="대기 중",
            font=ctk.CTkFont(size=14)
        )
        self.progress_label.pack(side="left", padx=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=300)
        self.progress_bar.pack(side="left", fill="x", expand=True)
        self.progress_bar.set(0)
        
        # 발송 버튼
        btn_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=20, pady=15)
        
        self.send_btn = ctk.CTkButton(
            btn_frame,
            text="📤 메일 발송",
            command=self.start_sending,
            width=150,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#388E3C"
        )
        self.send_btn.pack(side="right")
        
        # 로그 영역
        log_frame = ctk.CTkFrame(bottom_frame)
        log_frame.pack(fill="x")
        
        log_label = ctk.CTkLabel(
            log_frame,
            text="📝 발송 로그",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        log_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=120,
            font=ctk.CTkFont(size=12)
        )
        self.log_text.pack(fill="x", padx=10, pady=(0, 10))
        
    def browse_file(self):
        """파일 선택 다이얼로그"""
        file_path = filedialog.askopenfilename(
            title="엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def load_excel(self):
        """엑셀 파일 로드"""
        file_path = self.file_path_var.get()
        
        if not file_path or file_path == "엑셀 파일을 선택하세요...":
            messagebox.showwarning("경고", "먼저 엑셀 파일을 선택하세요.")
            return
            
        try:
            self.df = pd.read_excel(file_path)
            self.populate_table()
            self.total_label.configure(text=f"/ 총 {len(self.df)}건")
            self.log("✅ 엑셀 파일 로드 완료: " + os.path.basename(file_path))
            self.log(f"   총 {len(self.df)}건의 데이터를 불러왔습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"파일 로드 실패:\n{e}")
            self.log(f"❌ 파일 로드 실패: {e}")
            
    def populate_table(self):
        """테이블에 데이터 채우기"""
        # 기존 데이터 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 데이터 추가
        for idx, row in self.df.iterrows():
            values = (
                idx + 1,
                row['고객번호'],
                row['고객명'],
                row['주문상품'],
                row['수량'],
                str(row['발송일'])[:10] if pd.notna(row['발송일']) else ''
            )
            self.tree.insert("", "end", values=values, iid=idx)
            
    def on_row_select(self, event):
        """행 선택 시 미리보기 업데이트"""
        selection = self.tree.selection()
        if not selection:
            return
            
        idx = int(selection[0])
        row = self.df.iloc[idx]
        
        self.preview_customer.configure(text=f"고객명: {row['고객명']}")
        self.preview_subject.configure(text=f"제목: {row['메일제목']}")
        
        self.preview_content.delete("1.0", "end")
        self.preview_content.insert("1.0", row['메일내용'])
        
    def log(self, message):
        """로그 메시지 추가"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        
    def start_sending(self):
        """메일 발송 시작"""
        if self.df is None or len(self.df) == 0:
            messagebox.showwarning("경고", "먼저 엑셀 파일을 불러오세요.")
            return
            
        if not self.gmail_password:
            messagebox.showerror("오류", "Gmail 앱 비밀번호가 설정되지 않았습니다.\n.env 파일을 확인하세요.")
            return
            
        try:
            count = int(self.count_var.get())
            if count <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("경고", "발송 개수를 올바르게 입력하세요.")
            return
            
        # 발송 확인
        if not messagebox.askyesno("발송 확인", f"{count}건의 메일을 발송하시겠습니까?"):
            return
            
        # 버튼 비활성화
        self.send_btn.configure(state="disabled")
        
        # 별도 스레드에서 발송
        thread = threading.Thread(target=self.send_emails, args=(count,))
        thread.daemon = True
        thread.start()
        
    def send_emails(self, count):
        """메일 발송 (별도 스레드)"""
        try:
            # SMTP 연결
            self.log("\n📧 Gmail SMTP 서버 연결 중...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.gmail_password)
            self.log("✅ SMTP 서버 연결 성공")
            
            # 발송할 데이터
            send_df = self.df.head(count)
            total = len(send_df)
            success = 0
            fail = 0
            
            self.log(f"\n📬 메일 발송 시작 (총 {total}건)")
            self.log("-" * 50)
            
            for idx, row in send_df.iterrows():
                # 진행률 업데이트
                progress = (idx + 1) / total
                self.after(0, lambda p=progress: self.progress_bar.set(p))
                self.after(0, lambda i=idx+1, t=total: self.progress_label.configure(
                    text=f"발송 중... {i}/{t}"
                ))
                
                customer_name = row['고객명']
                subject = row['메일제목']
                body = row['메일내용']
                
                self.log(f"[{idx + 1}/{total}] {customer_name}님...")
                
                # 메일 생성
                message = self.create_email(subject, body)
                
                try:
                    server.send_message(message)
                    self.log(f"  ✅ 발송 성공")
                    success += 1
                except Exception as e:
                    self.log(f"  ❌ 발송 실패: {e}")
                    fail += 1
                    
                time.sleep(1)  # 발송 제한 방지
                
            # 연결 종료
            server.quit()
            
            # 결과 출력
            self.log("\n" + "=" * 50)
            self.log("📊 발송 결과")
            self.log("=" * 50)
            self.log(f"✅ 성공: {success}건")
            self.log(f"❌ 실패: {fail}건")
            self.log("\n🎉 메일 발송이 완료되었습니다!")
            
            self.after(0, lambda: self.progress_label.configure(text="발송 완료!"))
            self.after(0, lambda: messagebox.showinfo(
                "완료", f"메일 발송이 완료되었습니다.\n\n성공: {success}건\n실패: {fail}건"
            ))
            
        except Exception as e:
            self.log(f"\n❌ 오류 발생: {e}")
            self.after(0, lambda: messagebox.showerror("오류", f"메일 발송 중 오류 발생:\n{e}"))
            
        finally:
            # 버튼 다시 활성화
            self.after(0, lambda: self.send_btn.configure(state="normal"))
            
    def create_email(self, subject, body):
        """이메일 메시지 생성"""
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = f"[테스트] {subject}"
        
        html_body = f"""
        <html>
        <body style="font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background-color: #4CAF50; color: white; padding: 20px; text-align: center;">
                    <h1 style="margin: 0;">🥩 팜앤푸드</h1>
                </div>
                <div style="padding: 20px; background-color: #f9f9f9;">
                    <p>{body}</p>
                </div>
                <div style="padding: 20px; text-align: center; color: #666; font-size: 12px;">
                    <p>본 메일은 테스트용으로 발송되었습니다.</p>
                    <p>© 2025 팜앤푸드. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(html_body, "html", "utf-8"))
        return message


if __name__ == "__main__":
    app = EmailSenderApp()
    app.mainloop()


