"""
키워드 + 참고자료 + 사용자 입력 기반 블로그 글 생성기 (GUI 버전)
OpenAI GPT-4o를 활용 (이미지, PDF 등 다양한 파일 지원)
"""

import os
import base64
import customtkinter as ctk
from tkinter import filedialog, messagebox, Frame
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import threading
import mimetypes

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 테마 설정
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 지원 파일 형식
SUPPORTED_FILES = {
    "텍스트": [".txt", ".md", ".csv", ".json", ".xml", ".html"],
    "이미지": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    "문서": [".pdf"]
}

ALL_EXTENSIONS = []
for exts in SUPPORTED_FILES.values():
    ALL_EXTENSIONS.extend(exts)


def get_file_type(filepath):
    """파일 형식 판별"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in SUPPORTED_FILES["이미지"]:
        return "image"
    elif ext in SUPPORTED_FILES["문서"]:
        return "pdf"
    else:
        return "text"


def encode_file_to_base64(filepath):
    """파일을 Base64로 인코딩"""
    with open(filepath, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def get_mime_type(filepath):
    """파일의 MIME 타입 반환"""
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        ext = os.path.splitext(filepath)[1].lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".pdf": "application/pdf"
        }
        return mime_map.get(ext, "application/octet-stream")
    return mime_type


class ArticleWriterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 윈도우 설정
        self.title("📝 AI 칼럼 생성기 (다중 파일 지원)")
        self.geometry("1100x900")
        self.minsize(900, 700)
        
        # 첨부 파일 목록
        self.attached_files = []
        
        # UI 구성
        self.setup_ui()
    
    def setup_ui(self):
        # 메인 컨테이너
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        # ========== 상단: 키워드 입력 ==========
        keyword_frame = ctk.CTkFrame(self, corner_radius=10)
        keyword_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        keyword_frame.grid_columnconfigure(1, weight=1)
        
        keyword_label = ctk.CTkLabel(keyword_frame, text="🔑 키워드:", font=("", 14, "bold"))
        keyword_label.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="w")
        
        self.keyword_entry = ctk.CTkEntry(
            keyword_frame, 
            placeholder_text="칼럼의 주제 키워드를 입력하세요", 
            height=40, 
            font=("", 14)
        )
        self.keyword_entry.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="ew")
        
        # ========== 파일 첨부 영역 ==========
        file_frame = ctk.CTkFrame(self, corner_radius=10)
        file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        file_frame.grid_columnconfigure(0, weight=1)
        
        # 파일 헤더
        file_header = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_header.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")
        file_header.grid_columnconfigure(1, weight=1)
        
        file_label = ctk.CTkLabel(file_header, text="📎 참고자료 파일:", font=("", 14, "bold"))
        file_label.grid(row=0, column=0, sticky="w")
        
        supported_label = ctk.CTkLabel(
            file_header, 
            text="지원: 이미지(PNG, JPG, GIF, WEBP), PDF, 텍스트(TXT, MD, CSV, JSON)", 
            font=("", 11), 
            text_color="gray"
        )
        supported_label.grid(row=0, column=1, padx=(10, 0), sticky="w")
        
        # 파일 버튼
        file_btn_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_btn_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        
        self.add_file_btn = ctk.CTkButton(
            file_btn_frame, 
            text="➕ 파일 추가", 
            width=120, 
            command=self.add_file
        )
        self.add_file_btn.pack(side="left", padx=(0, 10))
        
        self.clear_files_btn = ctk.CTkButton(
            file_btn_frame, 
            text="🗑️ 전체 삭제", 
            width=100, 
            fg_color="gray",
            command=self.clear_all_files
        )
        self.clear_files_btn.pack(side="left")
        
        # 첨부 파일 목록
        self.files_listbox_frame = ctk.CTkScrollableFrame(file_frame, height=80)
        self.files_listbox_frame.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="ew")
        self.files_listbox_frame.grid_columnconfigure(0, weight=1)
        
        self.no_files_label = ctk.CTkLabel(
            self.files_listbox_frame, 
            text="첨부된 파일이 없습니다 (선택사항)", 
            text_color="gray"
        )
        self.no_files_label.grid(row=0, column=0, pady=10)
        
        # ========== 사용자 직접 입력 영역 ==========
        user_input_frame = ctk.CTkFrame(self, corner_radius=10)
        user_input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        user_input_frame.grid_columnconfigure(0, weight=1)
        
        user_input_label = ctk.CTkLabel(
            user_input_frame, 
            text="✏️ 추가 내용 직접 입력 (선택사항):", 
            font=("", 14, "bold")
        )
        user_input_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        user_input_hint = ctk.CTkLabel(
            user_input_frame, 
            text="글에 포함하고 싶은 특정 정보, 관점, 요청사항 등을 입력하세요", 
            font=("", 11), 
            text_color="gray"
        )
        user_input_hint.grid(row=1, column=0, padx=15, pady=(0, 5), sticky="w")
        
        self.user_input_textbox = ctk.CTkTextbox(user_input_frame, height=100, font=("", 13))
        self.user_input_textbox.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        # ========== 버튼 영역 ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, padx=20, pady=10)
        
        self.generate_btn = ctk.CTkButton(
            button_frame, 
            text="✨ 블로그 글 생성", 
            width=200, 
            height=50, 
            font=("", 16, "bold"),
            command=self.generate_article
        )
        self.generate_btn.pack(side="left", padx=10)
        
        self.save_btn = ctk.CTkButton(
            button_frame, 
            text="💾 저장", 
            width=100, 
            height=50,
            font=("", 14),
            fg_color="green",
            command=self.save_article,
            state="disabled"
        )
        self.save_btn.pack(side="left", padx=10)
        
        # 모델 선택
        model_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        model_frame.pack(side="left", padx=20)
        
        model_label = ctk.CTkLabel(model_frame, text="모델:", font=("", 12))
        model_label.pack(side="left", padx=(0, 5))
        
        self.model_var = ctk.StringVar(value="gpt-5-nano")
        self.model_dropdown = ctk.CTkOptionMenu(
            model_frame,
            values=["gpt-5-nano", "gpt-5-mini", "gpt-5", "gpt-4o", "gpt-4o-mini"],
            variable=self.model_var,
            width=130
        )
        self.model_dropdown.pack(side="left")
        
        # 진행 상태
        self.progress_label = ctk.CTkLabel(self, text="", font=("", 12))
        self.progress_label.grid(row=4, column=0, pady=(10, 5), sticky="n")
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.grid(row=4, column=0, pady=(35, 10), sticky="n")
        self.progress_bar.set(0)
        
        # ========== 결과 영역 컨테이너 ==========
        self.result_container = ctk.CTkFrame(self, fg_color="transparent")
        self.result_container.grid(row=5, column=0, sticky="nsew", padx=0, pady=0)
        self.grid_rowconfigure(5, weight=1)
        self.result_container.grid_columnconfigure(0, weight=1)
        
        # 드래그 상태 변수 초기화
        self.splitter_dragging = False
        self.result_min_height = 200  # 최소 높이 (px)
        self.result_height = 400  # 초기 높이 (px)
        
        # ========== 결과 영역 프레임 ==========
        self.result_frame = ctk.CTkFrame(self.result_container, corner_radius=10)
        self.result_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=1)
        
        result_label = ctk.CTkLabel(self.result_frame, text="📄 생성된 칼럼", font=("", 14, "bold"))
        result_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.result_textbox = ctk.CTkTextbox(self.result_frame, font=("", 13), wrap="word")
        self.result_textbox.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")
        
        # 초기 높이 설정
        self.result_frame.configure(height=self.result_height)
        
        # ========== 드래그 가능한 구분선 (텍스트 박스 위) ==========
        # tkinter 기본 위젯 사용 (이벤트 처리가 더 확실함)
        splitter_frame = Frame(self.result_container, bg="#1a1a1a", height=10)
        splitter_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        splitter_frame.grid_columnconfigure(0, weight=1)
        
        # 구분선 (드래그 가능한 영역)
        # Windows 호환 커서 사용
        self.splitter = Frame(splitter_frame, bg="#4a4a4a", height=10, cursor="sb_v_double_arrow")
        self.splitter.pack(fill="both", expand=True)
        
        # 구분선 내부 핸들 (시각적 표시)
        handle = Frame(self.splitter, bg="#6a6a6a", height=2, width=80)
        handle.place(relx=0.5, rely=0.5, anchor="center")
        
        # 이벤트 바인딩 (구분선과 핸들 모두)
        for widget in [self.splitter, handle, splitter_frame]:
            widget.bind("<Button-1>", self.on_splitter_press)
            widget.bind("<B1-Motion>", self.on_splitter_drag)
            widget.bind("<ButtonRelease-1>", self.on_splitter_release)
            widget.bind("<Enter>", lambda e: self.splitter.configure(cursor="sb_v_double_arrow"))
            widget.bind("<Leave>", lambda e: self.splitter.configure(cursor=""))
        
        # 전역 마우스 이벤트 (드래그 중 창 밖으로 나갔다가 돌아올 때)
        self.bind_all("<B1-Motion>", self.on_splitter_drag_global)
        self.bind_all("<ButtonRelease-1>", self.on_splitter_release_global)
    
    def on_splitter_press(self, event):
        """구분선 클릭 시작"""
        self.splitter_dragging = True
        self.splitter_start_y = event.y_root
        self.result_start_height = self.result_height
        # 이벤트 전파 중단
        return "break"
    
    def on_splitter_drag(self, event):
        """구분선 드래그 중 (로컬 이벤트)"""
        if self.splitter_dragging:
            self._update_result_height(event.y_root)
        return "break"
    
    def on_splitter_drag_global(self, event):
        """구분선 드래그 중 (전역 이벤트)"""
        if self.splitter_dragging:
            self._update_result_height(event.y_root)
    
    def on_splitter_release(self, event):
        """구분선 드래그 종료 (로컬 이벤트)"""
        self.splitter_dragging = False
        return "break"
    
    def on_splitter_release_global(self, event):
        """구분선 드래그 종료 (전역 이벤트)"""
        self.splitter_dragging = False
    
    def _update_result_height(self, current_y_root):
        """결과 영역 높이 업데이트 (실시간)"""
        try:
            # 마우스 이동 거리 계산
            delta_y = current_y_root - self.splitter_start_y
            
            # 새로운 높이 계산 (위로 드래그 = 높이 증가, 아래로 드래그 = 높이 감소)
            new_height = self.result_start_height - delta_y
            
            # 최소 높이 제한
            if new_height < self.result_min_height:
                new_height = self.result_min_height
                # 시작 위치 조정 (경계에서 멈추도록)
                self.splitter_start_y = current_y_root - (self.result_start_height - new_height)
            
            # 최대 높이 제한 (창 높이에서 다른 요소들 제외한 공간)
            window_height = self.winfo_height()
            # 상단 영역들 대략적 높이 (키워드, 파일, 사용자 입력, 버튼, 진행바 등)
            top_area_height = 500
            max_height = max(window_height - top_area_height - 50, self.result_min_height)
            
            if new_height > max_height:
                new_height = max_height
                # 시작 위치 조정
                self.splitter_start_y = current_y_root - (self.result_start_height - new_height)
            
            # 결과 영역 높이 업데이트
            self.result_height = int(new_height)
            self.result_frame.configure(height=self.result_height)
            
            # 즉시 화면 업데이트
            self.update_idletasks()
            
        except Exception as e:
            print(f"높이 업데이트 오류: {e}")
    
    def add_file(self):
        """파일 추가"""
        filetypes = [
            ("지원되는 모든 파일", " ".join(f"*{ext}" for ext in ALL_EXTENSIONS)),
            ("이미지", "*.png *.jpg *.jpeg *.gif *.webp"),
            ("PDF", "*.pdf"),
            ("텍스트", "*.txt *.md *.csv *.json"),
            ("모든 파일", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="참고 자료 파일 선택",
            filetypes=filetypes
        )
        
        for filepath in files:
            if filepath not in self.attached_files:
                self.attached_files.append(filepath)
        
        self.update_file_list()
    
    def remove_file(self, filepath):
        """특정 파일 제거"""
        if filepath in self.attached_files:
            self.attached_files.remove(filepath)
        self.update_file_list()
    
    def clear_all_files(self):
        """모든 파일 제거"""
        self.attached_files = []
        self.update_file_list()
    
    def update_file_list(self):
        """파일 목록 UI 업데이트"""
        # 기존 위젯 삭제
        for widget in self.files_listbox_frame.winfo_children():
            widget.destroy()
        
        if not self.attached_files:
            self.no_files_label = ctk.CTkLabel(
                self.files_listbox_frame, 
                text="첨부된 파일이 없습니다 (선택사항)", 
                text_color="gray"
            )
            self.no_files_label.grid(row=0, column=0, pady=10)
        else:
            for i, filepath in enumerate(self.attached_files):
                file_item = ctk.CTkFrame(self.files_listbox_frame, fg_color="transparent")
                file_item.grid(row=i, column=0, sticky="ew", pady=2)
                file_item.grid_columnconfigure(1, weight=1)
                
                # 파일 타입 아이콘
                file_type = get_file_type(filepath)
                icon = "🖼️" if file_type == "image" else "📄" if file_type == "pdf" else "📝"
                
                icon_label = ctk.CTkLabel(file_item, text=icon, width=30)
                icon_label.grid(row=0, column=0, padx=(0, 5))
                
                filename = os.path.basename(filepath)
                name_label = ctk.CTkLabel(file_item, text=filename, anchor="w")
                name_label.grid(row=0, column=1, sticky="ew")
                
                remove_btn = ctk.CTkButton(
                    file_item, 
                    text="✕", 
                    width=30, 
                    height=25,
                    fg_color="red",
                    hover_color="darkred",
                    command=lambda fp=filepath: self.remove_file(fp)
                )
                remove_btn.grid(row=0, column=2, padx=(5, 0))
    
    def generate_article(self):
        """블로그 글 생성"""
        keyword = self.keyword_entry.get().strip()
        
        if not keyword:
            messagebox.showwarning("입력 필요", "키워드를 입력해주세요.")
            return
        
        # UI 상태 변경
        self.generate_btn.configure(state="disabled", text="생성 중...")
        self.save_btn.configure(state="disabled")
        self.progress_label.configure(text="🔄 AI가 블로그 글을 작성하고 있습니다...")
        self.progress_bar.set(0)
        self.progress_bar.start()
        
        # 결과 초기화
        self.result_textbox.delete("1.0", "end")
        
        # 사용자 직접 입력 내용
        user_additional = self.user_input_textbox.get("1.0", "end").strip()
        
        # 백그라운드에서 API 호출
        thread = threading.Thread(
            target=self._generate_thread, 
            args=(keyword, user_additional)
        )
        thread.start()
    
    def _generate_thread(self, keyword, user_additional):
        """백그라운드 스레드에서 API 호출"""
        try:
            result = self._call_api(keyword, user_additional)
            self.after(0, lambda: self._on_generation_complete(result))
        except Exception as e:
            self.after(0, lambda: self._on_generation_error(str(e)))
    
    def _call_api(self, keyword: str, user_additional: str) -> str:
        """OpenAI API 호출"""
        
        system_prompt = """당신은 10년 경력의 전문 블로그 작가입니다. 
