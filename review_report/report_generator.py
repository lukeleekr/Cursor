"""
보고서 생성 모듈
Markdown 및 HTML 형식의 보고서를 생성합니다.
"""

import os
from typing import Dict, Any
from datetime import datetime


class ReportGenerator:
    """Markdown 형식의 보고서를 생성하는 클래스"""
    
    def __init__(self, output_dir: str = 'reports'):
        """
        Args:
            output_dir: 보고서를 저장할 디렉토리
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def generate_markdown_report(self, analysis_results: Dict[str, Any],
                               filename: str = None) -> str:
        """
        Markdown 보고서를 생성합니다.
        
        Args:
            analysis_results: 분석 결과 딕셔너리
            filename: 출력 파일명 (None이면 자동 생성)
            
        Returns:
            생성된 파일 경로
        """
        if filename is None:
            filename = f'report_{self.timestamp}.md'
        
        filepath = os.path.join(self.output_dir, filename)
        
        basic_stats = analysis_results['basic_stats']
        sentiment_analysis = analysis_results.get('sentiment_analysis', {})
        
        md_content = f"""# 고객 리뷰 분석 보고서

**생성 일시:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. 기본 통계

- **총 리뷰 수:** {basic_stats['total_reviews']}
"""
        
        if basic_stats.get('rating_stats'):
            md_content += f"""
- **평균 평점:** {basic_stats['rating_stats']['mean']:.2f}
- **중앙값:** {basic_stats['rating_stats']['median']:.2f}
- **표준편차:** {basic_stats['rating_stats']['std']:.2f}
- **최소값:** {basic_stats['rating_stats']['min']}
- **최대값:** {basic_stats['rating_stats']['max']}

### 평점 분포

| 평점 | 리뷰 수 | 비율 (%) |
|------|---------|----------|
"""
            for rating in sorted(basic_stats.get('rating_distribution', {}).keys()):
                count = basic_stats['rating_distribution'][rating]
                pct = basic_stats['rating_percentage'][rating]
                md_content += f"| {rating}점 | {count} | {pct:.1f} |\n"
        
        if sentiment_analysis:
            md_content += f"""
---

## 2. 감정 분석 (OpenAI API)

- **긍정 리뷰:** {sentiment_analysis['positive']} ({sentiment_analysis['positive_percentage']:.1f}%)
- **부정 리뷰:** {sentiment_analysis['negative']} ({sentiment_analysis['negative_percentage']:.1f}%)
- **중립 리뷰:** {sentiment_analysis['neutral']} ({sentiment_analysis['neutral_percentage']:.1f}%)

### 긍정 키워드 분석

긍정 리뷰에서 자주 언급된 주요 키워드와 관련 리뷰입니다.

"""
            
            positive_keywords = sentiment_analysis.get('positive_keywords', [])
            if positive_keywords:
                for i, kw_data in enumerate(positive_keywords[:10], 1):
                    keyword = kw_data.get('keyword', 'N/A')
                    count = kw_data.get('count', 0)
                    reviews = kw_data.get('reviews', [])
                    
                    md_content += f"#### {i}. {keyword} (언급 횟수: {count})\n\n"
                    md_content += "**관련 리뷰:**\n\n"
                    for j, review in enumerate(reviews[:5], 1):
                        review_short = review[:150] + '...' if len(review) > 150 else review
                        md_content += f"{j}. {review_short}\n\n"
            else:
                md_content += "*키워드 정보가 없습니다.*\n\n"
            
            md_content += "### 부정 키워드 분석\n\n"
            md_content += "부정 리뷰에서 자주 언급된 주요 키워드와 관련 리뷰입니다.\n\n"
            
            negative_keywords = sentiment_analysis.get('negative_keywords', [])
            if negative_keywords:
                for i, kw_data in enumerate(negative_keywords[:10], 1):
                    keyword = kw_data.get('keyword', 'N/A')
                    count = kw_data.get('count', 0)
                    reviews = kw_data.get('reviews', [])
                    
                    md_content += f"#### {i}. {keyword} (언급 횟수: {count})\n\n"
                    md_content += "**관련 리뷰:**\n\n"
                    for j, review in enumerate(reviews[:5], 1):
                        review_short = review[:150] + '...' if len(review) > 150 else review
                        md_content += f"{j}. {review_short}\n\n"
            else:
                md_content += "*키워드 정보가 없습니다.*\n\n"
        
        if basic_stats.get('model_statistics'):
            md_content += """
