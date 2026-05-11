from langchain_community.chat_models import ChatZhipuAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 初始化模型
llm = ChatZhipuAI(
    api_key="API_KEY",
    model="glm-4-flash",
)

# 2. 创建模板（{topic}是可变占位符）
prompt = PromptTemplate.from_template("请用{language}解释一下什么是{topic}，50字以内")

# 3. 用LCEL串起来（| 表示“然后”）
chain = prompt | llm | StrOutputParser()

# 4. 运行
result = chain.invoke({"topic": "LangChain", "language": "中文"})
print(result)
