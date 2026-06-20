from dotenv import load_dotenv
load_dotenv()  # ← این باید خط دوم باشه، قبل از بقیه
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini",base_url="https://api.metisai.ir/openai/v1")
    

@tool
def code_generator(topic: str, level: str = "beginner") -> str:
    """کد آموزشی با توضیح کامل تولید می‌کنه"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", """تو یه معلم برنامه‌نویسی هستی.
کد رو به این فرمت بده:

## توضیح
(توضیح ساده موضوع)

## کد
```python
(کد کامل با کامنت فارسی)
```

## خروجی
(خروجی مورد انتظار)

## نکات مهم
(۲-۳ نکته کلیدی)"""),
        ("user", "موضوع: {topic}\nسطح: {level}\n\nکد آموزشی بنویس.")
    ])

    chain = prompt | llm
    response = chain.invoke({"topic": topic, "level": level})
    return response.content