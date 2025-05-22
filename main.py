import streamlit as st
from utils import qa_agent
from langchain.memory import ConversationBufferMemory

st.header("📃 智能单片机问答工具")

with st.sidebar:
    openai_api_key = st.text_input("请输入API密钥：", type="password")
    st.markdown("[获取API密钥](https://platform.moonshot.cn/)")

#使用会话状态避免每次提交初始化memory
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True,
                                                          memory_key="chat_history",
                                                          output_key="answer")

#uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")
st.write("同学们，大家好！欢迎来到单片机智能问答的世界！")
question = st.text_input("无论你是初学者，对单片机的基本概念、引脚功能、程序编程感到困惑；还是进阶学习者，正在钻研复杂的系统设计、通信协议、故障排查等问题，都可以在这里找到答案。只要输入你的问题，它会用清晰、准确且易于理解的方式为你解答，帮助你快速解锁单片机的奥秘。快来试试吧，让我们一起开启单片机学习的奇妙之旅！")    #disabled控制输入框是否允许输入

if question:
    if not openai_api_key:
        st.info("请输入你的API密钥")
        st.stop()

    with st.spinner("AI正在思考中，请稍等..."):
        result = qa_agent(question, st.session_state["memory"], openai_api_key)

    st.write("### 答案")
    st.write(result["answer"])
    #把历史对话放进记忆中
    st.session_state["chat_history"] = result["chat_history"]

if "chat_history" in st.session_state:
    with st.expander("历史消息"):
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.write(human_message.content)
            st.write(ai_message.content)
            if i < len(st.session_state["chat_history"])-2:
                st.divider()