복잡한 주제를 일반 독자들이 이해하기 쉽게 설명하는 능력이 뛰어납니다.

블로그 글 작성 시 다음 원칙을 따르세요:

1. **구조**: 
   - 흥미로운 도입부로 시작 (독자의 관심을 끄는 질문이나 상황 제시)
   - 본론에서 핵심 내용을 3-4개 섹션으로 나누어 분석
   - 통찰력 있는 결론으로 마무리

2. **톤앤매너**:
   - 전문적이면서도 친근한 어조
   - 독자와 대화하듯이 작성
   - 지나치게 딱딱하거나 학술적이지 않게

3. **전문 용어 처리**:
   - 전문 용어가 나오면 반드시 쉬운 말로 풀어서 설명
   - 일상적인 비유나 예시를 들어 이해를 도움
   - 예: "인플레이션(물가상승률) - 쉽게 말해, 작년에 1000원이던 라면이 올해 1100원이 되는 현상입니다"

4. **분석적 관점**:
   - 단순 정보 나열이 아닌, '왜?'와 '어떻게?'에 초점
   - 다양한 시각에서 주제를 조명
   - 현실적인 사례와 데이터 활용
   - 독자가 생각해볼 만한 질문 제시

5. **참고 자료 활용**:
   - 제공된 참고 자료(이미지, PDF, 텍스트)가 있다면 그 내용을 바탕으로 정확한 정보 전달
   - 이미지의 경우 시각적 정보를 텍스트로 설명하고 글에 녹여내기
   - 참고 자료의 핵심 내용을 자연스럽게 글에 녹여내기

