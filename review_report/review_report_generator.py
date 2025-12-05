"""
고객 리뷰 데이터 보고서 생성기
엑셀 파일의 리뷰 데이터를 분석하여 Markdown 형식의 보고서를 생성합니다.
OpenAI API를 활용한 감정 및 후기 분석을 포함합니다.
"""

import pandas as pd
import os
from typing import Optional, List
from column_detector import ColumnDetector
from analyzer import ReviewAnalyzer
from report_generator import ReportGenerator


class ReviewReportGenerator:
    """고객 리뷰 데이터를 분석하고 보고서를 생성하는 메인 클래스"""
    
    def __init__(self, excel_file: str, output_dir: str = 'reports', 
                 rating_column: str = '평점'):
        """
        Args:
            excel_file: 분석할 엑셀 파일 경로
            output_dir: 보고서를 저장할 디렉토리
            rating_column: 평점 컬럼명 (기본값: '평점')
        """
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f"엑셀 파일을 찾을 수 없습니다: {excel_file}")
        
        self.excel_file = excel_file
        self.output_dir = output_dir
        self.rating_column = rating_column
        
        # 모듈 초기화
        self.column_detector = ColumnDetector()
        self.analyzer = ReviewAnalyzer()
        self.report_generator = ReportGenerator(output_dir)
        
        # 데이터 로드
        self.df = None
        self.review_column = None
        self.analysis_results = None
    
    def load_data(self) -> pd.DataFrame:
        """
        엑셀 파일을 로드합니다.
        
        Returns:
            로드된 데이터프레임
        """
        try:
            self.df = pd.read_excel(self.excel_file)
            if self.df.empty:
                raise ValueError("엑셀 파일이 비어있습니다.")
            return self.df
        except Exception as e:
            raise ValueError(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {str(e)}")
    
    def detect_review_column(self, manual_column: Optional[str] = None) -> str:
        """
        리뷰 컬럼을 감지합니다.
        
        Args:
            manual_column: 수동으로 지정할 컬럼명 (None이면 자동 감지)
            
        Returns:
            리뷰 컬럼명
            
        Raises:
            ValueError: 리뷰 컬럼을 찾을 수 없는 경우
        """
        if self.df is None:
            self.load_data()
        
        if manual_column:
            if manual_column not in self.df.columns:
                raise ValueError(
                    f"지정한 컬럼 '{manual_column}'을 찾을 수 없습니다. "
                    f"사용 가능한 컬럼: {', '.join(self.df.columns.tolist())}"
                )
            self.review_column = manual_column
            return manual_column
        
        try:
            self.review_column = self.column_detector.find_review_column(self.df)
            return self.review_column
        except ValueError as e:
            # 사용자에게 수동 입력 옵션 제공
            available_columns = ', '.join(self.df.columns.tolist())
            error_msg = (
                f"{str(e)}\n\n"
                f"사용 가능한 컬럼 목록:\n"
                f"{available_columns}\n\n"
                f"수동으로 리뷰 컬럼을 지정하려면 detect_review_column(manual_column='컬럼명')을 사용하세요."
            )
            raise ValueError(error_msg)
    
    def analyze(self, review_column: Optional[str] = None) -> dict:
        """
        리뷰 데이터를 분석합니다.
        
        Args:
            review_column: 리뷰 컬럼명 (None이면 자동 감지)
            
        Returns:
            분석 결과 딕셔너리
        """
        if self.df is None:
            self.load_data()
        
        if review_column:
            self.review_column = review_column
        elif self.review_column is None:
            self.detect_review_column()
        
        # 리뷰 컬럼 유효성 검사
        if self.review_column not in self.df.columns:
            raise ValueError(f"리뷰 컬럼 '{self.review_column}'을 찾을 수 없습니다.")
        
        # 분석 수행
        self.analysis_results = self.analyzer.analyze_all(
            self.df, 
            self.review_column, 
            self.rating_column
        )
        
        return self.analysis_results
    
    def generate_report(self, filename: Optional[str] = None) -> str:
        """
        Markdown 보고서를 생성합니다.
        
        Args:
            filename: 출력 파일명 (None이면 자동 생성)
            
        Returns:
            생성된 파일 경로
        """
        if self.analysis_results is None:
            self.analyze()
        
        return self.report_generator.generate_markdown_report(
            self.analysis_results, 
            filename
        )
    
    def get_summary(self) -> dict:
        """
        분석 결과 요약을 반환합니다.
        
        Returns:
            요약 정보 딕셔너리
        """
        if self.analysis_results is None:
            self.analyze()
        
        basic_stats = self.analysis_results['basic_stats']
        sentiment_analysis = self.analysis_results.get('sentiment_analysis', {})
        
        summary = {
            'total_reviews': basic_stats['total_reviews'],
            'review_column': self.review_column,
            'rating_column': self.rating_column
        }
        
        if basic_stats.get('rating_stats'):
            summary['average_rating'] = basic_stats['rating_stats']['mean']
        
        if sentiment_analysis:
            summary['sentiment'] = {
                'positive': sentiment_analysis['positive'],
                'negative': sentiment_analysis['negative'],
                'neutral': sentiment_analysis['neutral']
            }
        
        return summary


# 명령줄 인터페이스
if __name__ == '__main__':
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='고객 리뷰 데이터를 분석하여 Markdown 보고서를 생성합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python review_report_generator.py "노트북 고객 리뷰 데이터.xlsx"
  python review_report_generator.py "데이터.xlsx" --output reports
  python review_report_generator.py "데이터.xlsx" --review-column "리뷰내용"
        """
    )
    
    parser.add_argument(
        'excel_file',
        help='분석할 엑셀 파일 경로'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='reports',
        help='보고서를 저장할 디렉토리 (기본값: reports)'
    )
    
    parser.add_argument(
        '--review-column', '-r',
        default=None,
        help='리뷰 컬럼명 (지정하지 않으면 자동 감지)'
    )
    
    parser.add_argument(
        '--rating-column',
        default='평점',
        help='평점 컬럼명 (기본값: 평점)'
    )
    
    parser.add_argument(
        '--filename', '-f',
        default=None,
        help='생성할 보고서 파일명 (지정하지 않으면 자동 생성)'
    )
    
    args = parser.parse_args()
    
    try:
        print("=" * 60)
        print("고객 리뷰 분석 보고서 생성기")
        print("=" * 60)
        print(f"\n엑셀 파일: {args.excel_file}")
        print(f"출력 디렉토리: {args.output}")
        
        # 보고서 생성기 초기화
        generator = ReviewReportGenerator(
            excel_file=args.excel_file,
            output_dir=args.output,
            rating_column=args.rating_column
        )
        
        # 리뷰 컬럼 감지
        if args.review_column:
            print(f"\n리뷰 컬럼: {args.review_column} (수동 지정)")
            generator.detect_review_column(manual_column=args.review_column)
        else:
            print("\n리뷰 컬럼 자동 감지 중...")
            review_col = generator.detect_review_column()
            print(f"감지된 리뷰 컬럼: {review_col}")
        
        # 분석 수행
        print("\n데이터 분석 중...")
        generator.analyze()
        
        # 보고서 생성
        print("\n보고서 생성 중...")
        report_file = generator.generate_report(filename=args.filename)
        
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
        
    except FileNotFoundError as e:
        print(f"\n오류: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"\n오류: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n예상치 못한 오류가 발생했습니다: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