---

## 3. 노트북 모델별 통계

| 모델명 | 평균 평점 | 리뷰 수 |
|--------|-----------|---------|
"""
            for model, stats in basic_stats['model_statistics'].items():
                avg_rating = stats.get('평균평점', 'N/A')
                review_count = stats.get('리뷰수', 0)
                if isinstance(avg_rating, (int, float)):
                    md_content += f"| {model} | {avg_rating:.2f} | {review_count} |\n"
                else:
                    md_content += f"| {model} | {avg_rating} | {review_count} |\n"
        
        if basic_stats.get('age_statistics'):
            md_content += """
---

## 4. 연령대별 통계

| 연령대 | 평균 평점 |
|--------|-----------|
"""
            for age, stats in basic_stats['age_statistics'].items():
                avg_rating = stats.get('평균평점', 'N/A')
                if isinstance(avg_rating, (int, float)):
                    md_content += f"| {age} | {avg_rating:.2f} |\n"
                else:
                    md_content += f"| {age} | {avg_rating} |\n"
        
        if basic_stats.get('gender_statistics'):
            md_content += """
---

## 5. 성별 통계

| 성별 | 평균 평점 |
|------|-----------|
"""
            for gender, stats in basic_stats['gender_statistics'].items():
                avg_rating = stats.get('평균평점', 'N/A')
                if isinstance(avg_rating, (int, float)):
                    md_content += f"| {gender} | {avg_rating:.2f} |\n"
                else:
                    md_content += f"| {gender} | {avg_rating} |\n"
        
        md_content += """
---

