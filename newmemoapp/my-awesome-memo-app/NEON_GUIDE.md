# Neon 사용 가이드

## Neon이란?

**Neon**은 서버리스 PostgreSQL 데이터베이스 서비스입니다.

### 특징:
- ✅ **무료 티어 제공** (충분한 용량)
- ✅ **서버리스** - 자동으로 스케일링
- ✅ **빠른 설정** - 몇 분 안에 시작 가능
- ✅ **Vercel과 완벽 호환**
- ✅ **자동 백업**

### 왜 Neon을 사용하나요?
- 로컬에서는 SQLite를 사용했지만, Vercel(서버리스 환경)에서는 파일 시스템이 영구적이지 않아 SQLite가 작동하지 않습니다
- PostgreSQL은 클라우드에서 안정적으로 작동합니다
- Neon은 무료이고 설정이 쉽습니다

---

## Neon에서 DATABASE_URL 얻는 방법

### 1단계: Neon 계정 생성 및 로그인

1. https://neon.tech 접속
2. **"Sign up"** 또는 **"Log in"** 클릭
3. GitHub 계정으로 로그인 (가장 쉬움)

### 2단계: 프로젝트 생성

1. 대시보드에서 **"Create a project"** 버튼 클릭
2. 프로젝트 이름 입력 (예: `memo-app`)
3. 데이터베이스 이름 입력 (기본값: `neondb` - 그대로 두어도 됨)
4. Region 선택:
   - 한국에서 사용: **Seoul (ap-northeast-2)** 또는 **Tokyo (ap-northeast-1)**
   - 가장 가까운 지역 선택
5. **"Create Project"** 클릭

### 3단계: DATABASE_URL 복사

프로젝트가 생성되면 자동으로 연결 정보가 표시됩니다:

1. 대시보드에서 **"Connection Details"** 섹션 찾기
2. **"Connection string"** 또는 **"Postgres connection string"** 찾기
3. 두 가지 형식이 있을 수 있습니다:
   - **psql 형식**: `postgres://user:password@host/dbname`
   - **URI 형식**: `postgresql://user:password@host/dbname?sslmode=require`
4. **복사 버튼** 클릭 (보통 클립보드 아이콘)

### 예시 DATABASE_URL:
```
postgresql://neondb_owner:AbCdEf123456@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### 4단계: 비밀번호 확인 (필요시)

- 처음 생성 시 비밀번호가 표시됩니다
- 나중에 확인하려면: 프로젝트 → Settings → Database → Reset password

---

## DATABASE_URL 구조 설명

```
postgresql://[사용자명]:[비밀번호]@[호스트]:[포트]/[데이터베이스명]?sslmode=require
```

- **사용자명**: 데이터베이스 사용자 (보통 `neondb_owner`)
- **비밀번호**: 프로젝트 생성 시 설정한 비밀번호
- **호스트**: Neon이 제공하는 서버 주소 (예: `ep-xxx-xxx.region.aws.neon.tech`)
- **포트**: 기본값 5432 (보통 URL에 포함되지 않음)
- **데이터베이스명**: 프로젝트 생성 시 설정한 이름 (기본값: `neondb`)
- **sslmode=require**: SSL 연결 필수

---

## 다음 단계

DATABASE_URL을 얻으셨다면:

1. ✅ Prisma 스키마를 PostgreSQL로 변경
2. ✅ Vercel에 환경 변수로 추가
3. ✅ 배포

DATABASE_URL을 알려주시면 설정을 도와드리겠습니다!

