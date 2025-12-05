"""
데이터 분석 모듈
기본 통계, OpenAI API를 활용한 감정 및 후기 분석을 수행합니다.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from collections import Counter
import re
import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()
load_dotenv()


class ReviewAnalyzer:
    """리뷰 데이터를 분석하는 클래스"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        분석기 초기화
        
        Args:
            api_key: OpenAI API 키 (None이면 .env에서 자동 로드)
            model: 사용할 OpenAI 모델 (기본값: gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API 키가 필요합니다. .env 파일에 OPENAI_API_KEY를 설정하거나 "
                "생성자에 api_key를 전달하세요."
            )
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def analyze_basic_stats(self, df: pd.DataFrame, review_col: str, 
                           rating_col: str = '평점') -> Dict[str, Any]:
        """
        기본 통계 분석을 수행합니다.
        
        Args:
            df: 분석할 데이터프레임
            review_col: 리뷰 컬럼명
            rating_col: 평점 컬럼명
            
        Returns:
            기본 통계 결과 딕셔너리
        """
        results = {
            'total_reviews': len(df),
            'review_column': review_col,
            'rating_column': rating_col
        }
        
        # 평점 분석
        if rating_col in df.columns:
            ratings = df[rating_col].dropna()
            results['rating_stats'] = {
                'mean': float(ratings.mean()),
                'median': float(ratings.median()),
                'std': float(ratings.std()),
                'min': int(ratings.min()),
                'max': int(ratings.max())
            }
            
            # 평점 분포
            rating_dist = ratings.value_counts().sort_index().to_dict()
            results['rating_distribution'] = {int(k): int(v) for k, v in rating_dist.items()}
            
            # 평점 비율
            total = len(ratings)
            results['rating_percentage'] = {
                int(k): round(v / total * 100, 2) 
                for k, v in rating_dist.items()
            }
        else:
            results['rating_stats'] = None
            results['rating_distribution'] = None
            results['rating_percentage'] = None
        
        # 노트북 모델별 분석
        if '노트북모델' in df.columns:
            model_stats = df.groupby('노트북모델').agg({
                rating_col: ['mean', 'count'] if rating_col in df.columns else 'count'
            }).round(2)
            
            if rating_col in df.columns:
                model_stats.columns = ['평균평점', '리뷰수']
                model_stats = model_stats.sort_values('평균평점', ascending=False)
            else:
                model_stats.columns = ['리뷰수']
                model_stats = model_stats.sort_values('리뷰수', ascending=False)
            
            results['model_statistics'] = model_stats.to_dict('index')
        
        # 연령대별 분석
        if '연령대' in df.columns:
            age_stats = df.groupby('연령대').agg({
                rating_col: 'mean' if rating_col in df.columns else 'count'
            }).round(2)
            
            if rating_col in df.columns:
                age_stats.columns = ['평균평점']
            else:
                age_stats.columns = ['리뷰수']
            
            results['age_statistics'] = age_stats.to_dict('index')
        
        # 성별 분석
        if '성별' in df.columns:
            gender_stats = df.groupby('성별').agg({
                rating_col: 'mean' if rating_col in df.columns else 'count'
            }).round(2)
            
            if rating_col in df.columns:
                gender_stats.columns = ['평균평점']
            else:
                gender_stats.columns = ['리뷰수']
            
            results['gender_statistics'] = gender_stats.to_dict('index')
        
        # 구매일자 분석
        if '구매일자' in df.columns:
            df['구매일자'] = pd.to_datetime(df['구매일자'], errors='coerce')
            date_range = df['구매일자'].dropna()
            if len(date_range) > 0:
                results['date_range'] = {
                    'start': date_range.min().strftime('%Y-%m-%d'),
                    'end': date_range.max().strftime('%Y-%m-%d'),
                    'total_days': (date_range.max() - date_range.min()).days
                }
        
        return results
    
    def _analyze_review_with_openai(self, review: str) -> Dict[str, str]:
        """
        OpenAI API를 사용하여 개별 리뷰를 분석합니다.
        
        Args:
            review: 분석할 리뷰 텍스트
            
        Returns:
            분석 결과 딕셔너리 (sentiment, summary)
        """
        prompt = f"""다음 고객 리뷰를 분석해주세요. JSON 형식으로 응답해주세요.

리뷰: {review}

다음 형식으로 응답해주세요:
{{
    "sentiment": "positive" 또는 "negative" 또는 "neutral",
    "summary": "리뷰의 핵심 내용을 1-2문장으로 요약"
}}

응답은 반드시 JSON 형식만 반환하세요."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 고객 리뷰를 분석하는 전문가입니다. JSON 형식으로만 응답하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            # JSON 추출 (코드 블록 제거)
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            result = json.loads(result_text)
            return result
        except Exception as e:
            print(f"리뷰 분석 중 오류 발생: {str(e)}")
            return {"sentiment": "neutral", "summary": "분석 실패"}
    
    def _extract_keywords_with_openai(self, reviews_list: List[str], sentiment_type: str) -> Dict[str, Any]:
        """
        OpenAI API를 사용하여 긍정/부정 키워드를 추출합니다.
        
        Args:
            reviews_list: 분석할 리뷰 리스트
            sentiment_type: 'positive' 또는 'negative'
            
        Returns:
            키워드 및 관련 리뷰 딕셔너리
        """
        reviews_text = "\n".join([f"- {review}" for review in reviews_list[:50]])  # 최대 50개만
        
        prompt = f"""다음 {sentiment_type} 리뷰들을 분석하여 주요 키워드와 각 키워드에 해당하는 리뷰를 추출해주세요.

