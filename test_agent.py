from agent.agent import TutorAgent

agent = TutorAgent()

# تست ۱ — سوال ساده
print("=== TEST 1 ===")
response = agent.chat("یه کوییز درباره Python lists بساز")
print(response)

# تست ۲ — تغییر سطح
print("\n=== TEST 2 ===")
agent.set_level("advanced")
response = agent.chat("مسیر یادگیری برای تبدیل شدن به Backend Developer بساز")
print(response)