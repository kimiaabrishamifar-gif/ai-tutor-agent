from dotenv import load_dotenv
load_dotenv()  # ← این باید خط دوم باشه، قبل از بقیه
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate



llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://api.metisai.ir/openai/v1"
)

@tool
def roadmap_generator(goal: str, level: str = "beginner") -> str:
    """مسیر یادگیری شخصی‌سازی شده تولید می‌کنه"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", """تو یه مشاور آموزش برنامه‌نویسی هستی.
مسیر یادگیری رو به این فرمت بده:

## هدف
(هدف نهایی)

## مرحله ۱ — پایه (۲-۴ هفته)
- موضوع ۱
- موضوع ۲
- منبع پیشنهادی

## مرحله ۲ — میانی (۴-۸ هفته)
- موضوع ۱
- موضوع ۲
- منبع پیشنهادی

## مرحله ۳ — پیشرفته (۸-۱۲ هفته)
- موضوع ۱
- موضوع ۲
- منبع پیشنهادی

## پروژه‌های پیشنهادی
(۲-۳ پروژه برای تمرین)"""),
        ("user", "هدف: {goal}\nسطح فعلی: {level}\n\nمسیر یادگیری بساز.")
    ])

    chain = prompt | llm
    response = chain.invoke({"goal": goal, "level": level})
    return response.content