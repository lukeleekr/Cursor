import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from datetime import datetime
import glob

# 한글 폰트 설정 (Windows)
import platform
import os

# 전역 폰트 속성 설정
if platform.system() == 'Windows':
    # 맑은 고딕 폰트 경로들 시도
    font_paths = [
        'C:/Windows/Fonts/malgun.ttf',
        'C:/Windows/Fonts/malgun.ttc',
        'C:/Windows/Fonts/gulim.ttc',
    ]
    
    font_prop = None
    font_name = None
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_prop = fm.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                break
            except:
                continue
    
    if font_prop:
        # 폰트 파일을 직접 로드하여 설정
        plt.rcParams['font.family'] = font_name
        plt.rcParams['font.sans-serif'] = [font_name, 'Malgun Gothic', '맑은 고딕', 'Arial Unicode MS']
        global_font_prop = font_prop
        print(f"한글 폰트 설정 완료: {font_name} (경로: {font_path})")
    else:
        # 폰트 파일이 없으면 폰트 이름으로 설정
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['font.sans-serif'] = ['Malgun Gothic', '맑은 고딕', 'Arial Unicode MS']
        global_font_prop = fm.FontProperties(family='Malgun Gothic')
        print("한글 폰트 설정 완료: Malgun Gothic (기본 설정)")
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'
    global_font_prop = None

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 스타일 설정
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# seaborn 폰트 설정도 강제로 변경
if platform.system() == 'Windows':
    if global_font_prop:
        sns.set(font=global_font_prop.get_name())
    else:
        sns.set(font='Malgun Gothic')

def load_data(excel_file):
    """엑셀 파일에서 데이터 로드"""
    df = pd.read_excel(excel_file)
    
    # 숫자 데이터 전처리
    numeric_columns = ['내가 살 때(3.75g) - 순금', '내가 팔 때(3.75g) - 순금', 
                      '내가 팔 때(3.75g) - 18K', '내가 팔 때(3.75g) - 14K']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
    
    # 날짜 변환
    df['고시날짜'] = pd.to_datetime(df['고시날짜'], format='%Y.%m.%d', errors='coerce')
    df = df.sort_values('고시날짜').reset_index(drop=True)
    
    return df

