from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import time

def scrape_gold_prices():
    """
    한국금거래소 웹사이트에서 금 시세 데이터를 스크래핑하여 엑셀 파일로 저장합니다.
    """
    url = "https://www.koreagoldx.co.kr/price/gold"
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않음
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        print("브라우저를 시작하는 중...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"페이지 로딩 중: {url}")
        driver.get(url)
        
        # 테이블이 로드될 때까지 대기
        print("테이블 데이터 로딩 대기 중...")
        wait = WebDriverWait(driver, 20)
        
        # Tabulator 테이블이 로드될 때까지 대기
        wait.until(EC.presence_of_element_located((By.ID, "example-table")))
        time.sleep(3)  # 추가 대기 시간 (데이터 로딩 완료를 위해)
        
        # 데이터 추출 (여러 페이지에서 수집)
        print("데이터 추출 중...")
        df_data = []
        max_data = 100
        page = 1
        
        while len(df_data) < max_data:
            # 현재 페이지의 행 가져오기
            rows = driver.find_elements(By.CSS_SELECTOR, "#example-table .tabulator-row")
            
            if not rows:
                print(f"페이지 {page}에서 데이터를 찾을 수 없습니다.")
                break
            
            print(f"페이지 {page}: {len(rows)}개의 행을 찾았습니다.")
            
            # 현재 페이지의 데이터 추출
            for i, row in enumerate(rows):
                if len(df_data) >= max_data:
                    break
                    
                try:
                    cells = row.find_elements(By.CSS_SELECTOR, ".tabulator-cell")
                    if len(cells) >= 5:
                        date = cells[0].text.strip()
                        s_pure = cells[1].text.strip()  # 내가 살 때 - 순금
                        p_pure = cells[2].text.strip()  # 내가 팔 때 - 순금
                        p_18k = cells[3].text.strip()   # 내가 팔 때 - 18K
                        p_14k = cells[4].text.strip()   # 내가 팔 때 - 14K
                        
                        # 중복 체크 (같은 날짜와 가격이면 스킵)
                        is_duplicate = False
                        for existing in df_data:
                            if existing['고시날짜'] == date and existing['내가 살 때(3.75g) - 순금'] == s_pure:
                                is_duplicate = True
                                break
                        
                        if not is_duplicate:
                            df_data.append({
                                '고시날짜': date,
                                '내가 살 때(3.75g) - 순금': s_pure,
                                '내가 팔 때(3.75g) - 순금': p_pure,
                                '내가 팔 때(3.75g) - 18K': p_18k,
                                '내가 팔 때(3.75g) - 14K': p_14k
                            })
                except Exception as e:
                    print(f"행 처리 중 오류: {e}")
                    continue
            
            # 다음 페이지로 이동
            if len(df_data) < max_data:
                try:
                    # 다음 페이지 버튼 찾기
                    next_button = driver.find_element(By.CSS_SELECTOR, "button.tabulator-page[data-page='next']:not([disabled])")
                    if next_button.is_enabled():
                        next_button.click()
                        time.sleep(2)  # 페이지 로딩 대기
                        page += 1
                    else:
                        print("더 이상 페이지가 없습니다.")
                        break
                except Exception as e:
                    print(f"다음 페이지로 이동할 수 없습니다: {e}")
                    break
        
        if not df_data:
            print("추출된 데이터가 없습니다.")
            return
        
        # 데이터프레임 생성
        df = pd.DataFrame(df_data)
        
        # 엑셀 파일로 저장
        filename = f"금시세_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')
        
        print(f"\n데이터가 성공적으로 저장되었습니다: {filename}")
        print(f"총 {len(df)}개의 데이터가 저장되었습니다.")
        print(f"\n저장된 데이터 미리보기:")
        print(df.head(10))
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
            print("\n브라우저를 종료했습니다.")

if __name__ == "__main__":
    scrape_gold_prices()

