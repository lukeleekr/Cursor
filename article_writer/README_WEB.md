# AI 칼럼 생성기 (Web 버전)

Next.js + shadcn/ui 기반의 웹 애플리케이션입니다.

## 🚀 시작하기

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

`.env.local` 파일을 생성하고 OpenAI API 키를 추가하세요:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

## 📦 기능

- ✅ 키워드 기반 칼럼 생성
- ✅ 다중 파일 첨부 (이미지, PDF, 텍스트)
- ✅ 사용자 직접 입력
- ✅ 모델 선택 (GPT-5-nano, GPT-5-mini, GPT-5, GPT-4o, GPT-4o-mini)
- ✅ 실시간 진행률 표시
- ✅ 결과 다운로드 (Markdown)

## 🛠️ 기술 스택

- **Framework**: Next.js 14
- **UI**: shadcn/ui (Radix UI + Tailwind CSS)
- **API**: OpenAI API
- **Language**: TypeScript

## 📝 사용 방법

1. 키워드 입력
2. (선택) 참고자료 파일 첨부
3. (선택) 추가 내용 직접 입력
4. 모델 선택
5. "칼럼 생성" 버튼 클릭
6. 생성된 칼럼 확인 및 다운로드

## 🔧 빌드

```bash
npm run build
npm start
```




