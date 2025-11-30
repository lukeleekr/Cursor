# Vercel 배포 가이드

## ✅ 완료된 작업

1. ✅ Prisma 스키마를 PostgreSQL로 변경
2. ✅ Neon 데이터베이스 연결 설정
3. ✅ 데이터베이스 테이블 생성 완료

## Vercel 배포 단계

### 1단계: GitHub에 코드 푸시

```bash
# Git 초기화 (아직 안 했다면)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Add PostgreSQL support and prepare for Vercel deployment"

# GitHub 저장소 생성 후
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2단계: Vercel에서 프로젝트 배포

1. **Vercel 접속**
   - https://vercel.com 접속
   - GitHub로 로그인

2. **프로젝트 추가**
   - "Add New Project" 클릭
   - GitHub 저장소 선택 (`memo-app` 또는 프로젝트 이름)
   - "Import" 클릭

3. **프로젝트 설정**
   - Framework Preset: **Next.js** (자동 감지됨)
   - Root Directory: `./` (프로젝트 루트)
   - Build Command: `npm run build` (자동 설정됨)
   - Output Directory: `.next` (자동 설정됨)

4. **환경 변수 추가** ⭐ 중요!
   - "Environment Variables" 섹션 클릭
   - 다음 변수 추가:
     ```
     Key: DATABASE_URL
     Value: postgresql://neondb_owner:npg_XwMheL9OB2oE@ep-withered-butterfly-a1a0ct29-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
     ```
   - Environment: **Production**, **Preview**, **Development** 모두 선택
   - "Save" 클릭

5. **배포**
   - "Deploy" 버튼 클릭
   - 배포 완료까지 2-3분 소요

### 3단계: 배포 확인

- 배포가 완료되면 Vercel이 URL을 제공합니다
- 예: `https://memo-app-xxx.vercel.app`
- 해당 URL로 접속하여 앱이 정상 작동하는지 확인

## 주의사항

### 보안
- ⚠️ DATABASE_URL에 비밀번호가 포함되어 있으므로 절대 공개하지 마세요
- ⚠️ GitHub에 `.env` 파일을 커밋하지 마세요 (이미 `.gitignore`에 포함됨)

### 환경 변수
- Vercel의 환경 변수는 각 환경(Production, Preview, Development)별로 설정 가능
- Production과 Preview 환경에 모두 설정하는 것을 권장

### 데이터베이스 연결
- Neon은 무료 티어에서도 충분한 용량을 제공합니다
- 필요시 Neon 대시보드에서 사용량 확인 가능

## 문제 해결

### 배포 실패 시
1. Vercel 로그 확인: 프로젝트 → Deployments → 실패한 배포 클릭 → Logs 확인
2. 환경 변수 확인: DATABASE_URL이 올바르게 설정되었는지 확인
3. Prisma Client 생성 확인: `postinstall` 스크립트가 실행되는지 확인

### 데이터베이스 연결 오류 시
1. Neon 대시보드에서 데이터베이스 상태 확인
2. DATABASE_URL이 올바른지 확인 (특히 비밀번호)
3. SSL 모드 확인 (`sslmode=require` 포함되어 있는지)

## 다음 단계

배포가 완료되면:
1. ✅ 앱이 정상 작동하는지 테스트
2. ✅ 회원가입/로그인 기능 테스트
3. ✅ 메모 작성/삭제 기능 테스트
4. ✅ 커스텀 도메인 설정 (선택사항)

