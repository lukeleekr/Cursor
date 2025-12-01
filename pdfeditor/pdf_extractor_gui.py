"""
PDF 도구 - GUI 버전
- 페이지 추출: PDF에서 원하는 페이지만 추출
- PDF 병합: 여러 PDF 파일을 하나로 합치기
- 드래그 앤 드롭 지원
"""

import os
from datetime import datetime
from tkinter import filedialog
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PyPDF2 import PdfReader, PdfWriter, PdfMerger


class PDFToolApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        # 윈도우 설정
        self.title("PDF 도구")
        self.geometry("540x750")
        self.resizable(False, False)
        
        # 라이트 테마 설정
        ctk.set_appearance_mode("light")
        
        # 커스텀 색상
        self.colors = {
            "primary": "#6366F1",
            "primary_hover": "#4F46E5",
            "secondary": "#F1F5F9",
            "accent": "#10B981",
            "danger": "#EF4444",
            "warning": "#F59E0B",
            "text": "#1E293B",
            "text_light": "#64748B",
            "white": "#FFFFFF",
            "border": "#E2E8F0"
        }
        
        # 변수 초기화
        self.pdf_path = ""
        self.total_pages = 0
        self.merge_files = []  # 병합할 파일 목록
        self.selected_file_idx = -1  # 선택된 파일 인덱스
        
        # 배경색 설정
        self.configure(fg_color=self.colors["white"])
        
        # UI 생성
        self.create_widgets()
    
    def create_widgets(self):
        # 제목
        title_label = ctk.CTkLabel(
            self, 
            text="PDF 도구",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=self.colors["text"]
        )
        title_label.pack(pady=(25, 5))
        
        subtitle_label = ctk.CTkLabel(
            self,
            text="페이지 추출 & PDF 병합",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_light"]
        )
        subtitle_label.pack(pady=(0, 15))
        
        # 탭뷰 생성
        self.tabview = ctk.CTkTabview(
            self, 
            width=480, 
            height=630,
            fg_color=self.colors["white"],
            segmented_button_fg_color=self.colors["secondary"],
            segmented_button_selected_color=self.colors["primary"],
            segmented_button_unselected_color=self.colors["secondary"]
        )
        self.tabview.pack(padx=25, pady=(0, 20))
        
        # 탭 추가
        self.tabview.add("📄 페이지 추출")
        self.tabview.add("📎 PDF 병합")
        
        # 각 탭 UI 생성
        self.create_extract_tab()
        self.create_merge_tab()
    
    # ==================== 페이지 추출 탭 ====================
    def create_extract_tab(self):
        tab = self.tabview.tab("📄 페이지 추출")
        
        # === PDF 파일 선택 섹션 ===
        file_frame = ctk.CTkFrame(
            tab, 
            fg_color=self.colors["secondary"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"]
        )
        file_frame.pack(fill="x", pady=(15, 12), padx=10)
        
        file_label = ctk.CTkLabel(
            file_frame, 
            text="📄 PDF 파일 (드래그 앤 드롭 가능)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        file_label.pack(anchor="w", padx=18, pady=(14, 8))
        
        # 드래그 앤 드롭 설정
        file_frame.drop_target_register(DND_FILES)
        file_frame.dnd_bind('<<Drop>>', self.on_extract_file_drop)
        
        file_select_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_select_frame.pack(fill="x", padx=18, pady=(0, 8))
        
        self.file_entry = ctk.CTkEntry(
            file_select_frame, 
            placeholder_text="파일을 선택하세요...",
            state="readonly",
            height=38,
            corner_radius=8,
            fg_color=self.colors["white"],
            border_color=self.colors["border"],
            text_color=self.colors["text"]
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        file_btn = ctk.CTkButton(
            file_select_frame, 
            text="찾아보기",
            width=90,
            height=38,
            corner_radius=8,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            command=self.select_file
        )
        file_btn.pack(side="right")
        
        self.page_info_label = ctk.CTkLabel(
            file_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_light"]
        )
        self.page_info_label.pack(anchor="w", padx=18, pady=(0, 14))
        
        # === 페이지 범위 섹션 ===
        range_frame = ctk.CTkFrame(
            tab, 
            fg_color=self.colors["secondary"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"]
        )
        range_frame.pack(fill="x", pady=(0, 12), padx=10)
        
        range_label = ctk.CTkLabel(
            range_frame, 
            text="📑 추출할 페이지 범위",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        range_label.pack(anchor="w", padx=18, pady=(14, 12))
        
        range_input_frame = ctk.CTkFrame(range_frame, fg_color="transparent")
        range_input_frame.pack(fill="x", padx=18, pady=(0, 14))
        
        start_label = ctk.CTkLabel(range_input_frame, text="시작", text_color=self.colors["text"])
        start_label.pack(side="left")
        
        self.start_entry = ctk.CTkEntry(
            range_input_frame, width=70, height=38, justify="center", corner_radius=8,
            fg_color=self.colors["white"], border_color=self.colors["border"], text_color=self.colors["text"]
        )
        self.start_entry.pack(side="left", padx=(8, 25))
        
        end_label = ctk.CTkLabel(range_input_frame, text="끝", text_color=self.colors["text"])
        end_label.pack(side="left")
        
        self.end_entry = ctk.CTkEntry(
            range_input_frame, width=70, height=38, justify="center", corner_radius=8,
            fg_color=self.colors["white"], border_color=self.colors["border"], text_color=self.colors["text"]
        )
        self.end_entry.pack(side="left", padx=(8, 0))
        
        # === 저장 위치 섹션 ===
        save_frame = ctk.CTkFrame(
            tab, 
            fg_color=self.colors["secondary"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"]
        )
        save_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        save_label = ctk.CTkLabel(
            save_frame, 
            text="📁 저장 위치",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        save_label.pack(anchor="w", padx=18, pady=(14, 8))
        
        save_select_frame = ctk.CTkFrame(save_frame, fg_color="transparent")
        save_select_frame.pack(fill="x", padx=18, pady=(0, 14))
        
        self.save_entry = ctk.CTkEntry(
            save_select_frame, 
            placeholder_text="원본 파일과 같은 위치",
            state="readonly",
            height=38,
            corner_radius=8,
            fg_color=self.colors["white"],
            border_color=self.colors["border"],
            text_color=self.colors["text"]
        )
        self.save_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            save_select_frame, 
            text="변경",
            width=90,
            height=38,
            corner_radius=8,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            command=self.select_save_location
        )
        save_btn.pack(side="right")
        
        # === 추출 버튼 ===
        self.extract_btn = ctk.CTkButton(
            tab,
            text="✨ 추출하기",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=55,
            corner_radius=12,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            command=self.extract_pages
        )
        self.extract_btn.pack(fill="x", pady=(0, 12), padx=10)
        
        # === 상태 메시지 ===
        self.extract_status_label = ctk.CTkLabel(
            tab, text="", font=ctk.CTkFont(size=13), wraplength=400
        )
        self.extract_status_label.pack(pady=(0, 5))
    
    # ==================== PDF 병합 탭 ====================
    def create_merge_tab(self):
        tab = self.tabview.tab("📎 PDF 병합")
        
        # === 파일 목록 섹션 ===
        list_frame = ctk.CTkFrame(
            tab, 
            fg_color=self.colors["secondary"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"]
        )
        list_frame.pack(fill="both", expand=True, pady=(15, 12), padx=10)
        
        list_header = ctk.CTkFrame(list_frame, fg_color="transparent")
        list_header.pack(fill="x", padx=18, pady=(14, 8))
        
        list_label = ctk.CTkLabel(
            list_header, 
            text="📎 병합할 PDF 파일 (드래그 앤 드롭 가능)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        list_label.pack(side="left")
        
        # 드래그 앤 드롭 설정
        list_frame.drop_target_register(DND_FILES)
        list_frame.dnd_bind('<<Drop>>', self.on_merge_file_drop)
        
        self.file_count_label = ctk.CTkLabel(
            list_header,
            text="0개",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_light"]
        )
        self.file_count_label.pack(side="right")
        
        # 파일 리스트 (스크롤 가능)
        self.file_list_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color=self.colors["white"],
            corner_radius=8,
            height=180
        )
        self.file_list_frame.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        
        # 안내 라벨
        self.merge_hint_label = ctk.CTkLabel(
            self.file_list_frame,
            text="파일을 추가하세요\n\n💡 1번 → 2번 → 3번 순서로 병합됩니다\n(1번 파일이 결과물의 앞쪽에 위치)",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_light"]
        )
        self.merge_hint_label.pack(pady=30)
        
        # === 컨트롤 버튼 바 ===
        control_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        control_frame.pack(fill="x", padx=18, pady=(0, 14))
        
        # 파일 추가 버튼
        add_btn = ctk.CTkButton(
            control_frame,
            text="➕ 추가",
            width=75,
            height=36,
            corner_radius=8,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            font=ctk.CTkFont(size=13),
            command=self.add_merge_files
        )
        add_btn.pack(side="left", padx=(0, 5))
        
        # 위로 버튼
        self.up_btn = ctk.CTkButton(
            control_frame,
            text="⬆ 위로",
            width=75,
            height=36,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            font=ctk.CTkFont(size=13),
            command=self.move_selected_up
        )
        self.up_btn.pack(side="left", padx=(0, 5))
        
        # 아래로 버튼
        self.down_btn = ctk.CTkButton(
            control_frame,
            text="⬇ 아래",
            width=75,
            height=36,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            font=ctk.CTkFont(size=13),
            command=self.move_selected_down
        )
        self.down_btn.pack(side="left", padx=(0, 5))
        
        # 선택 삭제 버튼
        self.del_btn = ctk.CTkButton(
            control_frame,
            text="🗑 삭제",
            width=75,
            height=36,
            corner_radius=8,
            fg_color=self.colors["danger"],
            hover_color="#DC2626",
            font=ctk.CTkFont(size=13),
            command=self.remove_selected
        )
        self.del_btn.pack(side="left", padx=(0, 5))
        
        # 전체 삭제 버튼
        clear_btn = ctk.CTkButton(
            control_frame,
            text="전체삭제",
            width=75,
            height=36,
            corner_radius=8,
            fg_color="#94A3B8",
            hover_color="#64748B",
            font=ctk.CTkFont(size=13),
            command=self.clear_merge_files
        )
        clear_btn.pack(side="right")
        
        # === 저장 위치 섹션 ===
        merge_save_frame = ctk.CTkFrame(
            tab, 
            fg_color=self.colors["secondary"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"]
        )
        merge_save_frame.pack(fill="x", pady=(0, 12), padx=10)
        
        merge_save_label = ctk.CTkLabel(
            merge_save_frame, 
            text="📁 저장 위치 및 파일명",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        merge_save_label.pack(anchor="w", padx=18, pady=(14, 8))
        
        merge_save_select_frame = ctk.CTkFrame(merge_save_frame, fg_color="transparent")
        merge_save_select_frame.pack(fill="x", padx=18, pady=(0, 14))
        
        self.merge_save_entry = ctk.CTkEntry(
            merge_save_select_frame, 
            placeholder_text="저장할 위치를 선택하세요...",
            state="readonly",
            height=38,
            corner_radius=8,
            fg_color=self.colors["white"],
            border_color=self.colors["border"],
            text_color=self.colors["text"]
        )
        self.merge_save_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        merge_save_btn = ctk.CTkButton(
            merge_save_select_frame, 
            text="선택",
            width=90,
            height=38,
            corner_radius=8,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            command=self.select_merge_save_location
        )
        merge_save_btn.pack(side="right")
        
        # === 병합 버튼 (더 크게) ===
        self.merge_btn = ctk.CTkButton(
            tab,
            text="🔗 병합하기",
            font=ctk.CTkFont(size=20, weight="bold"),
            height=60,
            corner_radius=12,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            command=self.merge_pdfs
        )
        self.merge_btn.pack(fill="x", pady=(0, 10), padx=10)
        
        # === 상태 메시지 ===
        self.merge_status_label = ctk.CTkLabel(
            tab, text="", font=ctk.CTkFont(size=13), wraplength=400
        )
        self.merge_status_label.pack(pady=(0, 5))
    
    # ==================== 페이지 추출 기능 ====================
    def on_extract_file_drop(self, event):
        """페이지 추출 탭에 파일 드롭 처리"""
        files = self.parse_drop_files(event.data)
        if files:
            # PDF 파일만 필터링
            pdf_files = [f for f in files if f.lower().endswith('.pdf')]
            if pdf_files:
                self.load_extract_file(pdf_files[0])  # 첫 번째 PDF 파일만 사용
            else:
                self.set_extract_status("❌ PDF 파일만 지원됩니다.", "red")
    
    def parse_drop_files(self, data):
        """드롭된 파일 경로 파싱"""
        files = []
        # Windows에서 여러 파일은 중괄호로 묶임
        if '{' in data:
            import re
            files = re.findall(r'\{([^}]+)\}', data)
            # 중괄호 없는 단일 파일도 처리
            remaining = re.sub(r'\{[^}]+\}', '', data).strip()
            if remaining:
                files.extend(remaining.split())
        else:
            files = data.split()
        return [f.strip() for f in files if f.strip()]
    
    def load_extract_file(self, file_path):
        """추출 탭에 파일 로드"""
        self.pdf_path = file_path
        self.file_entry.configure(state="normal")
        self.file_entry.delete(0, "end")
        self.file_entry.insert(0, os.path.basename(file_path))
        self.file_entry.configure(state="readonly")
        
        try:
            reader = PdfReader(file_path)
            self.total_pages = len(reader.pages)
            self.page_info_label.configure(
                text=f"전체 {self.total_pages} 페이지",
                text_color=self.colors["text_light"]
            )
            self.start_entry.delete(0, "end")
            self.start_entry.insert(0, "1")
            self.end_entry.delete(0, "end")
            self.end_entry.insert(0, str(self.total_pages))
            self.set_extract_status("✅ 파일이 로드되었습니다.", "green")
        except Exception as e:
            self.set_extract_status(f"❌ 파일을 읽을 수 없습니다: {e}", "red")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="PDF 파일 선택",
            filetypes=[("PDF 파일", "*.pdf"), ("모든 파일", "*.*")]
        )
        
        if file_path:
            self.pdf_path = file_path
            self.file_entry.configure(state="normal")
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, os.path.basename(file_path))
            self.file_entry.configure(state="readonly")
            
            try:
                reader = PdfReader(file_path)
                self.total_pages = len(reader.pages)
                self.page_info_label.configure(
                    text=f"전체 {self.total_pages} 페이지",
                    text_color=self.colors["text_light"]
                )
                self.start_entry.delete(0, "end")
                self.start_entry.insert(0, "1")
                self.end_entry.delete(0, "end")
                self.end_entry.insert(0, str(self.total_pages))
                self.set_extract_status("", "gray")
            except Exception as e:
                self.set_extract_status(f"❌ 파일을 읽을 수 없습니다: {e}", "red")
    
    def select_save_location(self):
        folder_path = filedialog.askdirectory(title="저장 위치 선택")
        if folder_path:
            self.save_entry.configure(state="normal")
            self.save_entry.delete(0, "end")
            self.save_entry.insert(0, folder_path)
            self.save_entry.configure(state="readonly")
    
    def extract_pages(self):
        if not self.pdf_path:
            self.set_extract_status("❌ PDF 파일을 선택해주세요.", "red")
            return
        
        try:
            start_page = int(self.start_entry.get())
            end_page = int(self.end_entry.get())
        except ValueError:
            self.set_extract_status("❌ 페이지 번호를 올바르게 입력해주세요.", "red")
            return
        
        if start_page < 1:
            self.set_extract_status("❌ 시작 페이지는 1 이상이어야 합니다.", "red")
            return
        if end_page > self.total_pages:
            self.set_extract_status(f"❌ 끝 페이지가 전체 페이지 수({self.total_pages})를 초과합니다.", "red")
            return
        if start_page > end_page:
            self.set_extract_status("❌ 시작 페이지가 끝 페이지보다 클 수 없습니다.", "red")
            return
        
        save_dir = self.save_entry.get()
        if not save_dir or save_dir == "원본 파일과 같은 위치":
            save_dir = os.path.dirname(self.pdf_path)
        
        base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"{base_name}_{timestamp}.pdf"
        output_path = os.path.join(save_dir, output_name)
        
        try:
            self.set_extract_status("🔄 추출 중...", "orange")
            self.update()
            
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()
            
            for page_num in range(start_page - 1, end_page):
                writer.add_page(reader.pages[page_num])
            
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            self.set_extract_status(f"✅ 추출 완료! → {output_name}", "green")
        except Exception as e:
            self.set_extract_status(f"❌ 오류 발생: {e}", "red")
    
    def set_extract_status(self, message: str, color: str):
        color_map = {
            "red": self.colors["danger"],
            "green": self.colors["accent"],
            "orange": self.colors["warning"],
            "gray": self.colors["text_light"]
        }
        self.extract_status_label.configure(text=message, text_color=color_map.get(color, color))
    
    # ==================== PDF 병합 기능 ====================
    def on_merge_file_drop(self, event):
        """병합 탭에 파일 드롭 처리"""
        files = self.parse_drop_files(event.data)
        if files:
            # PDF 파일만 필터링
            pdf_files = [f for f in files if f.lower().endswith('.pdf')]
            if pdf_files:
                added = 0
                for path in pdf_files:
                    if path not in self.merge_files:
                        self.merge_files.append(path)
                        added += 1
                self.update_merge_file_list()
                if added > 0:
                    self.set_merge_status(f"✅ {added}개 파일이 추가되었습니다.", "green")
            else:
                self.set_merge_status("❌ PDF 파일만 지원됩니다.", "red")
    
    def add_merge_files(self):
        file_paths = filedialog.askopenfilenames(
            title="PDF 파일 선택 (여러 개 선택 가능)",
            filetypes=[("PDF 파일", "*.pdf"), ("모든 파일", "*.*")]
        )
        
        if file_paths:
            for path in file_paths:
                if path not in self.merge_files:
                    self.merge_files.append(path)
            self.update_merge_file_list()
    
    def update_merge_file_list(self):
        # 기존 위젯 삭제
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        
        if not self.merge_files:
            self.selected_file_idx = -1
            self.merge_hint_label = ctk.CTkLabel(
                self.file_list_frame,
                text="파일을 추가하세요\n\n💡 1번 → 2번 → 3번 순서로 병합됩니다\n(1번 파일이 결과물의 앞쪽에 위치)",
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_light"]
            )
            self.merge_hint_label.pack(pady=30)
        else:
            # 선택 인덱스가 범위를 벗어나면 조정
            if self.selected_file_idx >= len(self.merge_files):
                self.selected_file_idx = len(self.merge_files) - 1
            
            # 순서 안내 라벨
            order_hint = ctk.CTkLabel(
                self.file_list_frame,
                text="💡 1번이 결과물의 맨 앞 페이지가 됩니다",
                font=ctk.CTkFont(size=11),
                text_color=self.colors["text_light"]
            )
            order_hint.pack(pady=(5, 8))
            
            for idx, file_path in enumerate(self.merge_files):
                self.create_file_item(idx, file_path)
        
        self.file_count_label.configure(text=f"{len(self.merge_files)}개")
    
    def create_file_item(self, idx: int, file_path: str):
        # 선택 여부에 따라 배경색 변경
        is_selected = (idx == self.selected_file_idx)
        bg_color = self.colors["primary"] if is_selected else self.colors["secondary"]
        text_color = self.colors["white"] if is_selected else self.colors["text"]
        num_color = self.colors["white"] if is_selected else self.colors["primary"]
        
        item_frame = ctk.CTkFrame(
            self.file_list_frame,
            fg_color=bg_color,
            corner_radius=8,
            height=44
        )
        item_frame.pack(fill="x", pady=2)
        item_frame.pack_propagate(False)
        
        # 순서 번호
        num_label = ctk.CTkLabel(
            item_frame,
            text=f"{idx + 1}.",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=num_color,
            width=30
        )
        num_label.pack(side="left", padx=(12, 5))
        
        # 파일명
        name_label = ctk.CTkLabel(
            item_frame,
            text=os.path.basename(file_path),
            font=ctk.CTkFont(size=13),
            text_color=text_color,
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 클릭 이벤트 바인딩 (선택 기능)
        for widget in [item_frame, num_label, name_label]:
            widget.bind("<Button-1>", lambda e, i=idx: self.select_file_item(i))
    
    def select_file_item(self, idx: int):
        """파일 항목 선택"""
        self.selected_file_idx = idx
        self.update_merge_file_list()
    
    def move_selected_up(self):
        """선택된 파일을 위로 이동"""
        if self.selected_file_idx > 0:
            idx = self.selected_file_idx
            self.merge_files[idx], self.merge_files[idx - 1] = self.merge_files[idx - 1], self.merge_files[idx]
            self.selected_file_idx = idx - 1
            self.update_merge_file_list()
        elif self.selected_file_idx == -1:
            self.set_merge_status("⚠️ 파일을 먼저 선택해주세요.", "orange")
    
    def move_selected_down(self):
        """선택된 파일을 아래로 이동"""
        if 0 <= self.selected_file_idx < len(self.merge_files) - 1:
            idx = self.selected_file_idx
            self.merge_files[idx], self.merge_files[idx + 1] = self.merge_files[idx + 1], self.merge_files[idx]
            self.selected_file_idx = idx + 1
            self.update_merge_file_list()
        elif self.selected_file_idx == -1:
            self.set_merge_status("⚠️ 파일을 먼저 선택해주세요.", "orange")
    
    def remove_selected(self):
        """선택된 파일 삭제"""
        if 0 <= self.selected_file_idx < len(self.merge_files):
            del self.merge_files[self.selected_file_idx]
            self.update_merge_file_list()
            self.set_merge_status("", "gray")
        else:
            self.set_merge_status("⚠️ 삭제할 파일을 선택해주세요.", "orange")
    
    def clear_merge_files(self):
        self.merge_files = []
        self.update_merge_file_list()
    
    def select_merge_save_location(self):
        file_path = filedialog.asksaveasfilename(
            title="저장할 파일 선택",
            defaultextension=".pdf",
            filetypes=[("PDF 파일", "*.pdf")],
            initialfile=f"병합_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if file_path:
            self.merge_save_entry.configure(state="normal")
            self.merge_save_entry.delete(0, "end")
            self.merge_save_entry.insert(0, file_path)
            self.merge_save_entry.configure(state="readonly")
    
    def merge_pdfs(self):
        if len(self.merge_files) < 2:
            self.set_merge_status("❌ 병합할 PDF 파일을 2개 이상 추가해주세요.", "red")
            return
        
        save_path = self.merge_save_entry.get()
        if not save_path:
            self.set_merge_status("❌ 저장 위치를 선택해주세요.", "red")
            return
        
        try:
            self.set_merge_status("🔄 병합 중...", "orange")
            self.update()
            
            merger = PdfMerger()
            
            for file_path in self.merge_files:
                merger.append(file_path)
            
            merger.write(save_path)
            merger.close()
            
            self.set_merge_status(f"✅ 병합 완료! → {os.path.basename(save_path)}", "green")
        except Exception as e:
            self.set_merge_status(f"❌ 오류 발생: {e}", "red")
    
    def set_merge_status(self, message: str, color: str):
        color_map = {
            "red": self.colors["danger"],
            "green": self.colors["accent"],
            "orange": self.colors["warning"],
            "gray": self.colors["text_light"]
        }
        self.merge_status_label.configure(text=message, text_color=color_map.get(color, color))


if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()
