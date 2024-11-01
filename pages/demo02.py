'''
基于历史聊天记录
'''

import streamlit as st
# langchain调用大模型，导入langchain的代码 大模型对象
from langchain_openai import ChatOpenAI
# 引入一个提示词对象
from langchain.prompts import PromptTemplate
#
from langchain.chains import LLMChain
# 记忆模块
from langchain.memory import ConversationBufferMemory



# 构建一个大模型
model = ChatOpenAI(
    temperature=0.8,# 温度 创新性
    model="glm-4-plus", # 大模型名字
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    api_key="96915ebe38efd95895bf9da56c95f508.WvBXo4mq8kFLkTTw"
)
# 创建记忆模块对象
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

memory = ConversationBufferMemory(memory_key="history")

# 创建提示词对象
prompt = PromptTemplate.from_template(f"你的名字是布丁，你是一只会说话的狗，你现在要扮演一个温柔体贴的角色,""你非常可爱，但又有点小小的傲娇，你现在要和你男朋友对话，" "直接回答问题，不要重复我的话，你男朋友说的话是{input}，你和男朋友的历史对话为{history}")

chain = LLMChain(
    llm = model,
    prompt = prompt,
    memory = st.session_state.memory
)

st.title("小布丁来和你聊天喽")
if "cache1" not in st.session_state:
    st.session_state.cache1 = []
else:
    for message in st.session_state.cache1:
        with st.chat_message(message['role']):
            st.write(message["content"])

# 创建一个聊天框
problem = st.chat_input("布丁正在等待你的回应")

# 判断是用来确定用户有没有输出问题
if problem:
    # 将用户问题输入到界面上
    with st.chat_message("user"):
        st.write(problem)
        st.session_state.cache1.append({"role": "user", "content": problem})
    # 调用大模型回答问题
    result = chain.invoke({"input": problem})
    # 将大模型回答的问题输出到界面上
    with st.chat_message("assistant"):
        st.write(result['text'])
        st.session_state.cache1.append({"role": "assistant", "content": result['text']})
