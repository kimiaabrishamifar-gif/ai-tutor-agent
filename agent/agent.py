from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool

from agent.tools.quiz import quiz_generator
from agent.tools.code_gen import code_generator
from agent.tools.github import github_reviewer
from agent.tools.roadmap import roadmap_generator
from middleware.student_level import build_system_prompt
from middleware.memory import ConversationMemory

load_dotenv()

tools = [quiz_generator, code_generator, github_reviewer, roadmap_generator]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://api.metisai.ir/openai/v1"
)

# مدل رو به tools وصل می‌کنیم — روش جدید LangChain
llm_with_tools = llm.bind_tools(tools)

class TutorAgent:
    def __init__(self):
        self.memory = ConversationMemory()
        self.tools_map = {t.name: t for t in tools}

    def chat(self, user_message: str) -> str:
        level = self.memory.user_context["level"]
        context = self.memory.get_context_summary()

        system_prompt = build_system_prompt(f"""
تو یه دستیار آموزشی هوشمند برای یادگیری برنامه‌نویسی هستی.
همیشه به فارسی جواب بده.

ابزارهایی که داری:
- quiz_generator: برای ساخت کوییز
- code_generator: برای نوشتن کد آموزشی  
- github_reviewer: برای بررسی پروژه‌های GitHub
- roadmap_generator: برای ساخت مسیر یادگیری

اطلاعات کاربر:
{context}
""", level)

        # ساخت تاریخچه پیام‌ها
        messages = [SystemMessage(content=system_prompt)]
        for msg in self.memory.messages:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        messages.append(HumanMessage(content=user_message))

        # مرحله ۱: مدل تصمیم می‌گیره از کدوم tool استفاده کنه
        response = llm_with_tools.invoke(messages)

        # مرحله ۲: اگه tool call داشت، اجراش کن
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"[Agent] از tool استفاده می‌کنه: {tool_name}")
            print(f"[Agent] با آرگومان‌ها: {tool_args}")

            # tool رو پیدا کن و اجرا کن
            selected_tool = self.tools_map[tool_name]
            tool_result = selected_tool.invoke(tool_args)

            # نتیجه رو به مدل بده تا پاسخ نهایی بسازه
            from langchain_core.messages import ToolMessage
            messages.append(response)
            messages.append(ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            ))

            final_response = llm_with_tools.invoke(messages)
            result = final_response.content
        else:
            result = response.content

        # ذخیره در memory
        self.memory.add_message("user", user_message)
        self.memory.add_message("assistant", result)

        return result

    def set_level(self, level: str):
        self.memory.update_context("level", level)
        return f"سطح به {level} تغییر کرد."