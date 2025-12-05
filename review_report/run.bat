@echo off
chcp 65001 >nul
echo ============================================================
echo 고객 리뷰 분석 보고서 생성기
echo ============================================================
echo.

if "%~1"=="" (
    echo 사용법: run.bat "엑셀파일경로"
    echo.
    echo 예시: run.bat "노트북 고객 리뷰 데이터.xlsx"
    echo.
    pause
    exit /b 1
)

python review_report_generator.py "%~1"

if errorlevel 1 (
    echo.
    echo 오류가 발생했습니다.
    pause
    exit /b 1
)

echo.
pause

