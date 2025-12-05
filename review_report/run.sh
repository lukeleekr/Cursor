#!/bin/bash
# 고객 리뷰 분석 보고서 생성기 실행 스크립트

echo "============================================================"
echo "고객 리뷰 분석 보고서 생성기"
echo "============================================================"
echo ""

if [ -z "$1" ]; then
    echo "사용법: ./run.sh 엑셀파일경로"
    echo ""
    echo "예시: ./run.sh \"노트북 고객 리뷰 데이터.xlsx\""
    exit 1
fi

python3 review_report_generator.py "$1"

if [ $? -ne 0 ]; then
    echo ""
    echo "오류가 발생했습니다."
    exit 1
fi

