"""
고객 리뷰 분석 보고서 생성기 GUI
tkinter를 사용한 그래픽 사용자 인터페이스
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
from review_report_generator import ReviewReportGenerator


class ReviewReportGUI:
    """고객 리뷰 분석 보고서 생성기 GUI 클래스"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("고객 리뷰 분석 보고서 생성기")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.excel_file_path = None
        self.output_dir = "reports"
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성 요소 설정"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 제목
        title_label = ttk.Label(
            main_frame, 
            text="고객 리뷰 분석 보고서 생성기",
            font=("맑은 고딕", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Excel 파일 선택
        ttk.Label(main_frame, text="Excel 파일:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(main_frame, textvariable=self.file_path_var, width=50, state='readonly')
        file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        browse_btn = ttk.Button(main_frame, text="파일 선택", command=self.browse_file)
        browse_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # 출력 디렉토리 선택
        ttk.Label(main_frame, text="저장 위치:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.output_dir_var = tk.StringVar(value=self.output_dir)
        output_entry = ttk.Entry(main_frame, textvariable=self.output_dir_var, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        output_btn = ttk.Button(main_frame, text="폴더 선택", command=self.browse_output_dir)
        output_btn.grid(row=2, column=2, padx=5, pady=5)
        
        # 분석 시작 버튼
        self.analyze_btn = ttk.Button(
            main_frame, 
            text="분석 시작", 
            command=self.start_analysis,
            state='disabled'
        )
        self.analyze_btn.grid(row=3, column=0, columnspan=3, pady=20)
        
        # 진행 상황 표시
        ttk.Label(main_frame, text="진행 상황:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.progress_var = tk.StringVar(value="대기 중...")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        progress_label.grid(row=4, column=1, sticky=tk.W, padx=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 로그 영역
        ttk.Label(main_frame, text="로그:").grid(row=6, column=0, sticky=(tk.W, tk.N), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame, 
            height=15, 
            width=70,
            state='disabled'
        )
        self.log_text.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        main_frame.rowconfigure(7, weight=1)
        
        # 결과 표시 영역
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(result_frame, textvariable=self.result_var, foreground="green")
        self.result_label.grid(row=0, column=0)
        
        self.open_report_btn = ttk.Button(
            result_frame,
            text="보고서 열기",
            command=self.open_report,
            state='disabled'
        )
        self.open_report_btn.grid(row=0, column=1, padx=10)
        
        self.generated_report_path = None
    
    def browse_file(self):
        """Excel 파일 선택 대화상자"""
        file_path = filedialog.askopenfilename(
            title="Excel 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            self.excel_file_path = file_path
            self.file_path_var.set(file_path)
            self.analyze_btn.config(state='normal')
            self.log_message(f"파일 선택됨: {os.path.basename(file_path)}")
    
    def browse_output_dir(self):
        """출력 디렉토리 선택 대화상자"""
        dir_path = filedialog.askdirectory(title="저장 위치 선택")
        
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_var.set(dir_path)
            self.log_message(f"저장 위치: {dir_path}")
    
    def log_message(self, message):
        """로그 메시지 추가"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
    
    def start_analysis(self):
        """분석 시작 (별도 스레드에서 실행)"""
        if not self.excel_file_path:
            messagebox.showerror("오류", "Excel 파일을 선택해주세요.")
            return
        
        # UI 비활성화
        self.analyze_btn.config(state='disabled')
        self.progress_bar.start()
        self.progress_var.set("분석 중...")
        self.result_var.set("")
        self.open_report_btn.config(state='disabled')
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # 별도 스레드에서 분석 실행
        thread = threading.Thread(target=self.run_analysis, daemon=True)
        thread.start()
    
    def run_analysis(self):
        """실제 분석 실행 (별도 스레드)"""
        try:
            self.log_message("=" * 60)
            self.log_message("고객 리뷰 분석 시작")
            self.log_message("=" * 60)
            
            # 출력 디렉토리 업데이트
            output_dir = self.output_dir_var.get() or "reports"
            
            # 보고서 생성기 초기화
            self.log_message(f"\n엑셀 파일 로드 중: {os.path.basename(self.excel_file_path)}")
            generator = ReviewReportGenerator(
                excel_file=self.excel_file_path,
                output_dir=output_dir
            )
            
            # 리뷰 컬럼 감지
            self.log_message("리뷰 컬럼 자동 감지 중...")
            review_col = generator.detect_review_column()
            self.log_message(f"감지된 리뷰 컬럼: {review_col}")
            
            # 분석 수행
            self.log_message("\n데이터 분석 중... (OpenAI API 호출 중이므로 시간이 걸릴 수 있습니다)")
            generator.analyze()
            
            # 보고서 생성
            self.log_message("\n보고서 생성 중...")
            report_path = generator.generate_report()
            self.generated_report_path = report_path
            
            # HTML 보고서도 생성됨
            html_path = report_path.replace('.md', '.html')
            
            # 요약 정보
            summary = generator.get_summary()
            
            # UI 업데이트 (메인 스레드에서)
            self.root.after(0, self.analysis_complete, report_path, html_path, summary)
            
        except Exception as e:
            error_msg = f"오류 발생: {str(e)}"
            self.log_message(f"\n{error_msg}")
            self.root.after(0, self.analysis_error, error_msg)
    
    def analysis_complete(self, report_path, html_path, summary):
        """분석 완료 후 UI 업데이트"""
        self.progress_bar.stop()
        self.progress_var.set("완료!")
        self.analyze_btn.config(state='normal')
        
        self.log_message("\n" + "=" * 60)
        self.log_message("분석 완료!")
        self.log_message("=" * 60)
        self.log_message(f"\n생성된 보고서:")
        self.log_message(f"  - Markdown: {report_path}")
        self.log_message(f"  - HTML: {html_path}")
        self.log_message(f"\n분석 요약:")
        self.log_message(f"  - 총 리뷰 수: {summary['total_reviews']}")
        if 'average_rating' in summary:
            self.log_message(f"  - 평균 평점: {summary['average_rating']:.2f}")
        if 'sentiment' in summary:
            self.log_message(f"  - 긍정: {summary['sentiment']['positive']}개")
            self.log_message(f"  - 부정: {summary['sentiment']['negative']}개")
            self.log_message(f"  - 중립: {summary['sentiment']['neutral']}개")
        
        self.result_var.set(f"보고서 생성 완료: {os.path.basename(report_path)}")
        self.open_report_btn.config(state='normal')
        
        messagebox.showinfo("완료", f"보고서가 생성되었습니다!\n\n{report_path}")
    
    def analysis_error(self, error_msg):
        """분석 오류 시 UI 업데이트"""
        self.progress_bar.stop()
        self.progress_var.set("오류 발생")
        self.analyze_btn.config(state='normal')
        messagebox.showerror("오류", error_msg)
    
    def open_report(self):
        """생성된 보고서 열기"""
        if self.generated_report_path and os.path.exists(self.generated_report_path):
            # HTML 보고서가 있으면 HTML을, 없으면 Markdown을 열기
            html_path = self.generated_report_path.replace('.md', '.html')
            if os.path.exists(html_path):
                os.startfile(html_path)
            else:
                os.startfile(self.generated_report_path)
        else:
            messagebox.showwarning("경고", "보고서 파일을 찾을 수 없습니다.")


def main():
    """GUI 애플리케이션 실행"""
    root = tk.Tk()
    app = ReviewReportGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

