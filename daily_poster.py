
import os
import requests
import random
import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
WP_URL = os.getenv("WP_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

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

categories = {
    "diet": 2,
    "foods": 3,
    "tips": 4,
    "tools": 5,
    "myths": 6
}

def choose_topic():
    category = random.choice(list(topics.keys()))
    topic = random.choice(topics[category])
    return category, topic

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

def post_to_wordpress(title, content, category_id):
    url = f"{WP_URL}/wp-json/wp/v2/posts"
    auth = (WP_USERNAME, WP_PASSWORD)
    data = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": [category_id]
    }
    response = requests.post(url, auth=auth, json=data)
    print(f"[{datetime.datetime.now()}] Posted to WordPress: {response.status_code}")
    if response.status_code != 201:
        print("Error response:", response.text)

def main():
    category, topic = choose_topic()
    content = generate_post(topic)
    post_to_wordpress(topic, content, categories[category])

if __name__ == "__main__":
    main()
