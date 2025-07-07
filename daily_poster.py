import os
import requests
import random
import datetime
import re
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

# 콘텐츠 필터링 (406 오류 회피 목적)
def sanitize_content(content):
    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<(iframe|embed|object).*?>.*?</\1>', '', content, flags=re.DOTALL)
    content = re.sub(r'<.*?>', '', content)  # 모든 HTML 태그 제거
    content = re.sub(r'javascript:', '', content, flags=re.IGNORECASE)
    content = re.sub(r'on\w+=".*?"', '', content)
    return content

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

# 메인 실행 함수
def main():
    category, topic = choose_topic()
    raw_content = generate_post(topic)
    clean_content = sanitize_content(raw_content)
    
    # 생성된 글 콘솔에 출력 (테스트용)
    print("\n==== Generated Content ====\n")
    print(clean_content)
    print("\n===========================\n")
    
    post_to_wordpress(topic, clean_content, categories[category])
    
    post_to_wordpress(topic, clean_content, categories[category])

if __name__ == "__main__":
    main()
