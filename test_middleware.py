from middleware.student_level import build_system_prompt
from middleware.memory import ConversationMemory

# تست Student Level
print("=== STUDENT LEVEL ===")
prompt = build_system_prompt("تو یه معلم برنامه‌نویسی هستی.", "beginner")
print(prompt)

print("\n=== MEMORY ===")
memory = ConversationMemory()
memory.add_message("user", "useEffect چیه؟")
memory.add_message("assistant", "useEffect یه hook در React هست...")
memory.update_context("level", "intermediate")
memory.update_context("topics_studied", ["React", "useEffect"])

print(memory.get_context_summary())