# 메모 앱

Next.js와 Prisma를 사용한 메모 관리 애플리케이션입니다.

## 기능

- ✅ 회원가입/로그인/로그아웃
- ✅ 사용자별 메모 작성 및 관리
- ✅ 메모 검색
- ✅ 메모 색상 커스터마이징

## 로컬 개발

```bash
# 의존성 설치
npm install

# 데이터베이스 마이그레이션
npx prisma db push

# 개발 서버 실행
npm run dev
```

## Vercel 배포

### 방법 1: Vercel CLI 사용

```bash
# Vercel CLI 설치
npm i -g vercel

# 배포
vercel

# 프로덕션 배포
vercel --prod
```

### 방법 2: GitHub 연동

1. GitHub에 코드 푸시
2. [Vercel](https://vercel.com)에 로그인
3. "Add New Project" 클릭
4. GitHub 저장소 선택
5. 환경 변수 설정:
   - `DATABASE_URL`: 데이터베이스 연결 문자열
6. "Deploy" 클릭

## 환경 변수

`.env` 파일에 다음 변수를 설정하세요:

```
DATABASE_URL="file:./dev.db"  # 로컬 개발용
# 또는
DATABASE_URL="postgresql://..."  # Vercel 배포용 (PostgreSQL)
```

## 데이터베이스

로컬 개발: SQLite 사용
Vercel 배포: PostgreSQL 권장 (Vercel Postgres 또는 외부 서비스 사용)

## 기술 스택

- Next.js 16
- React 19
- Prisma 6
- TypeScript
- Tailwind CSS
- bcryptjs (비밀번호 해싱)
