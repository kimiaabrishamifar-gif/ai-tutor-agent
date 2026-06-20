from dotenv import load_dotenv
load_dotenv()  # ← این باید خط دوم باشه، قبل از بقیه
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import requests



llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://api.metisai.ir/openai/v1"
)

def get_repo_info(repo_url: str) -> dict:
    """اطلاعات ریپو رو از GitHub API می‌گیره"""
    # استخراج username/reponame از URL
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    headers = {"Accept": "application/vnd.github.v3+json"}

    # اطلاعات کلی ریپو
    repo_data = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}",
        headers=headers
    ).json()

    # لیست فایل‌های ریپو
    contents = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/contents",
        headers=headers
    ).json()

    file_names = []
    if isinstance(contents, list):
        file_names = [f["name"] for f in contents]

    return {
        "name": repo_data.get("name", ""),
        "description": repo_data.get("description", "بدون توضیح"),
        "language": repo_data.get("language", "نامشخص"),
        "stars": repo_data.get("stargazers_count", 0),
        "files": file_names
    }

@tool
def github_reviewer(repo_url: str, level: str = "beginner") -> str:
    """یه ریپوی GitHub رو بررسی می‌کنه و بازخورد آموزشی میده"""

    repo_info = get_repo_info(repo_url)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """تو یه مدرس برنامه‌نویسی هستی که پروژه‌های دانشجوها رو بررسی می‌کنی.
بازخورد رو به این فرمت بده:

## خلاصه پروژه
(یه توضیح کوتاه)

## نکات مثبت
(چی خوبه)

## پیشنهادات بهبود
(چی رو می‌تونه بهتر کنه)

## امتیاز کلی
(از ۱۰)"""),
        ("user", """پروژه: {name}
توضیح: {description}
زبان: {language}
فایل‌ها: {files}
سطح دانشجو: {level}

این پروژه رو بررسی کن.""")
    ])

    chain = prompt | llm
    response = chain.invoke({
        "name": repo_info["name"],
        "description": repo_info["description"],
        "language": repo_info["language"],
        "files": ", ".join(repo_info["files"]),
        "level": level
    })
    return response.content