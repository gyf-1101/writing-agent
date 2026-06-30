import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

def test_api():
    try:
        response = client.chat.completions.create(
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            messages=[
                {"role": "user", "content": "用一句话解释什么是 AI Agent"}
            ]
        )
        print("✅ DeepSeek API 调用成功！")
        print("🤖 回复：", response.choices[0].message.content)
    except Exception as e:
        print("❌ 调用失败：", e)

if __name__ == "__main__":
    test_api()
