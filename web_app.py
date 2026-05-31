import streamlit as st

st.title("📚 PDF问答助手")

# 初始化会话状态（关键！）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏：上传文件
with st.sidebar:
    st.header("文档上传")
    uploaded_file = st.file_uploader("选择PDF", type=["pdf"])

    if uploaded_file is not None:
        st.success(f"已加载：{uploaded_file.name}")

# 主区域：问答
question = st.text_input("输入你的问题：")

# 按钮：只有点击时才执行
if st.button("提交问题"):
    if uploaded_file and question:
        with st.spinner("AI思考中..."):
            # 这里放你的RAG代码
            # answer = your_rag_function(question, uploaded_file)

            # 模拟回答（替换成真实RAG）
            answer = f"关于「{question}」的回答（这里是RAG返回的结果）"

        # 显示回答
        st.success("回答：")
        st.write(answer)

        # 保存到历史记录
        st.session_state.messages.append({"question": question, "answer": answer})
    else:
        #用于显示黄色警告框。
        st.warning("请先上传PDF并输入问题")