6. **사용자 요청사항**:
   - 사용자가 추가로 입력한 내용이 있다면 반드시 반영

7. **길이**: 
   - 약 1500-2500자 분량
   - 각 섹션에 소제목 포함"""

        # 메시지 구성 (GPT-5 계열은 developer 역할, 그 외는 system 역할)
        model = self.model_var.get()
        role = "developer" if model.startswith("gpt-5") else "system"
        messages = [{"role": role, "content": system_prompt}]
        
        # 사용자 메시지 content 구성
        user_content = []
        
        # 텍스트 프롬프트
        prompt_text = f"다음 키워드에 대한 블로그 글을 작성해주세요.\n\n키워드: {keyword}\n"
        
        if user_additional:
            prompt_text += f"\n===== 사용자 추가 요청 =====\n{user_additional}\n"
        
        prompt_text += "\n요청사항:\n"
        prompt_text += "- 이 키워드와 관련된 핵심 이슈나 트렌드를 분석해주세요\n"
        prompt_text += "- 일반 독자가 이해할 수 있도록 전문 용어는 쉽게 풀어서 설명해주세요\n"
        prompt_text += "- 구체적인 예시나 사례를 포함해주세요\n"
        prompt_text += "- 독자에게 새로운 통찰을 줄 수 있는 관점을 제시해주세요\n"
        
        # 첨부 파일 처리
        text_contents = []
        
        for filepath in self.attached_files:
            file_type = get_file_type(filepath)
            filename = os.path.basename(filepath)
            
            if file_type == "text":
                # 텍스트 파일 읽기
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    text_contents.append(f"\n===== 참고자료: {filename} =====\n{content}\n")
                except Exception as e:
                    text_contents.append(f"\n[파일 읽기 오류: {filename} - {str(e)}]\n")
            
            elif file_type == "image":
                # 이미지 파일
                base64_data = encode_file_to_base64(filepath)
                mime_type = get_mime_type(filepath)
                user_content.append({
                    "type": "text",
                    "text": f"\n[첨부 이미지: {filename}]"
                })
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_data}"
                    }
                })
            
            elif file_type == "pdf":
                # PDF 파일
                base64_data = encode_file_to_base64(filepath)
                user_content.append({
                    "type": "text",
                    "text": f"\n[첨부 PDF: {filename}]"
                })
                user_content.append({
                    "type": "file",
                    "file": {
                        "filename": filename,
                        "file_data": f"data:application/pdf;base64,{base64_data}"
                    }
                })
        
        # 텍스트 참고자료 추가
        if text_contents:
            prompt_text += "\n" + "\n".join(text_contents)
        
        # 최종 사용자 메시지 구성
        user_content.insert(0, {"type": "text", "text": prompt_text})
        
        messages.append({"role": "user", "content": user_content})
        
        # API 호출
        model = self.model_var.get()
        
        # GPT-5 계열은 max_completion_tokens 사용, 그 외는 max_tokens
        if model.startswith("gpt-5"):
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=16000
            )
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=4000
            )
        
        content = response.choices[0].message.content
        if content is None or content.strip() == "":
            raise Exception("API 응답이 비어있습니다.")
        return content
    
    def _on_generation_complete(self, result: str):
        """생성 완료 처리"""
        self.progress_bar.stop()
        self.progress_bar.set(1)
        self.progress_label.configure(text="✅ 생성 완료!")
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", result)
        
        self.generate_btn.configure(state="normal", text="✨ 블로그 글 생성")
        self.save_btn.configure(state="normal")
    
    def _on_generation_error(self, error: str):
        """에러 처리"""
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.progress_label.configure(text="❌ 오류 발생")
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"오류가 발생했습니다:\n{error}")
        
        self.generate_btn.configure(state="normal", text="✨ 블로그 글 생성")
        messagebox.showerror("오류", f"글 생성 중 오류가 발생했습니다:\n{error}")
    
    def save_article(self):
        """블로그 글 저장"""
        content = self.result_textbox.get("1.0", "end").strip()
        
        if not content:
            messagebox.showwarning("저장 실패", "저장할 내용이 없습니다.")
            return
        
        keyword = self.keyword_entry.get().strip() or "article"
        
        # output 폴더 생성
        os.makedirs("output", exist_ok=True)
        
        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_keyword = safe_keyword.replace(' ', '_')[:30]
        
        filename = f"output/{timestamp}_{safe_keyword}.md"
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {keyword}\n\n")
            f.write(f"*생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}*\n\n")
            if self.attached_files:
                f.write("*참고자료:*\n")
                for fp in self.attached_files:
                    f.write(f"- {os.path.basename(fp)}\n")
                f.write("\n")
            f.write("---\n\n")
            f.write(content)
        
        messagebox.showinfo("저장 완료", f"파일이 저장되었습니다:\n{filename}")


if __name__ == "__main__":
    app = ArticleWriterApp()
    app.mainloop()
