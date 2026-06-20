from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://api.metisai.ir/openai/v1"
)

class ConversationMemory:
    def __init__(self, max_messages: int = 10):
        self.messages = []          # تاریخچه پیام‌ها
        self.max_messages = max_messages
        self.user_context = {       # اطلاعات کاربر
            "level": "beginner",
            "topics_studied": [],
            "preferred_language": "python"
        }

    def add_message(self, role: str, content: str):
        """پیام جدید اضافه می‌کنه"""
        self.messages.append({"role": role, "content": content})

        # اگه پیام‌ها زیاد شدن، خلاصه می‌کنه
        if len(self.messages) > self.max_messages:
            self._summarize()

    def _summarize(self):
        """وقتی مکالمه طولانی شد، خلاصه می‌کنه"""
        history_text = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in self.messages[:-4]  # آخرین ۴ پیام رو نگه می‌داره
        ])

        summary_response = llm.invoke([
            SystemMessage(content="خلاصه‌ای کوتاه از این مکالمه به فارسی بنویس:"),
            HumanMessage(content=history_text)
        ])

        # جایگزین کردن پیام‌های قدیمی با خلاصه
        self.messages = [
            {"role": "system", "content": f"خلاصه مکالمه قبلی: {summary_response.content}"},
            *self.messages[-4:]  # فقط آخرین ۴ پیام
        ]

    def update_context(self, key: str, value):
        """اطلاعات کاربر رو آپدیت می‌کنه"""
        self.user_context[key] = value

    def get_context_summary(self) -> str:
        """خلاصه context کاربر رو برمی‌گردونه"""
        topics = ", ".join(self.user_context["topics_studied"]) or "هنوز موضوعی مطالعه نشده"
        return f"""
سطح: {self.user_context['level']}
موضوعات مطالعه شده: {topics}
زبان مورد علاقه: {self.user_context['preferred_language']}
"""