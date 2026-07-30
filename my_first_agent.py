import os
from qwen_agent.agents import Assistant

# 配置使用Qwen模型
llm_cfg = {
    'model': 'qwen-plus',
    'model_server': 'dashscope',
    'api_key': 'sk-ws-H.EIYXMMX.2HgY.MEQCIE1CnqVEwJVOha6_O7Nf76pSYh-KZoSQt6jwE8O5pfwuAiAkxkvaGwM72kwZU-PVksT8vScWFXNF0i7C8gsqD2nMDA'
}

# 系统提示词：定义Agent的角色
system_prompt = """你是一个Web自动化测试专家。
当用户给你一个测试任务时，你会：
1. 理解用户要测试什么功能
2. 拆解成具体的测试步骤
3. 规划如何执行这些步骤
4. 返回结构化的测试计划

注意：你的回答要包含：测试目标、测试步骤、预期结果。
"""

# 创建Assistant
bot = Assistant(
    llm=llm_cfg,
    system_message=system_prompt,
    function_list=[],
)

# 测试任务
test_task = "请为'用户登录功能'设计一个测试计划，包含正常登录、密码错误、账号不存在三个场景。"

print("=== 正在执行AI测试任务 ===")
print(f"测试指令: {test_task}\n")

messages = [{'role': 'user', 'content': test_task}]

print("=== AI测试执行结果 ===")
for response in bot.run(messages=messages):
    for msg in response:
        if msg['role'] == 'assistant':
            print(msg['content'])