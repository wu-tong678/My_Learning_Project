from langchain_community.chat_models import ChatTongyi
from langchain.tools import tool

llm = ChatTongyi(model="qwen-plus", temperature=0, dashscope_api_key="你的Key")


@tool
def multiply(a: int, b: int) -> int:
    """计算两个数的乘积。"""
    return a * b


@tool
def get_weather(location: str) -> str:
    """查询天气。"""
    weather_db = {"北京": "晴天 25°C", "上海": "雨天 20°C"}
    return weather_db.get(location, "暂无数据")


tools = {tool.name: tool for tool in [multiply, get_weather]}


def my_agent(user_input):
    llm_with_tools = llm.bind_tools(list(tools.values()))
    response = llm_with_tools.invoke(user_input)

    results = {}
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        result = tools[tool_name].invoke(tool_args)
        results[tool_name] = result
        print(f"执行 {tool_name}({tool_args}) = {result}")

    final = llm.invoke(f"用户问：{user_input}\n工具结果：{results}\n请回答用户。")
    return final.content


print(my_agent("北京天气？算15乘32"))