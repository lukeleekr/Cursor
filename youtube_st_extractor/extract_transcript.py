"""
YouTube Transcript Extractor
Extracts subtitles from YouTube videos using youtube-transcript-api with proxy support.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from openai import OpenAI


def extract_video_id(url: str) -> str:
    """
    Extract video ID from YouTube URL.
    
    Args:
        url: YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
    
    Returns:
        Video ID string
    """
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        # Assume it's already a video ID
        return url


def detect_multilingual(text: str) -> bool:
    """
    Detect if text contains both Korean and English.
    
    Args:
        text: Text to check
    
    Returns:
        True if text contains both Korean and English characters
    """
    has_korean = any('\uac00' <= char <= '\ud7a3' for char in text)
    has_english = any(char.isalpha() and ord(char) < 128 for char in text)
    return has_korean and has_english


def check_spelling_with_gpt(text: str, api_key: str, language: str = "ko") -> str:
    """
    Check spelling and grammar of text using GPT model with language-specific formatting.
    Handles multilingual text (e.g., Korean + English) by correcting each language separately.
    
    Args:
        text: Text to check
        api_key: OpenAI API key
        language: Language code (e.g., 'ko', 'en')
    
    Returns:
        Corrected text with proper paragraph breaks
    """
    client = OpenAI(api_key=api_key)
    
    # Check if text is multilingual (Korean + English)
    is_multilingual = detect_multilingual(text)
    
    if is_multilingual:
        # Multilingual prompt (Korean + English)
        system_prompt = "You are an expert in both Korean and English spelling, grammar, and punctuation. You correct each language according to its own rules without translating. You improve readability by adding natural paragraph breaks while maintaining the original meaning and tone."
        user_prompt = """다음 텍스트는 한국어와 영어가 섞여 있습니다. 각 언어의 맞춤법, 띄어쓰기, 문법을 해당 언어의 규칙에 맞게 교정해주세요.
중요: 절대로 번역하지 마세요. 한국어는 한국어로, 영어는 영어로 그대로 유지하면서 각각의 맞춤법과 문법만 수정해주세요.
또한 자연스러운 흐름에 따라 문단을 나누어 가독성을 높여주세요.
원문의 의미와 톤은 그대로 유지하면서, 문맥에 맞게 문단을 구분하고 각 언어의 맞춤법과 띄어쓰기를 정확하게 수정해주세요.
수정된 텍스트만 출력하고, 다른 설명이나 주석은 포함하지 마세요.

Text:
{text}"""
    elif language == "ko":
        system_prompt = "당신은 한국어 맞춤법, 띄어쓰기, 문법을 검사하고 수정하는 전문가입니다. 텍스트의 의미와 톤을 유지하면서 자연스러운 문단 구분을 추가하여 가독성을 높입니다."
        user_prompt = """다음 한국어 텍스트의 맞춤법, 띄어쓰기, 문법을 검사하고 수정해주세요. 
또한 자연스러운 흐름에 따라 문단을 나누어 가독성을 높여주세요. 
원문의 의미와 톤은 그대로 유지하면서, 문맥에 맞게 문단을 구분하고 맞춤법과 띄어쓰기를 정확하게 수정해주세요.
수정된 텍스트만 출력하고, 다른 설명이나 주석은 포함하지 마세요.

텍스트:
{text}"""
    elif language == "en":
        system_prompt = "You are an expert in English spelling, grammar, and punctuation. You improve readability by adding natural paragraph breaks while maintaining the original meaning and tone."
        user_prompt = """Please check and correct the spelling, grammar, and punctuation of the following English text.
Also, divide the text into natural paragraphs to improve readability based on the flow and context.
Maintain the original meaning and tone while correcting grammar and spelling accurately.
Output only the corrected text without any explanations or comments.

Text:
{text}"""
    else:
        # Default to English for other languages
        system_prompt = f"You are an expert in {language} language spelling, grammar, and punctuation. You improve readability by adding natural paragraph breaks while maintaining the original meaning and tone."
        user_prompt = f"""Please check and correct the spelling, grammar, and punctuation of the following {language} text.
Also, divide the text into natural paragraphs to improve readability based on the flow and context.
Maintain the original meaning and tone while correcting grammar and spelling accurately.
Output only the corrected text without any explanations or comments.

