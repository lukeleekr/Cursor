"""
키워드 기반 분석 칼럼 생성기
OpenAI GPT-5-nano를 활용한 전문적이면서도 쉽게 읽히는 칼럼 작성
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_column(keyword: str) -> str:
    """
    주어진 키워드를 바탕으로 분석적 칼럼을 생성합니다.
    
    Args:
        keyword: 칼럼의 주제가 될 키워드
    
    Returns:
        생성된 칼럼 텍스트
    """
    
    system_prompt = """당신은 10년 경력의 전문 칼럼니스트입니다. 
복잡한 주제를 일반 독자들이 이해하기 쉽게 설명하는 능력이 뛰어납니다.

칼럼 작성 시 다음 원칙을 따르세요:

1. **구조**: 
   - 흥미로운 도입부로 시작
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

5. **길이**: 
   - 약 1500-2000자 분량
   - 각 섹션에 소제목 포함"""

    user_prompt = f"""다음 키워드에 대한 분석적 칼럼을 작성해주세요.

키워드: {keyword}

요청사항:
- 이 키워드와 관련된 핵심 이슈나 트렌드를 분석해주세요
- 일반 독자가 이해할 수 있도록 전문 용어는 쉽게 풀어서 설명해주세요
- 구체적인 예시나 사례를 포함해주세요
- 독자에게 새로운 통찰을 줄 수 있는 관점을 제시해주세요"""

    try:
        # GPT-5-nano는 reasoning 모델이므로 developer 역할 사용
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_completion_tokens=16000
        )
        
        # 디버깅: 전체 응답 출력
        print("\n[DEBUG] 전체 응답:")
        print(response)
        print()
        
        # 응답 내용 확인
        content = response.choices[0].message.content
        if content is None or content.strip() == "":
            return f"오류: API 응답이 비어있습니다.\n응답 객체: {response.choices[0]}"
        return content
    
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"


def save_column(keyword: str, content: str) -> str:
    """
    생성된 칼럼을 파일로 저장합니다.
    
    Args:
        keyword: 칼럼 키워드
        content: 칼럼 내용
    
    Returns:
        저장된 파일 경로
    """
    # output 폴더 생성
    os.makedirs("output", exist_ok=True)
    
    # 파일명 생성 (날짜_키워드.md)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 파일명에 사용할 수 없는 문자 제거
    safe_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_keyword = safe_keyword.replace(' ', '_')[:30]  # 최대 30자
    
    filename = f"output/{timestamp}_{safe_keyword}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {keyword}\n\n")
        f.write(f"*생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}*\n\n")
        f.write("---\n\n")
        f.write(content)
    
    return filename


def main():
    print("=" * 60)
    print("📝 AI 분석 칼럼 생성기")
    print("=" * 60)
    print()
    
    # 키워드 입력
    keyword = input("칼럼 주제 키워드를 입력하세요: ").strip()
    
    if not keyword:
        print("❌ 키워드를 입력해주세요.")
        return
    
    print()
    print(f"🔍 '{keyword}'에 대한 칼럼을 생성 중입니다...")
    print("   (약 30초~1분 소요될 수 있습니다)")
    print()
    
    # 칼럼 생성
    column = generate_column(keyword)
    
    if column.startswith("오류가"):
        print(column)
        return
    
    # 결과 출력
    print("=" * 60)
    print("📄 생성된 칼럼")
    print("=" * 60)
    print()
    print(column)
    print()
    
    # 저장 여부 확인
    save_choice = input("💾 칼럼을 파일로 저장하시겠습니까? (y/n): ").strip().lower()
    
    if save_choice == 'y':
        filepath = save_column(keyword, column)
        print(f"✅ 저장 완료: {filepath}")
    
    print()
    print("감사합니다! 🙏")


if __name__ == "__main__":
    main()

