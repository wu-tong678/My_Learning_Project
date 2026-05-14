from langchain_community.chat_models import ChatZhipuAI

# 连接智谱
llm = ChatZhipuAI(
    api_key="1017a85ed2874e23983ac4ec8b17f951.FvXi975NPHkrEgQq",
    model="glm-4-flash",
)

# 手动存储对话历史
chat_history = []

print("开始聊天（输入 quit 退出）\n")

while True:
    user_input = input("你: ")
    if user_input.lower() == "quit":
        break

    # 把用户消息加入历史
    chat_history.append(f"用户: {user_input}")

    # 对话历史用换行拼起来，末尾加上换行和AI
    full_prompt = "\n".join(chat_history) + "\nAI: "

    # 发给AI
    response = llm.invoke(full_prompt)

    # 把AI回复加入历史
    chat_history.append(f"AI: {response.content}")

    print(f"AI: {response.content}\n")