*이 보고서는 OpenAI API를 활용하여 자동으로 생성되었습니다.*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # HTML 보고서도 함께 생성 (클릭 가능한 인터랙티브 버전)
        html_filepath = filepath.replace('.md', '.html')
        self.generate_html_report(analysis_results, html_filepath)
        
        return filepath
    
    def generate_html_report(self, analysis_results: Dict[str, Any],
                            filepath: str = None) -> str:
        """
        HTML 보고서를 생성합니다 (클릭 가능한 키워드 포함).
        
        Args:
            analysis_results: 분석 결과 딕셔너리
            filepath: 출력 파일 경로
            
        Returns:
            생성된 파일 경로
        """
        if filepath is None:
            filepath = os.path.join(self.output_dir, f'report_{self.timestamp}.html')
        
        basic_stats = analysis_results['basic_stats']
        sentiment_analysis = analysis_results.get('sentiment_analysis', {})
        
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>고객 리뷰 분석 보고서</title>
    <style>
        body {{
            font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
            border-left: 4px solid #4CAF50;
            padding-left: 10px;
        }}
        h3 {{
            color: #666;
            margin-top: 20px;
        }}
        .stat-box {{
            background-color: #f9f9f9;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 3px solid #4CAF50;
        }}
        .keyword-item {{
            background-color: #e8f5e9;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        .keyword-item:hover {{
            background-color: #c8e6c9;
        }}
        .keyword-header {{
            font-weight: bold;
            font-size: 1.1em;
            color: #2e7d32;
            margin-bottom: 10px;
        }}
        .keyword-count {{
            color: #666;
            font-size: 0.9em;
        }}
        .review-list {{
            display: none;
            margin-top: 10px;
            padding-left: 20px;
        }}
        .review-list.active {{
            display: block;
        }}
        .review-item {{
            background-color: #f5f5f5;
            padding: 10px;
            margin: 5px 0;
            border-radius: 3px;
            border-left: 3px solid #81c784;
        }}
        .negative-keyword {{
            background-color: #ffebee;
        }}
        .negative-keyword:hover {{
            background-color: #ffcdd2;
        }}
        .negative-keyword .keyword-header {{
            color: #c62828;
        }}
        .negative-keyword .review-item {{
            border-left-color: #ef5350;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
    </style>
    <script>
        function toggleReviews(element) {{
            const reviewList = element.querySelector('.review-list');
            if (reviewList) {{
                if (reviewList.classList.contains('active')) {{
                    reviewList.classList.remove('active');
                }} else {{
                    reviewList.classList.add('active');
                }}
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <h1>고객 리뷰 분석 보고서</h1>
        <p><strong>생성 일시:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>1. 기본 통계</h2>
        <div class="stat-box">
            <p><strong>총 리뷰 수:</strong> {basic_stats['total_reviews']}</p>
"""
        
        if basic_stats.get('rating_stats'):
            html_content += f"""
            <p><strong>평균 평점:</strong> {basic_stats['rating_stats']['mean']:.2f}</p>
            <p><strong>중앙값:</strong> {basic_stats['rating_stats']['median']:.2f}</p>
"""
        
        html_content += """
        </div>
"""
        
        if sentiment_analysis:
            html_content += f"""
        <h2>2. 감정 분석 (OpenAI API)</h2>
        <div class="stat-box">
            <p><strong>긍정 리뷰:</strong> {sentiment_analysis['positive']} ({sentiment_analysis['positive_percentage']:.1f}%)</p>
            <p><strong>부정 리뷰:</strong> {sentiment_analysis['negative']} ({sentiment_analysis['negative_percentage']:.1f}%)</p>
            <p><strong>중립 리뷰:</strong> {sentiment_analysis['neutral']} ({sentiment_analysis['neutral_percentage']:.1f}%)</p>
        </div>
        
        <h3>긍정 키워드 분석</h3>
        <p>키워드를 클릭하면 관련 리뷰를 확인할 수 있습니다.</p>
"""
            
            positive_keywords = sentiment_analysis.get('positive_keywords', [])
            if positive_keywords:
                for kw_data in positive_keywords[:10]:
                    keyword = kw_data.get('keyword', 'N/A')
                    count = kw_data.get('count', 0)
                    reviews = kw_data.get('reviews', [])
                    
                    html_content += f"""
        <div class="keyword-item" onclick="toggleReviews(this)">
            <div class="keyword-header">{keyword}</div>
            <div class="keyword-count">언급 횟수: {count}</div>
            <div class="review-list">
"""
                    for review in reviews[:5]:
                        review_escaped = review.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
                        html_content += f'                <div class="review-item">{review_escaped}</div>\n'
                    
                    html_content += """
            </div>
        </div>
"""
            else:
                html_content += "<p>키워드 정보가 없습니다.</p>"
            
            html_content += """
        <h3>부정 키워드 분석</h3>
        <p>키워드를 클릭하면 관련 리뷰를 확인할 수 있습니다.</p>
"""
            
            negative_keywords = sentiment_analysis.get('negative_keywords', [])
            if negative_keywords:
                for kw_data in negative_keywords[:10]:
                    keyword = kw_data.get('keyword', 'N/A')
                    count = kw_data.get('count', 0)
                    reviews = kw_data.get('reviews', [])
                    
                    html_content += f"""
        <div class="keyword-item negative-keyword" onclick="toggleReviews(this)">
            <div class="keyword-header">{keyword}</div>
            <div class="keyword-count">언급 횟수: {count}</div>
            <div class="review-list">
"""
                    for review in reviews[:5]:
                        review_escaped = review.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
                        html_content += f'                <div class="review-item">{review_escaped}</div>\n'
                    
                    html_content += """
            </div>
        </div>
"""
            else:
                html_content += "<p>키워드 정보가 없습니다.</p>"
        
        html_content += """
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
