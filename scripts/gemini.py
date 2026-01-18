from google import genai
from pathlib import Path
import os
import sys

# 1️⃣ 读取 API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not set")
    sys.exit(1)

# 2️⃣ 读取 prompt 文件
prompt_path = Path("prompt.txt")
prompt = prompt_path.read_text().strip()

# 3️⃣ 初始化 Gemini client
client = genai.Client(api_key=api_key)

# 4️⃣ 调用模型（不要 list models）
response = client.models.generate_content(
    model="gemini-1.5-pro-latest",
    contents=prompt,
)

# 5️⃣ 输出结果（GitHub Actions 日志可见）
print("📝 Gemini response:")
print(response.text)

