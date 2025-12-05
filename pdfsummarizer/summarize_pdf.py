"""
PDF 요약 프로그램
추출된 텍스트를 OpenAI GPT API로 요약합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import fitz  # PyMuPDF

# .env 파일에서 환경변수 로드
load_dotenv()

# OpenAI 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(pdf_path: str) -> str:
    """PDF 파일에서 텍스트를 추출합니다."""
    text_content = []
    
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_content.append(text)
        doc.close()
    except Exception as e:
        return f"오류 발생: {str(e)}"
    
    return "\n".join(text_content)


def summarize_text(text: str, filename: str) -> str:
    """
    텍스트를 GPT API로 요약합니다.
    
    Args:
        text: 요약할 텍스트
        filename: 파일명 (컨텍스트 제공용)
        
    Returns:
        요약된 텍스트
    """
    # 텍스트가 너무 길면 앞부분만 사용 (토큰 제한 고려)
    max_chars = 100000  # 약 25,000 토큰
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n... (텍스트가 길어 일부만 요약)"
    
    prompt = f"""다음은 PDF 문서 "{filename}"에서 추출한 텍스트입니다.

이 내용을 다음 형식으로 요약해주세요:

## 📋 문서 개요
(문서가 무엇에 관한 것인지 1-2문장으로)

## 🔑 핵심 내용
(주요 포인트를 bullet point로 정리)

## 💡 주요 인사이트
(문서에서 얻을 수 있는 중요한 통찰이나 결론)

---

문서 내용:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 문서 요약 전문가입니다. 핵심을 파악하고 명확하게 요약해주세요. 한국어로 답변합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # 일관성 있는 요약을 위해 낮은 온도
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"요약 중 오류 발생: {str(e)}"


def summarize_all_pdfs(folder_path: str = ".") -> dict:
    """
    폴더 내 모든 PDF 파일을 요약합니다.
    
    Args:
        folder_path: PDF 파일이 있는 폴더 경로
        
    Returns:
        {파일명: 요약} 형태의 딕셔너리
    """
    results = {}
    folder = Path(folder_path)
    pdf_files = list(folder.glob("*.pdf"))
    
    if not pdf_files:
        print("PDF 파일을 찾을 수 없습니다.")
        return results
    
    print(f"총 {len(pdf_files)}개의 PDF 파일을 발견했습니다.\n")
    
    for i, pdf_file in enumerate(sorted(pdf_files), 1):
        print(f"[{i}/{len(pdf_files)}] 처리 중: {pdf_file.name}")
        
        # 텍스트 추출
        print("  - 텍스트 추출 중...")
        text = extract_text_from_pdf(str(pdf_file))
        
        if text.startswith("오류"):
            print(f"  - ❌ {text}")
            results[pdf_file.name] = text
            continue
        
        # GPT로 요약
        print("  - GPT로 요약 중...")
        summary = summarize_text(text, pdf_file.name)
        results[pdf_file.name] = summary
        print("  - ✅ 완료!")
        print()
    
    return results


def save_summaries(results: dict, output_folder: str = "summaries"):
    """
    요약 결과를 파일로 저장합니다.
    
    Args:
        results: {파일명: 요약} 딕셔너리
        output_folder: 출력 폴더명
    """
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)
    
    for filename, summary in results.items():
        output_file = output_path / f"{Path(filename).stem}_요약.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"원본 파일: {filename}\n")
            f.write("=" * 60 + "\n\n")
            f.write(summary)
        print(f"저장됨: {output_file}")
    
    # 전체 요약을 하나의 파일로도 저장
    all_summaries_file = output_path / "_전체_요약.txt"
    with open(all_summaries_file, "w", encoding="utf-8") as f:
        f.write("PDF 문서 전체 요약\n")
        f.write("=" * 60 + "\n\n")
        
        for filename, summary in results.items():
            f.write(f"📄 {filename}\n")
            f.write("-" * 60 + "\n")
            f.write(summary)
            f.write("\n\n" + "=" * 60 + "\n\n")
    
    print(f"\n전체 요약 저장됨: {all_summaries_file}")


def main():
    print("=" * 60)
    print("📚 PDF 요약 프로그램 (GPT-4o-mini)")
    print("=" * 60)
    print()
    
    # API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 오류: OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")
        print("   .env 파일에 다음과 같이 추가해주세요:")
        print("   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx")
        return
    
    print("✅ API 키 확인됨\n")
    
    # PDF 요약 실행
    results = summarize_all_pdfs(".")
    
    if not results:
        return
    
    print()
    print("-" * 60)
    
    # 결과 저장
    save_summaries(results)
    
    print()
    print("=" * 60)
    print("✅ 요약 완료! 'summaries' 폴더에서 결과를 확인하세요.")
    print("=" * 60)


if __name__ == "__main__":
    main()

