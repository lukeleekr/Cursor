"""
축산물 발송 안내 메일 자동 발송 프로그램
Gmail SMTP를 사용하여 엑셀 파일의 고객에게 메일을 발송합니다.
"""

import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import time

# .env 파일에서 환경변수 로드
load_dotenv()

# Gmail SMTP 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# 테스트용 이메일 설정
TEST_EMAIL = "lukeleekr@gmail.com"
SENDER_EMAIL = TEST_EMAIL
RECEIVER_EMAIL = TEST_EMAIL

# Gmail 앱 비밀번호 (환경변수에서 가져옴)
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def load_excel_data(file_path: str, limit: int = 10) -> pd.DataFrame:
    """엑셀 파일에서 데이터를 로드합니다."""
    df = pd.read_excel(file_path)
    return df.head(limit)


def create_email_message(sender: str, receiver: str, subject: str, body: str) -> MIMEMultipart:
    """이메일 메시지를 생성합니다."""
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    
    # HTML 형식으로 메일 본문 작성
    html_body = f"""
    <html>
    <body style="font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #4CAF50; color: white; padding: 20px; text-align: center;">
                <h1 style="margin: 0;">🥩 팜앤푸드</h1>
            </div>
            <div style="padding: 20px; background-color: #f9f9f9;">
                <p>{body}</p>
            </div>
            <div style="padding: 20px; text-align: center; color: #666; font-size: 12px;">
                <p>본 메일은 테스트용으로 발송되었습니다.</p>
                <p>© 2025 팜앤푸드. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    message.attach(MIMEText(html_body, "html", "utf-8"))
    return message


def send_email(smtp_server: smtplib.SMTP, message: MIMEMultipart) -> bool:
    """이메일을 발송합니다."""
    try:
        smtp_server.send_message(message)
        return True
    except Exception as e:
        print(f"  ❌ 발송 실패: {e}")
        return False


def main():
    """메인 함수"""
    print("=" * 60)
    print("🚀 축산물 발송 안내 메일 자동 발송 프로그램")
    print("=" * 60)
    
    # Gmail 앱 비밀번호 확인
    if not GMAIL_APP_PASSWORD:
        print("\n❌ 오류: GMAIL_APP_PASSWORD 환경변수가 설정되지 않았습니다.")
        print("\n📋 설정 방법:")
        print("1. .env 파일을 생성하고 다음 내용을 추가하세요:")
        print("   GMAIL_APP_PASSWORD=your_app_password_here")
        print("\n2. Gmail 앱 비밀번호 생성 방법:")
        print("   - Google 계정 > 보안 > 2단계 인증 활성화")
        print("   - Google 계정 > 보안 > 앱 비밀번호 생성")
        print("   - 앱 선택: 메일, 기기 선택: Windows 컴퓨터")
        print("   - 생성된 16자리 비밀번호를 .env 파일에 저장")
        return
    
    # 엑셀 파일 로드
    excel_file = "축산메일실습용.xlsx"
    print(f"\n📂 엑셀 파일 로드 중: {excel_file}")
    
    try:
        df = load_excel_data(excel_file, limit=10)
        print(f"✅ {len(df)}개의 데이터 로드 완료")
    except Exception as e:
        print(f"❌ 엑셀 파일 로드 실패: {e}")
        return
    
    # SMTP 서버 연결
    print(f"\n📧 Gmail SMTP 서버 연결 중...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # TLS 암호화 시작
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        print("✅ SMTP 서버 연결 성공")
    except Exception as e:
        print(f"❌ SMTP 서버 연결 실패: {e}")
        return
    
    # 메일 발송
    print(f"\n📬 메일 발송 시작 (총 {len(df)}건)")
    print("-" * 60)
    
    success_count = 0
    fail_count = 0
    
    for idx, row in df.iterrows():
        customer_name = row['고객명']
        subject = row['메일제목']
        body = row['메일내용']
        
        print(f"\n[{idx + 1}/{len(df)}] {customer_name}님에게 메일 발송 중...")
        print(f"  📋 제목: {subject}")
        
        # 이메일 메시지 생성
        message = create_email_message(
            sender=SENDER_EMAIL,
            receiver=RECEIVER_EMAIL,  # 테스트용으로 모두 같은 주소로 발송
            subject=f"[테스트] {subject}",
            body=body
        )
        
        # 이메일 발송
        if send_email(server, message):
            print(f"  ✅ 발송 성공!")
            success_count += 1
        else:
            fail_count += 1
        
        # Gmail 발송 제한을 피하기 위해 잠시 대기
        time.sleep(1)
    
    # SMTP 서버 연결 종료
    server.quit()
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("📊 발송 결과")
    print("=" * 60)
    print(f"✅ 성공: {success_count}건")
    print(f"❌ 실패: {fail_count}건")
    print(f"📧 총 발송: {success_count + fail_count}건")
    print("\n🎉 메일 발송이 완료되었습니다!")


if __name__ == "__main__":
    main()


