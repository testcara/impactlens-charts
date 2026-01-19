from google import genai
from pathlib import Path
import os
import sys

# -----------------------------
# 1️⃣ API Key 检查
# -----------------------------
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not set")
    sys.exit(1)

# -----------------------------
# 2️⃣ 读取 prompt
# -----------------------------
prompt_file = Path("prompt.txt")
if not prompt_file.exists():
    print("❌ prompt.txt 不存在")
    sys.exit(1)

prompt = prompt_file.read_text().strip()

# -----------------------------
# 3️⃣ 初始化客户端
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# 4️⃣ 获取可用模型并选择最先进
# -----------------------------
try:
    models = client.models.list()
except Exception as e:
    print("❌ 获取模型列表失败:", e)
    sys.exit(1)

candidate_models = [m for m in models if 'gemini' in m.name.lower() and ('pro' in m.name.lower() or 'flash' in m.name.lower())]

if not candidate_models:
    print("⚠️ 没有找到 advanced 模型，使用 fallback gemini-1.5-flash")
    model_name = "gemini-1.5-flash"
else:
    model_name = sorted(candidate_models, key=lambda m: m.name)[-1].name

print("✅ 使用模型:", model_name)

# -----------------------------
# 5️⃣ 调用模型
# -----------------------------
try:
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
except Exception as e:
    print("❌ 模型调用失败:", e)
    sys.exit(1)

# -----------------------------
# 6️⃣ 输出
# -----------------------------
output_text = response.text
print("📝 Gemini response:")
print(output_text)

# 保存到文件
output_file = Path("output.txt")
output_file.write_text(output_text)
print(f"✅ 输出已保存到 {output_file}")

