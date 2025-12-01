"""
PDF 페이지 추출기
- PDF 파일에서 특정 페이지 범위를 추출하여 새 파일로 저장
- 새 파일명: 원본파일명_YYYYMMDD_HHMMSS.pdf
"""

import os
import sys
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter


def extract_pages(input_path: str, start_page: int, end_page: int) -> str:
    """
    PDF에서 특정 페이지 범위를 추출하여 새 파일로 저장
    
    Args:
        input_path: 입력 PDF 파일 경로
        start_page: 시작 페이지 (1부터 시작)
        end_page: 끝 페이지 (포함)
    
    Returns:
        생성된 파일 경로
    """
    # 파일 존재 확인
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {input_path}")
    
    # PDF 읽기
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    # 페이지 범위 검증
    if start_page < 1:
        raise ValueError("시작 페이지는 1 이상이어야 합니다.")
    if end_page > total_pages:
        raise ValueError(f"끝 페이지가 전체 페이지 수({total_pages})를 초과합니다.")
    if start_page > end_page:
        raise ValueError("시작 페이지가 끝 페이지보다 클 수 없습니다.")
    
    # 페이지 추출
    writer = PdfWriter()
    for page_num in range(start_page - 1, end_page):  # 0-indexed
        writer.add_page(reader.pages[page_num])
    
    # 출력 파일명 생성 (원본파일명_날짜시간.pdf)
    dir_name = os.path.dirname(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = f"{base_name}_{timestamp}.pdf"
    output_path = os.path.join(dir_name, output_name) if dir_name else output_name
    
    # 파일 저장
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
    
    return output_path


def main():
    print("=" * 50)
    print("       PDF 페이지 추출기")
    print("=" * 50)
    print()
    
    # PDF 파일 경로 입력
    while True:
        input_path = input("PDF 파일 경로를 입력하세요: ").strip()
        # 따옴표 제거 (드래그 앤 드롭 시 추가될 수 있음)
        input_path = input_path.strip('"').strip("'")
        
        if not input_path:
            print("❌ 파일 경로를 입력해주세요.\n")
            continue
        
        if not os.path.exists(input_path):
            print(f"❌ 파일을 찾을 수 없습니다: {input_path}\n")
            continue
        
        if not input_path.lower().endswith('.pdf'):
            print("❌ PDF 파일만 처리할 수 있습니다.\n")
            continue
        
        break
    
    # PDF 정보 표시
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        print(f"\n📄 파일: {os.path.basename(input_path)}")
        print(f"📑 전체 페이지 수: {total_pages}")
        print()
    except Exception as e:
        print(f"❌ PDF 파일을 읽는 중 오류가 발생했습니다: {e}")
        input("\n아무 키나 눌러 종료하세요...")
        sys.exit(1)
    
    # 페이지 범위 입력
    while True:
        try:
            page_range = input("추출할 페이지 범위를 입력하세요 (예: 1-5 또는 3): ").strip()
            
            if '-' in page_range:
                parts = page_range.split('-')
                start_page = int(parts[0].strip())
                end_page = int(parts[1].strip())
            else:
                start_page = end_page = int(page_range)
            
            if start_page < 1 or end_page < 1:
                print("❌ 페이지 번호는 1 이상이어야 합니다.\n")
                continue
            
            if start_page > end_page:
                print("❌ 시작 페이지가 끝 페이지보다 클 수 없습니다.\n")
                continue
            
            if end_page > total_pages:
                print(f"❌ 끝 페이지가 전체 페이지 수({total_pages})를 초과합니다.\n")
                continue
            
            break
        except ValueError:
            print("❌ 올바른 형식으로 입력해주세요. (예: 1-5 또는 3)\n")
    
    # 페이지 추출 실행
    print()
    print(f"🔄 {start_page}~{end_page} 페이지를 추출하는 중...")
    
    try:
        output_path = extract_pages(input_path, start_page, end_page)
        print()
        print("✅ 추출 완료!")
        print(f"📁 저장 위치: {output_path}")
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
    
    print()
    input("아무 키나 눌러 종료하세요...")


if __name__ == "__main__":
    main()