Text:
{text}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt.format(text=text)
                }
            ],
            temperature=0.3
        )
        
        corrected_text = response.choices[0].message.content.strip()
        return corrected_text
    
    except Exception as e:
        print(f"Error during spelling check: {e}")
        return text  # 오류 발생 시 원본 텍스트 반환


def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get proxy credentials from environment variables
    proxy_username = os.getenv("PROXY_USERNAME")
    proxy_password = os.getenv("PROXY_PASSWORD")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not proxy_username or not proxy_password:
        raise ValueError(
            "PROXY_USERNAME and PROXY_PASSWORD must be set in .env file"
        )
    
    if not openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY must be set in .env file"
        )
    
    # Get YouTube video URL from user input
    print("=" * 80)
    print("YouTube Transcript Extractor")
    print("=" * 80)
    print()
    video_url = input("Please enter the YouTube video URL: ").strip()
    
    if not video_url:
        raise ValueError("YouTube URL is required")
    
    video_id = extract_video_id(video_url)
    
    print(f"\nExtracting transcript for video ID: {video_id}")
    print(f"Video URL: {video_url}\n")
    
    # Initialize YouTube Transcript API with Webshare proxy configuration
    ytt_api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username=proxy_username,
            proxy_password=proxy_password,
        )
    )
    
    try:
        # Try to fetch transcript in preferred languages (ko, en)
        transcript_data = None
        transcript_language = None
        
        # Try Korean first
        try:
            transcript_data = ytt_api.fetch(video_id, languages=['ko'])
            transcript_language = 'ko'
            print("Using Korean transcript\n")
        except:
            # Try English
            try:
                transcript_data = ytt_api.fetch(video_id, languages=['en'])
                transcript_language = 'en'
                print("Using English transcript\n")
            except:
                # Fall back to default (any available language)
                try:
                    transcript_data = ytt_api.fetch(video_id)
                    # Try to detect language from text (simple heuristic)
                    # For now, default to 'en' if not Korean
                    full_text_temp = " ".join(snippet.text for snippet in transcript_data.snippets[:10])
                    # Simple language detection: if contains Korean characters, assume Korean
                    if any('\uac00' <= char <= '\ud7a3' for char in full_text_temp):
                        transcript_language = 'ko'
                    else:
                        transcript_language = 'en'
                    print(f"Using default transcript (Detected language: {transcript_language})\n")
                except Exception as e:
                    raise Exception(f"Could not fetch transcript: {e}")
        
        print("=" * 80)
        print("ORIGINAL TRANSCRIPT")
        print("=" * 80)
        print()
        
        # Combine all transcript snippets into one continuous text
        full_text = " ".join(snippet.text for snippet in transcript_data.snippets)
        print(full_text)
        
        print()
        print("=" * 80)
        print(f"Total snippets: {len(transcript_data.snippets)}")
        print(f"Language: {transcript_language}")
        print("=" * 80)
        print()
        
        # Check if text is multilingual
        is_multilingual = detect_multilingual(full_text)
        if is_multilingual:
            print(f"Checking spelling and grammar with GPT (Multilingual: Korean + English)...")
        else:
            print(f"Checking spelling and grammar with GPT (Language: {transcript_language})...")
        corrected_text = check_spelling_with_gpt(full_text, openai_api_key, transcript_language)
        
        print()
        print("=" * 80)
        print("CORRECTED TRANSCRIPT")
        print("=" * 80)
        print()
        print(corrected_text)
        print()
        print("=" * 80)
        
        # Save to markdown file
        output_filename = f"transcript_{video_id}.md"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(f"# YouTube Transcript\n\n")
            f.write(f"**Video ID:** {video_id}\n\n")
            f.write(f"**Video URL:** {video_url}\n\n")
            f.write(f"**Language:** {transcript_language}\n\n")
            f.write(f"**Extracted Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Snippets:** {len(transcript_data.snippets)}\n\n")
            f.write(f"---\n\n")
            f.write(f"## Corrected Transcript\n\n")
            f.write(corrected_text)
            f.write(f"\n\n---\n\n")
            f.write(f"## Original Transcript\n\n")
            f.write(full_text)
        
        print(f"\n✅ Transcript saved to: {output_filename}")
        
    except Exception as e:
        print(f"Error extracting transcript: {e}")
        raise


if __name__ == "__main__":
    main()

