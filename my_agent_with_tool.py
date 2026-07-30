import json
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool

# ===== 第一步：定义一个“浏览器测试工具” =====
# 这个工具让 Agent 能模拟执行浏览器操作
@register_tool('web_test')
class WebTestTool(BaseTool):
    description = '执行Web测试操作，包括打开页面、输入文本、点击按钮'
    parameters = [
        {'name': 'action', 'type': 'string', 'description': '操作类型: open/input/click/assert', 'required': True},
        {'name': 'target', 'type': 'string', 'description': '操作目标: URL/输入框描述/按钮描述', 'required': True},
        {'name': 'value', 'type': 'string', 'description': '输入值', 'required': False},
    ]

    def call(self, params: str, **kwargs) -> str:
        params = json.loads(params)
        action = params.get('action')
        target = params.get('target')
        value = params.get('value', '')

        # 模拟执行（这里是模拟，不是真正的浏览器操作）
        if action == 'open':
            result = f'✅ 成功打开页面: {target}'
        elif action == 'input':
            result = f'✅ 在 "{target}" 输入了: {value}'
        elif action == 'click':
            result = f'✅ 点击了按钮: {target}'
        elif action == 'assert':
            result = f'✅ 断言成功: 页面包含 "{target}"'
        else:
            result = f'❌ 未知操作: {action}'

        return json.dumps({'result': result}, ensure_ascii=False)


# ===== 第二步：配置 LLM（和之前一样） =====
llm_cfg = {
    'model': 'qwen-plus',
    'model_server': 'dashscope',
    'api_key': 'sk-ws-H.EIYXMMX.2HgY.MEQCIE1CnqVEwJVOha6_O7Nf76pSYh-KZoSQt6jwE8O5pfwuAiAkxkvaGwM72kwZU-PVksT8vScWFXNF0i7C8gsqD2nMDA'
}


# ===== 第三步：系统提示词（告诉 Agent 它能用工具） =====
system_prompt = """你是一个Web测试专家。
你可以使用 web_test 工具来执行浏览器操作：
- action: open（打开页面）/ input（输入文本）/ click（点击按钮）/ assert（断言验证）
- target: URL或页面元素描述
- value: 输入值（仅input需要）

收到测试任务后：
1. 拆解成操作步骤
2. 依次调用工具执行
3. 返回测试结果

用中文回复，结果要结构化。
"""


# ===== 第四步：创建带工具的 Agent =====
bot = Assistant(
    llm=llm_cfg,
    system_message=system_prompt,
    function_list=['web_test'],  # ⚠️ 这里比之前多了一个工具列表
)


# ===== 第五步：测试任务 =====
test_task = """
测试百度搜索功能：
1. 打开 https://www.baidu.com
2. 在搜索框输入"软件测试"
3. 点击搜索按钮
4. 断言：搜索结果页面包含"软件测试"文字
"""

print("=" * 50)
print("AI测试Agent开始执行（带工具版本）")
print("=" * 50)

messages = [{'role': 'user', 'content': test_task}]

for response in bot.run(messages=messages):
    for msg in response:
        if msg['role'] == 'assistant':
            content = msg.get('content', '')
            if content:
                print(content)
            # 如果 Agent 调用了工具，这里会显示
            if 'function_call' in msg:
                print(f"🔧 调用工具: {msg['function_call']}")

print("\n" + "=" * 50)
print("执行完成")
print("=" * 50)