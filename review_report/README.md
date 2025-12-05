# 고객 리뷰 데이터 보고서 생성기

엑셀 파일의 고객 리뷰 데이터를 분석하여 Markdown 형식의 보고서를 자동으로 생성하는 프로그램입니다. OpenAI API를 활용한 고급 감정 분석 및 리뷰 요약 기능을 제공합니다.

## 주요 기능

- **리뷰 컬럼 자동 감지**: 컬럼명의 키워드를 기반으로 리뷰 컬럼을 자동으로 찾습니다
- **기본 통계 분석**: 평점 분포, 평균 평점, 모델별 통계 등
- **OpenAI API 기반 감정 분석**: 리뷰 텍스트를 분석하여 긍정/부정/중립으로 분류
- **리뷰 요약**: OpenAI API를 활용한 각 리뷰의 핵심 내용 요약
- **Markdown 보고서**: 깔끔하고 읽기 쉬운 Markdown 형식의 보고서 생성

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. `.env` 파일 생성 및 OpenAI API 키 설정:
```bash
OPENAI_API_KEY=your_api_key_here
```

## 사용 방법

### 방법 1: GUI 프로그램 사용 (가장 간단, 추천)

Windows에서 GUI 프로그램을 실행합니다:

```bash
python gui_app.py
```

또는 배치 파일 사용:
```bash
run_gui.bat
```

GUI에서:
1. "파일 선택" 버튼을 클릭하여 Excel 파일 선택
2. (선택사항) "폴더 선택" 버튼으로 저장 위치 지정
3. "분석 시작" 버튼 클릭
4. 분석 완료 후 "보고서 열기" 버튼으로 결과 확인

### 방법 2: 배치 파일 사용 (Windows, 간단)

Windows에서는 배치 파일을 사용하면 가장 쉽습니다:

```bash
# 엑셀 파일을 run.bat에 드래그 앤 드롭하거나
run.bat "노트북 고객 리뷰 데이터.xlsx"
```

### 방법 2: 명령줄에서 실행

```bash
# 기본 사용법
python review_report_generator.py "노트북 고객 리뷰 데이터.xlsx"

# 출력 디렉토리 지정
python review_report_generator.py "데이터.xlsx" --output reports

# 리뷰 컬럼 수동 지정
python review_report_generator.py "데이터.xlsx" --review-column "리뷰내용"

# 모든 옵션 보기
python review_report_generator.py --help
```

### 방법 3: 간단한 실행 스크립트 사용

```bash
# 파일 경로 입력 대화상자 표시
python run.py

# 또는 명령줄에서 파일 경로 지정
python run.py "노트북 고객 리뷰 데이터.xlsx"
```

### 방법 4: Linux/Mac에서 실행

```bash
# 실행 권한 부여 (최초 1회)
chmod +x run.sh

# 실행
./run.sh "노트북 고객 리뷰 데이터.xlsx"
```

### 방법 3: Python 코드에서 사용

```python
from review_report_generator import ReviewReportGenerator

# 보고서 생성기 초기화
generator = ReviewReportGenerator('노트북 고객 리뷰 데이터.xlsx')

# Markdown 보고서 생성
report_file = generator.generate_report()
print(f"생성된 보고서: {report_file}")
```

### 리뷰 컬럼 수동 지정

리뷰 컬럼을 자동으로 찾지 못한 경우, 수동으로 지정할 수 있습니다:

```bash
python review_report_generator.py "데이터.xlsx" --review-column "리뷰내용"
```

또는 Python 코드에서:

```python
generator.detect_review_column(manual_column='리뷰내용')
generator.analyze()
generator.generate_report()
```

## 파일 구조

```
review_report/
├── gui_app.py                  # GUI 프로그램 (추천)
├── run_gui.bat                 # GUI 실행 배치 파일
├── review_report_generator.py  # 메인 프로그램 (CLI 포함)
├── run.py                      # 간단한 실행 스크립트 (Python)
├── run.bat                     # Windows 배치 파일
├── run.sh                      # Linux/Mac 실행 스크립트
├── column_detector.py          # 리뷰 컬럼 자동 감지 모듈
├── analyzer.py                 # 데이터 분석 모듈 (OpenAI API 활용)
├── report_generator.py         # Markdown/HTML 보고서 생성 모듈
├── requirements.txt            # 필요한 패키지 목록
├── .env                        # OpenAI API 키 설정 파일
└── README.md                   # 이 파일
```

## 리뷰 컬럼 자동 감지

프로그램은 다음 키워드를 포함한 컬럼명을 자동으로 찾습니다:

1. **우선순위 1**: "리뷰", "review"
2. **우선순위 2**: "comment", "댓글"
3. **우선순위 3**: "내용", "content", "text", "텍스트"
4. **우선순위 4**: "의견", "opinion", "feedback"
5. **우선순위 5**: "평가", "evaluation", "assessment"

키워드로 찾지 못한 경우, 텍스트가 가장 긴 컬럼을 후보로 고려합니다.

## 보고서 내용

생성되는 보고서에는 다음 내용이 포함됩니다:

- **기본 통계**: 총 리뷰 수, 평균 평점, 평점 분포 등
- **감정 분석**: OpenAI API를 활용한 긍정/부정/중립 리뷰 비율
- **키워드 기반 분석**: 
  - 긍정 리뷰에서 자주 언급된 키워드와 관련 리뷰
  - 부정 리뷰에서 자주 언급된 키워드와 관련 리뷰
  - HTML 보고서에서는 키워드를 클릭하면 관련 리뷰 원문 확인 가능
- **모델별 통계**: 노트북 모델별 평균 평점 및 리뷰 수 (해당 컬럼이 있는 경우)
- **연령대/성별 분석**: 고객 특성별 통계 (해당 컬럼이 있는 경우)

### 보고서 형식

- **Markdown (.md)**: 텍스트 기반 보고서, 모든 정보 포함
- **HTML (.html)**: 인터랙티브 보고서, 키워드 클릭 시 관련 리뷰 표시

## 요구사항

- Python 3.7 이상
- pandas
- openpyxl
- openai
- python-dotenv

## OpenAI API 사용

이 프로그램은 OpenAI API를 사용하여 리뷰의 감정을 분석하고 요약합니다. 

- **모델**: 기본적으로 `gpt-4o-mini`를 사용합니다 (비용 효율적)
- **API 키**: `.env` 파일에 `OPENAI_API_KEY`를 설정해야 합니다
- **비용**: 리뷰 수에 따라 API 호출 비용이 발생합니다

## 주의사항

- OpenAI API 호출에는 비용이 발생할 수 있습니다
- 대량의 리뷰를 분석할 경우 시간이 소요될 수 있습니다
- API 호출 제한을 고려하여 배치 처리 방식을 사용합니다

## 라이선스

이 프로젝트는 자유롭게 사용할 수 있습니다.
