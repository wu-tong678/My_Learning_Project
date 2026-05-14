from langchain_community.chat_models import ChatTongyi
from langchain.tools import tool
#from langchain.agents import create_tool_calling_agent, AgentExecutor
#from langchain_core.prompts import ChatPromptTemplate
llm = ChatTongyi(
    model="qwen-plus",
    temperature=0,
    dashscope_api_key="密钥"
)

@tool
def multiply(a: int, b: int) -> int:
    """计算两个数的乘积。"""
    return a * b

@tool
def get_weather(location: str) -> str:
    """查询指定城市的天气。"""
    weather_db = {"北京": "晴天 25°C", "上海": "雨天 20°C"}
    return weather_db.get(location, "暂无数据")

#自己写tool+循环=agent
'''
tools = {tool.name: tool for tool in [multiply, get_weather]}

# 绑定工具
llm_with_tools = llm.bind_tools(list(tools.values()))

# 用户问题
user_input = "北京天气怎么样？顺便算一下 15 乘以 32"
response = llm_with_tools.invoke(user_input)

# 执行 LLM 想调用的工具
results = {}
if hasattr(response, "tool_calls") and response.tool_calls:
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        result = tools[tool_name].invoke(tool_args)
        results[tool_name] = result
        print(f"执行 {tool_name}({tool_args}) = {result}")

# 把结果返回给 LLM 生成最终回答
final_response = llm.invoke(
    f"用户问：{user_input}\n\n"
    f"工具执行结果：{results}\n\n"
    f"请基于这些结果回答用户。"
)
print("\n最终回答：", final_response.content)
'''
#调用agent
'''
tools = [multiply, get_weather]

# 创建 Prompt（必须带 {agent_scratchpad}）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手，可以调用工具。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 创建 Agent（官方3行）
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({"input": "北京天气怎么样？顺便算一下 15 乘以 32"})

print(result["output"])
'''