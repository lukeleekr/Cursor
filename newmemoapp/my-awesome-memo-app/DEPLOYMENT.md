# Vercel 배포 가이드 - DATABASE_URL 설정 방법

## DATABASE_URL이란?

데이터베이스 연결을 위한 URL 문자열입니다. PostgreSQL의 경우 다음과 같은 형식입니다:

```
postgresql://사용자명:비밀번호@호스트:포트/데이터베이스명?sslmode=require
```

## 방법 1: Vercel Postgres 사용 (가장 쉬움) ⭐

### 단계:

1. **Vercel 대시보드 접속**
   - https://vercel.com 접속
   - 로그인

2. **프로젝트 생성 후 Storage 추가**
   - 프로젝트 선택 (또는 새로 생성)
   - 상단 메뉴에서 **"Storage"** 탭 클릭
   - **"Create Database"** 클릭
   - **"Postgres"** 선택
   - 데이터베이스 이름 입력 후 생성

3. **DATABASE_URL 자동 설정**
   - Vercel Postgres를 사용하면 자동으로 환경 변수가 설정됩니다
   - `POSTGRES_URL` 또는 `DATABASE_URL`이 자동으로 생성됩니다
   - 별도로 복사할 필요 없음!

4. **환경 변수 확인**
   - 프로젝트 설정 → Environment Variables에서 확인 가능

---

## 방법 2: Neon 사용 (무료, 추천) ⭐⭐

### 단계:

1. **Neon 계정 생성**
   - https://neon.tech 접속
   - GitHub로 로그인 (또는 이메일)

2. **프로젝트 생성**
   - "Create a project" 클릭
   - 프로젝트 이름 입력
   - 데이터베이스 이름 입력 (기본값: `neondb`)
   - Region 선택 (가장 가까운 지역)
   - "Create Project" 클릭

3. **DATABASE_URL 복사**
   - 프로젝트 대시보드에서 **"Connection Details"** 섹션 확인
   - **"Connection string"** 또는 **"Postgres connection string"** 찾기
   - 형식: `postgresql://사용자명:비밀번호@호스트/데이터베이스명?sslmode=require`
   - **복사 버튼** 클릭하여 전체 URL 복사

4. **Vercel에 환경 변수 추가**
   - Vercel 프로젝트 설정 → Environment Variables
   - Key: `DATABASE_URL`
   - Value: 복사한 연결 문자열 붙여넣기
   - Environment: Production, Preview, Development 모두 선택
   - "Save" 클릭

---

## 방법 3: Supabase 사용 (무료)

### 단계:

1. **Supabase 계정 생성**
   - https://supabase.com 접속
   - GitHub로 로그인

2. **프로젝트 생성**
   - "New Project" 클릭
   - Organization 선택
   - 프로젝트 이름 입력
   - 데이터베이스 비밀번호 설정
   - Region 선택
   - "Create new project" 클릭

3. **DATABASE_URL 찾기**
   - 프로젝트 대시보드에서 왼쪽 메뉴 **"Settings"** 클릭
   - **"Database"** 선택
   - **"Connection string"** 섹션에서 **"URI"** 탭 선택
   - 연결 문자열 복사 (비밀번호 부분은 `[YOUR-PASSWORD]`로 표시됨)
   - 실제 비밀번호로 교체 필요

4. **비밀번호 교체**
   - 복사한 URL에서 `[YOUR-PASSWORD]`를 프로젝트 생성 시 설정한 비밀번호로 교체

5. **Vercel에 환경 변수 추가**
   - Vercel 프로젝트 설정 → Environment Variables
   - Key: `DATABASE_URL`
   - Value: 비밀번호가 교체된 연결 문자열
   - Environment: Production, Preview, Development 모두 선택
   - "Save" 클릭

---

## 방법 4: Railway 사용 (무료)

### 단계:

1. **Railway 계정 생성**
   - https://railway.app 접속
   - GitHub로 로그인

2. **PostgreSQL 생성**
   - "New Project" 클릭
   - "New" → "Database" → "Add PostgreSQL" 선택

3. **DATABASE_URL 복사**
   - PostgreSQL 서비스 클릭
   - "Variables" 탭에서 `DATABASE_URL` 찾기
   - 값 복사

4. **Vercel에 환경 변수 추가**
   - Vercel 프로젝트 설정 → Environment Variables
   - Key: `DATABASE_URL`
   - Value: 복사한 값
   - Environment: Production, Preview, Development 모두 선택
   - "Save" 클릭

---

## DATABASE_URL 예시

### Neon 예시:
```
postgresql://user:password@ep-xxx-xxx.region.aws.neon.tech/neondb?sslmode=require
```

### Supabase 예시:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

### Vercel Postgres 예시:
```
postgres://default:password@ep-xxx-xxx.region.postgres.vercel-storage.com:5432/verceldb
```

---

## 주의사항

1. **비밀번호 보안**
   - DATABASE_URL에는 비밀번호가 포함되어 있으므로 절대 공개하지 마세요
   - GitHub에 커밋하지 마세요 (`.env` 파일은 `.gitignore`에 포함되어 있음)

2. **환경별 설정**
   - Production, Preview, Development 환경에 각각 설정 가능
   - 개발 환경과 프로덕션 환경을 분리하는 것을 권장

3. **SSL 모드**
   - 대부분의 클라우드 데이터베이스는 `?sslmode=require` 필요
   - 연결 문자열에 포함되어 있는지 확인

---

## 추천 순서

1. **Vercel Postgres** - Vercel과 통합되어 가장 쉬움
2. **Neon** - 무료 티어가 넉넉하고 사용하기 쉬움
3. **Supabase** - 추가 기능이 많지만 설정이 조금 복잡
4. **Railway** - 간단하지만 무료 티어 제한이 있음

