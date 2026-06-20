from dotenv import load_dotenv
load_dotenv()  
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini",base_url="https://api.metisai.ir/openai/v1")
    

@tool
def quiz_generator(topic: str, level: str = "beginner") -> str:
    """یه کوییز ۵ سوالی درباره موضوع موردنظر تولید می‌کنه"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", """تو یه معلم برنامه‌نویسی هستی.
کوییز رو به این فرمت دقیق بساز:

سوال ۱: ...
الف) ...
ب) ...
ج) ...
د) ...
جواب: الف

و همینطور تا سوال ۵"""),
        ("user", "موضوع: {topic}\nسطح: {level}\n\nیه کوییز ۵ سوالی بساز.")
    ])

    chain = prompt | llm
    response = chain.invoke({"topic": topic, "level": level})
    return response.content