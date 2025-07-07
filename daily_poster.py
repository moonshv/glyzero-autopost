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
categ
