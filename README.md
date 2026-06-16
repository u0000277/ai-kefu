import streamlit as st
from openai import OpenAI

# 页面标题
st.title("🤖 AI客服助手")
st.write("输入顾客的问题，AI帮你自动回复")

# 侧边栏：输入API密钥
with st.sidebar:使用st.sidebar：
    st.header("设置")
    api_key = st.text_input("输入你的API密钥", type="password")
    st.caption("密钥不会保存，放心使用")

# 输入框
user_input = st.text_area("顾客的问题：", placeholder="例如：我的快递什么时候到？")

# 按钮
if st.button("生成回复"):如果 st.button("生成回复")：
    if not api_key:    如果没有 API 密钥：
        st.warning("请先在侧边栏输入API密钥")
    elif not user_input:
        st.warning("请输入顾客的问题")
    else:
        # 调用AI
        client = OpenAI(        客户端 = OpenAI(        客户端 = OpenAI(        客户端 = OpenAI(        客户端 = OpenAI(        客户端 = OpenAI(        客户端 = OpenAI(        客户端 = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        with st.spinner("AI正在思考..."):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的客服助手，回答要简洁友好，不超过100字。"},
                    {"role": "user", "content": user_input}
                ]
            )
        
        # 显示结果
        st.success("回复生成成功！")
        st.write(response.choices[0].message.content)

# 页面底部
st.divider()
st.caption("AI客服助手 v1.0 | 由DeepSeek驱动")
