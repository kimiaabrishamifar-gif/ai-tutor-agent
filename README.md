# 🎓 دستیار آموزشی هوشمند برنامه‌نویسی

یک AI Agent آموزشی مبتنی بر LangChain که با توجه به سطح دانشجو، توضیحات شخصی‌سازی شده ارائه می‌دهد، کوییز تولید می‌کند، کد می‌نویسد، مسیر یادگیری طراحی می‌کند و پروژه‌های GitHub را بررسی می‌کند.

---

## ✨ قابلیت‌ها

| ابزار | توضیح | مثال |
|-------|--------|-------|
| 🧪 Quiz Generator | تولید کوییز ۵ سوالی از هر موضوع | `یه کوییز درباره React Hooks بساز` |
| 💻 Code Generator | تولید کد آموزشی با توضیح فارسی | `یه مثال FastAPI CRUD بنویس` |
| 🔍 GitHub Reviewer | بررسی پروژه‌های GitHub و بازخورد | `این ریپو رو بررسی کن: github.com/...` |
| 🗺️ Roadmap Generator | مسیر یادگیری شخصی‌سازی شده | `مسیر یادگیری Backend Developer بساز` |

---

## 🧠 Middleware ها

- **Student Level Middleware** — پاسخ‌ها بر اساس سطح دانشجو (Beginner / Intermediate / Advanced) تنظیم می‌شوند
- **Conversation Memory** — تاریخچه مکالمه ذخیره و در صورت طولانی شدن خلاصه می‌شود
- **Context Management** — سطح، موضوعات مطالعه شده و علاقه‌مندی‌های کاربر ذخیره می‌شود

---

## 🏗️ معماری پروژه

```
ai-tutor/
├── main.py                    # FastAPI Server
├── index.html                 # رابط کاربری چت
├── agent/
│   ├── agent.py               # Agent اصلی (LangChain)
│   └── tools/
│       ├── quiz.py            # Quiz Generator Tool
│       ├── code_gen.py        # Code Generator Tool
│       ├── github.py          # GitHub Reviewer Tool
│       └── roadmap.py         # Roadmap Generator Tool
└── middleware/
    ├── student_level.py       # Student Level Middleware
    └── memory.py              # Conversation Memory
```

---

## 🛠️ تکنولوژی‌ها

- **LangChain** — ساخت Agent و Tools
- **FastAPI** — Backend API
- **OpenAI GPT-4o-mini** — مدل زبانی
- **GitHub API** — دریافت اطلاعات ریپو
- **HTML/CSS/JS** — رابط کاربری

---

## 🚀 راه‌اندازی

### ۱. نصب پیش‌نیازها

```bash
git clone https://github.com/kimiaabrishamifar-gif/ai-tutor-agent
cd ai-tutor-agent
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### ۲. تنظیم کلید API

یک فایل `.env` در پوشه پروژه بساز:

```
OPENAI_API_KEY=your_api_key_here
```

### ۳. اجرای سرور

```bash
uvicorn main:app --reload
```

سرور روی `http://localhost:8000` اجرا می‌شود.

### ۴. استفاده از رابط کاربری

فایل `index.html` را در مرورگر باز کن.

---

## 📡 API Endpoints

| Method | Endpoint | توضیح |
|--------|----------|--------|
| `POST` | `/chat` | ارسال پیام به Agent |
| `POST` | `/set-level` | تغییر سطح دانشجو |
| `GET` | `/context` | دریافت context فعلی کاربر |
| `GET` | `/docs` | مستندات Swagger UI |

### نمونه Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "یه کوییز درباره Python بساز", "level": "beginner"}'
```

---

## 📊 نمونه خروجی

**Quiz Generator:**
```
سوال ۱: برای افزودن یک عنصر به انتهای لیست از کدام متد استفاده می‌شود؟
الف) add()
ب) append()  ✓
ج) insert()
د) extend()
```

**Roadmap Generator:**
```
مرحله ۱ — پایه (۲-۴ هفته)
- مبانی Python
- آشنایی با HTTP و REST
- منبع: Automate the Boring Stuff with Python
```

---

## 📋 معیارهای ارزیابی

| بخش | پیاده‌سازی |
|-----|-----------|
| Agent اصلی | ✅ LangChain با bind_tools |
| Quiz Generator | ✅ |
| Code Generator | ✅ |
| GitHub Reviewer | ✅ GitHub API |
| Roadmap Generator | ✅ |
| Student Level Middleware | ✅ |
| Context & Memory | ✅ ConversationMemory |
| رابط کاربری | ✅ Chat UI |
