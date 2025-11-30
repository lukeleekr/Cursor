# Neon 프로젝트 생성 및 DATABASE_URL 얻기

## 방법 1: 웹에서 직접 생성 (추천)

1. **Neon 대시보드 접속**
   - https://console.neon.tech 접속
   - 로그인 (이미 인증 완료됨)

2. **프로젝트 생성**
   - "Create a project" 또는 "New Project" 클릭
   - 프로젝트 이름: `memo-app`
   - Region: `Seoul (ap-northeast-2)` 또는 `Tokyo (ap-northeast-1)` 선택
   - "Create Project" 클릭

3. **DATABASE_URL 복사**
   - 프로젝트 대시보드에서 "Connection Details" 섹션 찾기
   - "Connection string" 또는 "Postgres connection string" 복사
   - 예시: `postgresql://user:password@ep-xxx-xxx.region.aws.neon.tech/neondb?sslmode=require`

## 방법 2: CLI로 생성 (대화형)

터미널에서 다음 명령어 실행:
```bash
npx neonctl@latest projects create --name memo-app
```

질문에 답변:
- Organization: Luke 선택
- Use as default: Y (Enter)

## DATABASE_URL을 얻은 후

1. `.env` 파일에 추가 (로컬 개발용)
2. Vercel 환경 변수에 추가 (배포용)
3. Prisma 스키마를 PostgreSQL로 변경

