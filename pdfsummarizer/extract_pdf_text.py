"""
PDF 텍스트 추출 프로그램
현재 폴더에 있는 모든 PDF 파일에서 텍스트를 추출합니다.
"""

import fitz  # PyMuPDF
import os
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    PDF 파일에서 텍스트를 추출합니다.
    
    Args:
        pdf_path: PDF 파일 경로
        
    Returns:
        추출된 텍스트
    """
    text_content = []
    
    try:
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            if text.strip():
                text_content.append(f"--- 페이지 {page_num + 1} ---")
                text_content.append(text)
        
        doc.close()
        
    except Exception as e:
        return f"오류 발생: {str(e)}"
    
    return "\n".join(text_content)


def extract_all_pdfs(folder_path: str = ".") -> dict:
    """
    폴더 내 모든 PDF 파일에서 텍스트를 추출합니다.
    
    Args:
        folder_path: 검색할 폴더 경로 (기본값: 현재 폴더)
        
    Returns:
        {파일명: 추출된 텍스트} 형태의 딕셔너리
    """
    results = {}
    folder = Path(folder_path)
    
    pdf_files = list(folder.glob("*.pdf"))
    
    if not pdf_files:
        print("PDF 파일을 찾을 수 없습니다.")
        return results
    
    print(f"총 {len(pdf_files)}개의 PDF 파일을 발견했습니다.\n")
    
    for pdf_file in sorted(pdf_files):
        print(f"처리 중: {pdf_file.name}")
        text = extract_text_from_pdf(str(pdf_file))
        results[pdf_file.name] = text
    
    return results


def save_extracted_text(results: dict, output_folder: str = "extracted_texts"):
    """
    추출된 텍스트를 파일로 저장합니다.
    
    Args:
        results: {파일명: 텍스트} 딕셔너리
        output_folder: 출력 폴더명
    """
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)
    
    for filename, text in results.items():
        output_file = output_path / f"{Path(filename).stem}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"저장됨: {output_file}")


def main():
    print("=" * 60)
    print("PDF 텍스트 추출 프로그램")
    print("=" * 60)
    print()
    
    # 현재 폴더의 PDF 파일들에서 텍스트 추출
    results = extract_all_pdfs(".")
    
    if not results:
        return
    
    print()
    print("-" * 60)
    
    # 결과를 텍스트 파일로 저장
    save_extracted_text(results)
    
    print()
    print("-" * 60)
    print()
    
    # 콘솔에 결과 출력
    for filename, text in results.items():
        print(f"\n{'=' * 60}")
        print(f"파일: {filename}")
        print("=" * 60)
        print(text[:2000] if len(text) > 2000 else text)  # 처음 2000자만 출력
        if len(text) > 2000:
            print(f"\n... (총 {len(text)}자, 나머지는 저장된 파일에서 확인)")
    
    print()
    print("=" * 60)
    print("추출 완료! 'extracted_texts' 폴더에서 전체 내용을 확인하세요.")
    print("=" * 60)


if __name__ == "__main__":
    main()

