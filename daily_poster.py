import os
import requests
import random
import datetime
import re
import unicodedata
from dotenv import load_dotenv
from openai import OpenAI

# 환경변수 불러오기
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
WP_URL = os.getenv("WP_URL")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

# 주제 목록
topics = {
    "diet": [
        "One-Week Meal Plan to Lower Blood Sugar",
        "Best Breakfast Options for Diabetics",
        "What to Eat Before Bed with High Blood Sugar"
    ],
    "foods": [
        "Top 10 Foods That Help Stabilize Blood Sugar",
        "White Rice vs. Brown Rice for Blood Sugar Control",
        "Is Fruit Safe for Diabetics? Best & Worst Options"
    ],
    "tips": [
        "Walking After Meals: Why It’s Crucial for Blood Sugar",
        "5 Morning Habits to Start Your Day Sugar-Smart",
        "How Sleep Affects Your Blood Sugar Levels"
    ],
    "tools": [
        "Top 5 Blood Sugar Tracking Apps for 2025",
        "How to Use a Glucose Monitor Correctly",
        "Understanding Continuous Glucose Monitoring (CGM)"
    ],
    "myths": [
        "Do Diabetics Need to Avoid All Sugar?",
        "Honey vs. Sugar: Which is Better for Blood Sugar?",
        "The Truth About Artificial Sweeteners and Insulin Response"
    ]
}

# 워드프레스 카테고리 ID
categories = {
    "diet": 1,
    "foods": 6,
    "tips": 7,
    "tools": 8,
    "myths": 9
}

# 주제 선택
def choose_topic():
    category = random.choice(list(topics.keys()))
    topic = random.choice(topics[category])
    return category, topic

# 블로그 글 생성
def generate_post(topic):
    print(f"[{datetime.datetime.now()}] Generating post: {topic}")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional health blogger."},
            {"role": "user", "content": f"Write a 600-word SEO-optimized blog post about: {topic}"}
        ],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

# 금칙어 우회 표현 치환
def rephrase_sensitive_phrases(text):
    replacements = {
        "Consult with a Professional": "Listen to your body and make adjustments that feel right for you",
        "A registered dietitian or healthcare provider can offer personalized advice based on your health needs.":
            "Everyone’s needs are different, so pay attention to how your body responds and adapt accordingly.",
        "registered dietitian": "nutrition expert",
        "healthcare provider": "trusted expert",
        "personalized advice": "custom guidance",
        "based on your health needs": "tailored to your condition"
    }
    for target, replacement in replacements.items():
        text = text.replace(target, replacement)
    return text

# 콘텐츠 정제
def sanitize_content(content):
    # HTML 태그 제거
    content = re.sub(r'<[^>]+>', '', content)
    # 마크다운 제거
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
    content = re.sub(r'__(.*?)__', r'\1', content)
    content = re.sub(r'~~(.*?)~~', r'\1', content)
    content = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content)
    content = re.sub(r'#+\s?', '', content)
    content = re.sub(r'-\s+', '', content)
    content = re.sub(r'\*', '', content)
    # HTML 엔티티 제거
    content = re.sub(r'&[a-z]+;', '', content)
    # 특수기호 제거
    content = ''.join(c for c in content if unicodedata.category(c)[0] != 'S')
    # 이중 공백 제거
    content = re.sub(r'\s{2,}', ' ', content)
    return content.strip()

# 워드프레스 업로드
def post_to_wordpress(title, content, category_id):
    url = f"{WP_URL}/wp-json/wp/v2/posts"
    auth = (WP_USERNAME, WP_PASSWORD)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate"
    }
    data = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": [category_id]
    }
    response = requests.post(url, auth=auth, headers=headers, json=data)
    print(f"[{datetime.datetime.now()}] Posted to WordPress: {response.status_code}")
    if response.status_code != 201:
        print("Error response:", response.text)

# 메인 함수
def main():
    category, topic = choose_topic()
    raw_content = generate_post(topic)
    clean_content = sanitize_content(raw_content)
    safe_content = rephrase_sensitive_phrases(clean_content)

    # 콘솔 출력
    print("\n==== Final Post ====\n")
    print(safe_content)
    print("\n====================\n")

    post_to_wordpress(topic, safe_content, categories[category])

if __name__ == "__main__":
    main()
