# YouTube Transcript Extractor

YouTube 비디오의 자막을 추출하는 Python 프로그램입니다.

## 설치

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
   - `.env.example` 파일을 `.env`로 복사
   - `.env` 파일에 Webshare 프록시 사용자명과 비밀번호 입력:
   ```
   PROXY_USERNAME=your_username
   PROXY_PASSWORD=your_password
   ```

## 사용 방법

```bash
python extract_transcript.py
```

프로그램은 지정된 YouTube 비디오의 자막을 추출하여 콘솔에 출력합니다.

## 참고

- 이 프로그램은 `youtube-transcript-api` 라이브러리를 사용합니다.
- Webshare 프록시를 통해 요청을 전송하여 IP 차단을 우회합니다.
- 프록시 설정은 `.env` 파일에서 관리됩니다.