리뷰 목록:
{reviews_text}

다음 JSON 형식으로 응답해주세요:
{{
    "keywords": [
        {{
            "keyword": "키워드명",
            "count": 키워드가 언급된 리뷰 수,
            "reviews": ["관련 리뷰 1", "관련 리뷰 2", ...]
        }}
    ]
}}

상위 10개 키워드만 추출하고, 각 키워드당 최대 5개의 관련 리뷰를 포함하세요.
응답은 반드시 JSON 형식만 반환하세요."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 고객 리뷰에서 키워드를 추출하는 전문가입니다. JSON 형식으로만 응답하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content.strip()
            # JSON 추출 (코드 블록 제거)
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            result = json.loads(result_text)
            return result
        except Exception as e:
            print(f"키워드 추출 중 오류 발생: {str(e)}")
            return {"keywords": []}
    
    def analyze_sentiment_and_reviews(self, reviews: pd.Series, 
                                      batch_size: int = 10,
                                      extract_keywords: bool = True) -> Dict[str, Any]:
        """
        OpenAI API를 사용하여 리뷰의 감정과 후기를 분석합니다.
        
        Args:
            reviews: 리뷰 텍스트 시리즈
            batch_size: 한 번에 처리할 리뷰 수 (API 호출 제한 고려)
            extract_keywords: 키워드 추출 여부
            
        Returns:
            감정 및 후기 분석 결과 딕셔너리
        """
        reviews = reviews.dropna().astype(str)
        total = len(reviews)
        
        if total == 0:
            return {
                'total': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'positive_percentage': 0,
                'negative_percentage': 0,
                'neutral_percentage': 0,
                'positive_keywords': [],
                'negative_keywords': [],
                'review_summaries': []
            }
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        review_summaries = []
        positive_reviews = []
        negative_reviews = []
        
        print(f"총 {total}개의 리뷰를 분석합니다...")
        
        for i, review in enumerate(reviews, 1):
            if i % batch_size == 0:
                print(f"진행 중: {i}/{total} ({i/total*100:.1f}%)")
                time.sleep(0.5)  # API 호출 제한 방지
            
            analysis = self._analyze_review_with_openai(review)
            sentiment = analysis.get('sentiment', 'neutral')
            summary = analysis.get('summary', '')
            
            if sentiment == 'positive':
                positive_count += 1
                positive_reviews.append(review)
            elif sentiment == 'negative':
                negative_count += 1
                negative_reviews.append(review)
            else:
                neutral_count += 1
            
            review_summaries.append({
                'review': review,
                'sentiment': sentiment,
                'summary': summary
            })
        
        print(f"분석 완료: {total}/{total} (100.0%)")
        
        result = {
            'total': total,
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'positive_percentage': round(positive_count / total * 100, 2),
            'negative_percentage': round(negative_count / total * 100, 2),
            'neutral_percentage': round(neutral_count / total * 100, 2),
            'review_summaries': review_summaries
        }
        
        # 키워드 추출
        if extract_keywords:
            print("\n긍정 키워드 추출 중...")
            if positive_reviews:
                positive_keywords_data = self._extract_keywords_with_openai(positive_reviews, 'positive')
                result['positive_keywords'] = positive_keywords_data.get('keywords', [])
            else:
                result['positive_keywords'] = []
            
            print("부정 키워드 추출 중...")
            if negative_reviews:
                negative_keywords_data = self._extract_keywords_with_openai(negative_reviews, 'negative')
                result['negative_keywords'] = negative_keywords_data.get('keywords', [])
            else:
                result['negative_keywords'] = []
        else:
            result['positive_keywords'] = []
            result['negative_keywords'] = []
        
        return result
    
    
    def analyze_all(self, df: pd.DataFrame, review_col: str, 
                   rating_col: str = '평점') -> Dict[str, Any]:
        """
        모든 분석을 수행합니다.
        
        Args:
            df: 분석할 데이터프레임
            review_col: 리뷰 컬럼명
            rating_col: 평점 컬럼명
            
        Returns:
            모든 분석 결과를 포함한 딕셔너리
        """
        results = {
            'basic_stats': self.analyze_basic_stats(df, review_col, rating_col),
            'sentiment_analysis': self.analyze_sentiment_and_reviews(df[review_col])
        }
        
        return results

