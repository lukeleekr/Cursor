"""
리뷰 컬럼 자동 감지 모듈
컬럼명의 키워드를 기반으로 리뷰 컬럼을 자동으로 찾습니다.
"""

import pandas as pd
from typing import Optional, List


class ColumnDetector:
    """리뷰 컬럼을 자동으로 감지하는 클래스"""
    
    # 리뷰 컬럼을 찾기 위한 키워드 목록 (우선순위 순)
    REVIEW_KEYWORDS = [
        ['리뷰', 'review'],
        ['comment', '댓글'],
        ['내용', 'content', 'text', '텍스트'],
        ['의견', 'opinion', 'feedback'],
        ['평가', 'evaluation', 'assessment']
    ]
    
    def __init__(self, keywords: Optional[List[List[str]]] = None):
        """
        Args:
            keywords: 사용자 정의 키워드 목록 (기본값 사용 시 None)
        """
        self.keywords = keywords or self.REVIEW_KEYWORDS
    
    def find_review_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        데이터프레임에서 리뷰 컬럼을 자동으로 찾습니다.
        
        Args:
            df: 분석할 데이터프레임
            
        Returns:
            리뷰 컬럼명 (찾지 못한 경우 None)
            
        Raises:
            ValueError: 리뷰 컬럼을 찾지 못한 경우
        """
        if df.empty:
            raise ValueError("데이터프레임이 비어있습니다.")
        
        columns = df.columns.tolist()
        candidates = []
        
        # 각 우선순위 그룹별로 검색
        for priority, keyword_group in enumerate(self.keywords):
            for col in columns:
                col_lower = str(col).lower()
                for keyword in keyword_group:
                    if keyword.lower() in col_lower:
                        candidates.append({
                            'column': col,
                            'priority': priority,
                            'keyword': keyword
                        })
                        break  # 한 그룹에서 하나만 찾으면 충분
        
        if not candidates:
            # 키워드로 찾지 못한 경우, 텍스트가 가장 긴 컬럼을 후보로 고려
            text_columns = []
            for col in columns:
                if df[col].dtype == 'object':  # 문자열 타입
                    avg_length = df[col].astype(str).str.len().mean()
                    if avg_length > 20:  # 평균 길이가 20자 이상인 컬럼
                        text_columns.append({
                            'column': col,
                            'avg_length': avg_length,
                            'priority': 999  # 낮은 우선순위
                        })
            
            if text_columns:
                # 가장 긴 텍스트 컬럼을 선택
                best_candidate = max(text_columns, key=lambda x: x['avg_length'])
                return best_candidate['column']
            
            raise ValueError(
                f"리뷰 컬럼을 찾을 수 없습니다. "
                f"사용 가능한 컬럼: {', '.join(columns)}"
            )
        
        # 우선순위가 가장 높은 컬럼 선택 (같은 우선순위면 첫 번째)
        best_candidate = min(candidates, key=lambda x: (x['priority'], columns.index(x['column'])))
        return best_candidate['column']
    
    def detect_by_keywords(self, columns: List[str], keywords: List[str]) -> List[str]:
        """
        키워드 목록을 사용하여 매칭되는 컬럼을 찾습니다.
        
        Args:
            columns: 검색할 컬럼 목록
            keywords: 검색할 키워드 목록
            
        Returns:
            매칭되는 컬럼명 목록
        """
        matches = []
        columns_lower = [str(col).lower() for col in columns]
        keywords_lower = [kw.lower() for kw in keywords]
        
        for col, col_lower in zip(columns, columns_lower):
            for keyword in keywords_lower:
                if keyword in col_lower:
                    matches.append(col)
                    break
        
        return matches