def create_time_series_plot(df, output_dir='.'):
    """시계열 라인 차트 생성"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('금 시세 시계열 추이', fontsize=16, fontweight='bold', y=0.995)
    
    # 내가 살 때 - 순금
    axes[0, 0].plot(df['고시날짜'], df['내가 살 때(3.75g) - 순금'], 
                     color='#FF6B6B', linewidth=2, marker='o', markersize=3)
    axes[0, 0].set_title('내가 살 때(3.75g) - 순금', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('날짜')
    axes[0, 0].set_ylabel('가격 (원)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 내가 팔 때 - 순금
    axes[0, 1].plot(df['고시날짜'], df['내가 팔 때(3.75g) - 순금'], 
                     color='#4ECDC4', linewidth=2, marker='o', markersize=3)
    axes[0, 1].set_title('내가 팔 때(3.75g) - 순금', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('날짜')
    axes[0, 1].set_ylabel('가격 (원)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 내가 팔 때 - 18K
    axes[1, 0].plot(df['고시날짜'], df['내가 팔 때(3.75g) - 18K'], 
                     color='#95E1D3', linewidth=2, marker='o', markersize=3)
    axes[1, 0].set_title('내가 팔 때(3.75g) - 18K', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('날짜')
    axes[1, 0].set_ylabel('가격 (원)')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 내가 팔 때 - 14K
    axes[1, 1].plot(df['고시날짜'], df['내가 팔 때(3.75g) - 14K'], 
                     color='#F38181', linewidth=2, marker='o', markersize=3)
    axes[1, 1].set_title('내가 팔 때(3.75g) - 14K', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('날짜')
    axes[1, 1].set_ylabel('가격 (원)')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    filename = f'{output_dir}/1_시계열_추이.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ 생성 완료: {filename}")

def create_comparison_plot(df, output_dir='.'):
    """구매가와 판매가 비교 차트"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(df['고시날짜'], df['내가 살 때(3.75g) - 순금'], 
            label='구매가 (순금)', color='#FF6B6B', linewidth=2.5, marker='o', markersize=4)
    ax.plot(df['고시날짜'], df['내가 팔 때(3.75g) - 순금'], 
            label='판매가 (순금)', color='#4ECDC4', linewidth=2.5, marker='s', markersize=4)
    
    ax.fill_between(df['고시날짜'], df['내가 살 때(3.75g) - 순금'], 
                     df['내가 팔 때(3.75g) - 순금'], 
                     alpha=0.2, color='gray', label='매매 차액')
    
    ax.set_title('순금 구매가 vs 판매가 비교', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('날짜', fontsize=12)
    ax.set_ylabel('가격 (원)', fontsize=12)
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    filename = f'{output_dir}/2_구매가_판매가_비교.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ 생성 완료: {filename}")

def create_box_plot(df, output_dir='.'):
    """박스 플롯 - 가격 분포"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    data_to_plot = [
        df['내가 살 때(3.75g) - 순금'].dropna(),
        df['내가 팔 때(3.75g) - 순금'].dropna(),
        df['내가 팔 때(3.75g) - 18K'].dropna(),
        df['내가 팔 때(3.75g) - 14K'].dropna()
    ]
    
    labels = ['구매가\n(순금)', '판매가\n(순금)', '판매가\n(18K)', '판매가\n(14K)']
    
    bp = ax.boxplot(data_to_plot, tick_labels=labels, patch_artist=True,
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2),
                     whiskerprops=dict(color='black', linewidth=1.5),
                     capprops=dict(color='black', linewidth=1.5))
    
    ax.set_title('금 시세 분포 (박스 플롯)', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('가격 (원)', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    filename = f'{output_dir}/3_가격_분포_박스플롯.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ 생성 완료: {filename}")

def create_histogram(df, output_dir='.'):
    """히스토그램 - 가격 분포"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('금 시세 분포 (히스토그램)', fontsize=16, fontweight='bold', y=0.995)
    
    columns = ['내가 살 때(3.75g) - 순금', '내가 팔 때(3.75g) - 순금',
               '내가 팔 때(3.75g) - 18K', '내가 팔 때(3.75g) - 14K']
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181']
    
    for idx, (col, color) in enumerate(zip(columns, colors)):
        row = idx // 2
        col_idx = idx % 2
        
        data = df[col].dropna()
        axes[row, col_idx].hist(data, bins=20, color=color, alpha=0.7, edgecolor='black')
        axes[row, col_idx].axvline(data.mean(), color='red', linestyle='--', 
                                    linewidth=2, label=f'평균: {data.mean():,.0f}원')
        axes[row, col_idx].axvline(data.median(), color='blue', linestyle='--', 
                                    linewidth=2, label=f'중앙값: {data.median():,.0f}원')
        axes[row, col_idx].set_title(col, fontsize=11, fontweight='bold')
        axes[row, col_idx].set_xlabel('가격 (원)', fontsize=10)
        axes[row, col_idx].set_ylabel('빈도', fontsize=10)
        axes[row, col_idx].legend(fontsize=9)
        axes[row, col_idx].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    filename = f'{output_dir}/4_가격_분포_히스토그램.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ 생성 완료: {filename}")

def create_bar_chart(df, output_dir='.'):
    """막대 그래프 - 평균 가격 비교"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    categories = ['구매가\n(순금)', '판매가\n(순금)', '판매가\n(18K)', '판매가\n(14K)']
    means = [
        df['내가 살 때(3.75g) - 순금'].mean(),
        df['내가 팔 때(3.75g) - 순금'].mean(),
        df['내가 팔 때(3.75g) - 18K'].mean(),
        df['내가 팔 때(3.75g) - 14K'].mean()
    ]
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181']
    
    bars = ax.bar(categories, means, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # 값 표시
    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{mean:,.0f}원',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_title('평균 가격 비교', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('가격 (원)', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    filename = f'{output_dir}/5_평균_가격_비교.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ 생성 완료: {filename}")

def create_scatter_plot(df, output_dir='.'):
    """산점도 - 구매가 vs 판매가 관계"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    buy_price = df['내가 살 때(3.75g) - 순금'].dropna()
    sell_price = df['내가 팔 때(3.75g) - 순금'].dropna()
    
    # 같은 인덱스만 사용
    min_len = min(len(buy_price), len(sell_price))
    buy_price = buy_price.iloc[:min_len]
    sell_price = sell_price.iloc[:min_len]
    
    ax.scatter(buy_price, sell_price, alpha=0.6, s=50, color='#4ECDC4', edgecolors='black', linewidth=0.5)
    
    # 1:1 선 추가
    min_val = min(buy_price.min(), sell_price.min())
    max_val = max(buy_price.max(), sell_price.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='1:1 선')
    
    ax.set_title('구매가 vs 판매가 산점도', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('구매가 (순금, 원)', fontsize=12)
    ax.set_ylabel('판매가 (순금, 원)', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = f'{output_dir}/6_구매가_판매가_산점도.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ 생성 완료: {filename}")

def create_statistics_summary(df, output_dir='.'):
    """통계 요약 차트"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    # 통계값 계산
    stats_data = []
    columns = ['내가 살 때(3.75g) - 순금', '내가 팔 때(3.75g) - 순금',
               '내가 팔 때(3.75g) - 18K', '내가 팔 때(3.75g) - 14K']
    labels = ['구매가 (순금)', '판매가 (순금)', '판매가 (18K)', '판매가 (14K)']
    
    for col, label in zip(columns, labels):
        data = df[col].dropna()
        stats_data.append({
            '항목': label,
            '평균': data.mean(),
            '최대값': data.max(),
            '최소값': data.min(),
            '중앙값': data.median(),
            '표준편차': data.std()
        })
    
    # 테이블 생성
    table_data = []
    headers = ['항목', '평균', '최대값', '최소값', '중앙값', '표준편차']
    
    for stat in stats_data:
        table_data.append([
            stat['항목'],
            f"{stat['평균']:,.0f}",
            f"{stat['최대값']:,.0f}",
            f"{stat['최소값']:,.0f}",
            f"{stat['중앙값']:,.0f}",
            f"{stat['표준편차']:,.0f}"
        ])
    
    table = ax.table(cellText=table_data, colLabels=headers,
                     cellLoc='center', loc='center',
                     colWidths=[0.25, 0.15, 0.15, 0.15, 0.15, 0.15])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # 헤더 스타일
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#366092')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # 데이터 행 스타일
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#D9E1F2')
            else:
                table[(i, j)].set_facecolor('#FFFFFF')
    
    ax.set_title('금 시세 통계 요약', fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    filename = f'{output_dir}/7_통계_요약.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ 생성 완료: {filename}")

def main():
    """메인 함수"""
    # 가장 최근 엑셀 파일 찾기
    files = glob.glob("금시세_*.xlsx")
    if not files:
        print("엑셀 파일을 찾을 수 없습니다.")
        return
    
    # 통계 분석 파일 제외
    files = [f for f in files if '_통계분석' not in f]
    if not files:
        print("분석할 파일을 찾을 수 없습니다.")
        return
    
    excel_file = max(files)
    print(f"데이터 파일: {excel_file}\n")
    
    # 데이터 로드
    df = load_data(excel_file)
    print(f"총 {len(df)}개의 데이터 로드 완료\n")
    
    # 시각화 생성
    print("시각화 이미지 생성 중...\n")
    
    create_time_series_plot(df)
    create_comparison_plot(df)
    create_box_plot(df)
    create_histogram(df)
    create_bar_chart(df)
    create_scatter_plot(df)
    create_statistics_summary(df)
    
    print(f"\n모든 시각화 이미지 생성 완료! (총 7개)")

if __name__ == "__main__":
    main()

