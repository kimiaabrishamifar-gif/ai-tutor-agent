def get_level_instructions(level: str) -> str:
    """بر اساس سطح دانشجو، دستورالعمل مناسب برمی‌گردونه"""

    instructions = {
        "beginner": """
- از کلمات ساده استفاده کن
- هر مفهوم جدید رو با مثال توضیح بده
- از اصطلاحات فنی پیچیده پرهیز کن
- کدها رو خط به خط توضیح بده
""",
        "intermediate": """
- می‌تونی از اصطلاحات فنی استفاده کنی
- روی best practices تمرکز کن
- مثال‌های واقعی‌تر بزن
- چالش‌های رایج رو هم ذکر کن
""",
        "advanced": """
- توضیحات فنی و عمیق بده
- به performance و optimization اشاره کن
- edge case ها رو بررسی کن
- با design pattern ها آشنا هستی
"""
    }

    return instructions.get(level, instructions["beginner"])


def build_system_prompt(base_prompt: str, level: str) -> str:
    """یه system prompt کامل با در نظر گرفتن سطح دانشجو می‌سازه"""

    level_instructions = get_level_instructions(level)

    return f"""{base_prompt}

سطح دانشجو: {level}
دستورالعمل‌های تدریس:
{level_instructions}
"""