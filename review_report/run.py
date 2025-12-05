#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
간단한 실행 스크립트
엑셀 파일을 드래그 앤 드롭하거나 경로를 입력하여 실행할 수 있습니다.
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from review_report_generator import ReviewReportGenerator

def main():
    print("=" * 60)
    print("고객 리뷰 분석 보고서 생성기")
    print("=" * 60)
    
    # 명령줄 인자가 있으면 사용
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        # 사용자 입력 받기
        excel_file = input("\n엑셀 파일 경로를 입력하세요: ").strip().strip('"').strip("'")
    
    if not excel_file:
        print("오류: 엑셀 파일 경로를 입력해주세요.")
        sys.exit(1)
    
    if not os.path.exists(excel_file):
        print(f"오류: 파일을 찾을 수 없습니다: {excel_file}")
        sys.exit(1)
    
    try:
        print(f"\n엑셀 파일: {excel_file}")
        print("분석을 시작합니다...\n")
        
        # 보고서 생성기 초기화
        generator = ReviewReportGenerator(excel_file=excel_file)
        
        # 리뷰 컬럼 자동 감지
        print("리뷰 컬럼 자동 감지 중...")
        review_col = generator.detect_review_column()
        print(f"감지된 리뷰 컬럼: {review_col}\n")
        
        # 분석 수행
        print("데이터 분석 중... (OpenAI API 호출 중이므로 시간이 걸릴 수 있습니다)")
        generator.analyze()
        
        # 보고서 생성
        print("\n보고서 생성 중...")
        report_file = generator.generate_report()
        
        # 요약 정보 출력
        summary = generator.get_summary()
        
        print("\n" + "=" * 60)
        print("분석 완료!")
        print("=" * 60)
        print(f"\n생성된 보고서: {report_file}")
        print(f"\n분석 요약:")
        print(f"  총 리뷰 수: {summary['total_reviews']}")
        print(f"  리뷰 컬럼: {summary['review_column']}")
        if 'average_rating' in summary:
            print(f"  평균 평점: {summary['average_rating']:.2f}")
        if 'sentiment' in summary:
            print(f"  감정 분석:")
            print(f"    - 긍정: {summary['sentiment']['positive']}개")
            print(f"    - 부정: {summary['sentiment']['negative']}개")
            print(f"    - 중립: {summary['sentiment']['neutral']}개")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

