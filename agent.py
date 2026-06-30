import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import *

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

TOOLS = {
    "parse_outline": parse_outline,
    "write_section": write_section,
    "check_logic": check_logic,
    "check_consistency": check_consistency,
    "save_preference": save_preference,
    "export_doc": export_doc
}

def run_agent(user_input: str):
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个写作助手 Agent。"
                "你必须根据用户需求，决定调用哪个工具。"
                "只能输出 JSON，格式如下：\n"
                '{ "tool": "write_section", "args": { "title": "引言" } }'
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    decision = json.loads(response.choices[0].message.content)

    tool_name = decision["tool"]
    tool_args = decision["args"]

    if tool_name not in TOOLS:
        print(f"❌ 未知工具：{tool_name}")
        return

    tool_func = TOOLS[tool_name]
    result = tool_func(**tool_args)

    print("🤖 Agent 决策：", decision)
    print("🔧 工具执行结果：", result)

if __name__ == "__main__":
    run_agent(
        "帮我解析这个提纲：\n"
        "1. 引言\n"
        "2. 相关工作\n"
        "3. 实验\n"
        "4. 结论"
    )
