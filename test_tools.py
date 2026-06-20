from dotenv import load_dotenv
load_dotenv()

from agent.tools.github import github_reviewer
from agent.tools.roadmap import roadmap_generator

print("=== ROADMAP ===")
result = roadmap_generator.invoke({
    "goal": "Backend Developer",
    "level": "beginner"
})
print(result)

print("\n=== GITHUB REVIEW ===")
result = github_reviewer.invoke({
    "repo_url": "https://github.com/torvalds/linux",
    "level": "beginner"
})
print(result)