# 웹 스크래핑 프로젝트

Yahoo Finance와 한국금거래소에서 금융 데이터를 스크래핑하고 분석하는 Python 프로젝트입니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [필수 요구사항](#필수-요구사항)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
  - [주식 상승 종목 스크래핑](#1-주식-상승-종목-스크래핑)
  - [금시세 스크래핑](#2-금시세-스크래핑)
  - [금시세 분석](#3-금시세-분석)
  - [금시세 시각화](#4-금시세-시각화)
- [출력 파일](#출력-파일)
- [주의사항](#주의사항)
- [문제 해결](#문제-해결)

---

## 📖 프로젝트 개요

이 프로젝트는 다음과 같은 기능을 제공합니다:

1. **주식 상승 종목 스크래핑**: Yahoo Finance에서 상승률이 높은 주식 종목을 수집
2. **금시세 스크래핑**: 한국금거래소에서 실시간 금 시세 데이터 수집
3. **금시세 분석**: 수집된 금시세 데이터의 통계 분석
4. **금시세 시각화**: 금시세 데이터를 그래프로 시각화

---

## 🔧 필수 요구사항

- **Python 3.8 이상**
- **Google Chrome 브라우저** (Selenium WebDriver 사용)
- **인터넷 연결**

---

## 📦 설치 방법

### 1. 저장소 클론 또는 다운로드

```bash
git clone <repository-url>
cd crawling
```

### 2. 필요한 패키지 설치

```bash
pip install selenium webdriver-manager pandas openpyxl matplotlib
```

또는 requirements.txt가 있다면:

```bash
pip install -r requirements.txt
```

### 설치되는 주요 패키지:

- **selenium**: 웹 브라우저 자동화
- **webdriver-manager**: Chrome 드라이버 자동 관리
- **pandas**: 데이터 처리 및 분석
- **openpyxl**: 엑셀 파일 읽기/쓰기
- **matplotlib**: 데이터 시각화

---

## 🚀 사용 방법

### 1. 주식 상승 종목 스크래핑

Yahoo Finance에서 상승률이 높은 주식 종목을 스크래핑합니다.

```bash
python scrape_stock_gainers.py
```

#### 기능:
- Yahoo Finance의 "Top Stock Gainers" 페이지에서 데이터 수집
- 기본적으로 **50개 종목** 수집 (코드에서 변경 가능)
- 자동으로 페이지네이션 처리
- 엑셀 파일로 자동 저장

#### 출력 파일:
- `주식상승종목_YYYYMMDD_HHMMSS.xlsx`

#### 포함 데이터:
- Symbol (종목 심볼)
- Company Name (회사명)
- Price (현재가)
- Change (변동액)
- Change % (변동률)
- Volume (거래량)
- Avg Volume (평균 거래량)
- Market Cap (시가총액)
- P/E Ratio (PER)
- YTD Change % (연초 대비 변동률)
- 52 Week Low/High (52주 최저가/최고가)

#### 커스터마이징:

스크립트 내에서 수집할 종목 수를 변경할 수 있습니다:

```python
# scrape_stock_gainers.py의 main() 함수에서
data = scrape_stock_gainers(target_count=100)  # 100개로 변경
```

---

### 2. 금시세 스크래핑

한국금거래소에서 실시간 금 시세를 스크래핑합니다.

```bash
python scrape_gold_price.py
```

#### 기능:
- 한국금거래소 웹사이트에서 금 시세 데이터 수집
- 구매가, 판매가 등 다양한 가격 정보 수집
- 엑셀 파일로 자동 저장

#### 출력 파일:
- `금시세_YYYYMMDD_HHMMSS.xlsx`

---

### 3. 금시세 분석

스크래핑한 금시세 데이터를 분석하여 통계값을 계산합니다.

```bash
python analyze_gold_price.py
```

또는 스크립트 내에서 파일명을 지정:

```python
# analyze_gold_price.py 수정
excel_file = "금시세_20251129_233831.xlsx"
analyze_gold_prices(excel_file)
```

#### 기능:
- 평균, 최대, 최소 가격 계산
- 표준편차, 중앙값 등 통계값 계산
- 분석 결과를 별도 엑셀 파일로 저장

#### 출력 파일:
- `금시세_YYYYMMDD_HHMMSS_통계분석.xlsx`

---

### 4. 금시세 시각화

금시세 데이터를 그래프로 시각화합니다.

```bash
python visualize_gold_price.py
```

또는 스크립트 내에서 파일명을 지정:

```python
# visualize_gold_price.py 수정
excel_file = "금시세_20251129_233831.xlsx"
visualize_gold_prices(excel_file)
```

#### 생성되는 그래프:
1. `1_시계열_추이.png` - 시간에 따른 가격 추이
2. `2_구매가_판매가_비교.png` - 구매가와 판매가 비교
3. `3_가격_분포_박스플롯.png` - 가격 분포 박스플롯
4. `4_가격_분포_히스토그램.png` - 가격 분포 히스토그램
5. `5_평균_가격_비교.png` - 평균 가격 비교
6. `6_구매가_판매가_산점도.png` - 구매가와 판매가 산점도
7. `7_통계_요약.png` - 통계 요약 그래프

---

## 📁 출력 파일

### 주식 상승 종목 스크래핑
```
주식상승종목_YYYYMMDD_HHMMSS.xlsx
```

### 금시세 관련
```
금시세_YYYYMMDD_HHMMSS.xlsx                    # 원본 데이터
금시세_YYYYMMDD_HHMMSS_통계분석.xlsx           # 분석 결과
1_시계열_추이.png ~ 7_통계_요약.png            # 시각화 그래프
```

---

## ⚠️ 주의사항

### 1. 웹사이트 이용 약관 준수
- 웹사이트의 이용 약관을 확인하고 준수하세요
- 과도한 요청은 IP 차단을 유발할 수 있습니다
- 적절한 딜레이를 두고 사용하세요

### 2. 데이터 정확성
- 스크래핑된 데이터는 참고용입니다
- 투자 결정 시 공식 데이터를 확인하세요
- 웹사이트 구조 변경 시 스크립트 수정이 필요할 수 있습니다

### 3. Chrome 드라이버
- Chrome 브라우저가 설치되어 있어야 합니다
- `webdriver-manager`가 자동으로 드라이버를 관리하지만, 수동 설치가 필요할 수 있습니다

### 4. 헤드리스 모드
- 기본적으로 헤드리스 모드(브라우저 창 없이 실행)로 동작합니다
- 디버깅이 필요하면 `--headless` 옵션을 제거하세요

---

## 🔍 문제 해결

### Chrome 드라이버 오류

**문제**: `selenium.common.exceptions.WebDriverException`

**해결**:
```bash
# Chrome 브라우저가 최신 버전인지 확인
# webdriver-manager가 자동으로 관리하지만, 수동 설치가 필요할 수 있습니다
```

### 페이지 로딩 오류

**문제**: 테이블을 찾을 수 없음

**해결**:
- 인터넷 연결 확인
- 웹사이트가 정상 작동하는지 확인
- 스크립트의 대기 시간(`time.sleep()`) 증가

### 엑셀 파일 저장 오류

**문제**: `PermissionError` 또는 파일이 열려있음

**해결**:
- 엑셀 파일이 다른 프로그램에서 열려있지 않은지 확인
- 파일 권한 확인

### 데이터가 수집되지 않음

**문제**: 스크래핑은 성공했지만 데이터가 비어있음

**해결**:
- 웹사이트 구조가 변경되었을 수 있음
- CSS 선택자나 XPath 확인 필요
- 브라우저 개발자 도구로 요소 확인

---

## 📝 코드 구조

```
crawling/
├── scrape_stock_gainers.py    # 주식 상승 종목 스크래핑
├── scrape_gold_price.py        # 금시세 스크래핑
├── analyze_gold_price.py      # 금시세 분석
├── visualize_gold_price.py    # 금시세 시각화
└── README.md                   # 이 파일
```

---

## 🔄 업데이트 이력

### 2025-11-30
- 주식 상승 종목 스크래핑 기능 추가
- 페이지네이션 자동 처리 기능 추가
- 엑셀 파일 포맷팅 개선

---

## 📞 문의

문제가 발생하거나 개선 사항이 있으면 이슈를 등록해주세요.

---

## 📄 라이선스

이 프로젝트는 개인 사용 목적으로 제작되었습니다. 상업적 사용 시 해당 웹사이트의 이용 약관을 확인하세요.

---

## 🙏 감사의 말

- Yahoo Finance
- 한국금거래소
- Selenium, Pandas, Matplotlib 커뮤니티

