from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatZhipuAI
from langchain.chains import RetrievalQA


# ========== 1. 多文档路径列表 ==========
doc_paths = [
    "learn.pdf",
    "ai.txt"
]

# ========== 2. 加载所有文档 ==========
all_docs = []
for path in doc_paths:
    if path.endswith(".pdf"):#检查字符串是否以某个后缀结尾
        loader = PyPDFLoader(path)
    else:
        loader = TextLoader(path, encoding="utf-8")

    docs = loader.load()
    all_docs.extend(docs)  # 合并到总列表
    print(f"✅ 已加载: {path} ({len(docs)} 页/段)")

print(f"📚 共加载 {len(all_docs)} 个文档对象")

#======分割文本=====
splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
chunks=splitter.split_documents(all_docs)
print(f"分割成{len(chunks)}个文本")

#======向量化=====
print("初始化embedding...")
#对象，负责把文字转成向量
embeddings=ZhipuAIEmbeddings(
    model="embedding-2",
    api_key="1017a85ed2874e23983ac4ec8b17f951.FvXi975NPHkrEgQq"
)

#========存入向量库======
vectorstore=FAISS.from_documents(chunks,embeddings)
print(f"向量库创建完成")


#=====创建LLM====
llm=ChatZhipuAI(
    model="glm-4-plus",
    temperature=0,
    api_key="1017a85ed2874e23983ac4ec8b17f951.FvXi975NPHkrEgQq"

)

#====创建RAG问答=====
qa=RetrievalQA.from_chain_type(
    llm=llm,#指定生成答案的模型
    #向量库包装成检索器，每次返回最相关的 3 个文本块
    retriever=vectorstore.as_retriever(search_kwargs={"k":3}),
    #True返回答案 + 参考来源，False	只返回答案
    return_source_documents=True
)

#=====提问====
question = "这些文档（包括PDF和TXT）分别讲了什么？"
#返回字典
result=qa.invoke({"query":question})

print(f"问题:{question}")
print(f"回答:{result['result']}")
print(f"参考了{len(result['source_documents'])}个片段")