import streamlit as st
from openai import OpenAI

# ========== 页面设置 ==========
st.set_page_config(
    page_title="AI客服助手 · 阿里云百炼",
    page_icon="🤖",
    layout="wide"
)

# ========== 初始化会话状态 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# ========== 侧边栏 ==========
with st.sidebar:
    st.image("https://img.alicdn.com/imgextra/i4/O1CN01YfLxCS1qUKxZ5ZaR4_!!6000000005501-2-tps-200-200.png", width=60)
    st.header("⚙️ 阿里云百炼设置")
    
    # API密钥
    st.subheader("🔑 API密钥")
    api_key = st.text_input(
        "输入百炼API-KEY",
        type="password",
        placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx",
        help="从 dashscope.console.aliyun.com → API-KEY管理 获取"
    )
    
    st.divider()
    
    # 模型选择
    st.subheader("🧠 模型选择")
    model = st.selectbox(
        "选择模型",
        options=[
            "qwen-plus",
            "qwen-turbo",
            "qwen-max",
            "qwen-max-longcontext"
        ],
        index=0,
        help="""
        - qwen-plus: 性价比最高，推荐日常使用
        - qwen-turbo: 速度最快，成本最低
        - qwen-max: 能力最强，复杂任务用
        - qwen-max-longcontext: 超长文本处理
        """
    )
    
    st.divider()
    
    # 客服设定
    st.subheader("📋 客服设定")
    system_prompt = st.text_area(
        "系统提示词（定义AI角色）",
        value="你是一个专业的客服助手，代表一家线上店铺。你需要：\n1. 用友好、热情的语气回复顾客\n2. 回答简洁明了，每次不超过150字\n3. 遇到售后问题主动提供解决方案\n4. 不知道的问题诚实说明，并引导顾客联系人工客服\n5. 适当使用表情符号让对话更亲切",
        height=200
    )
    
    # 店铺知识库
    st.subheader("📚 店铺知识库")
    knowledge_base = st.text_area(
        "粘贴店铺信息（AI会参考这些内容回复）",
        value="""店铺名称：阳光优选商城
主营商品：服装、鞋帽、家居用品
营业时间：周一至周日 9:00-22:00
客服在线时间：每天 8:00-24:00

退换货政策：
- 7天无理由退换货
- 质量问题包往返运费
- 非质量问题买家承担退货运费
- 退货地址：浙江省杭州市余杭区文一西路969号

物流信息：
- 默认发中通快递
- 48小时内发货
- 江浙沪1-2天送达
- 其他地区3-5天送达
- 满99元包邮

常见问题：
- 尺码不准可以免费换货一次
- 洗后缩水属于质量问题，可全额退款
- 优惠券不能叠加使用""",
        height=300,
        help="把你的店铺信息、退换货政策、物流信息等粘贴在这里"
    )
    
    st.divider()
    
    # 高级参数
    with st.expander("🔧 高级参数"):
        temperature = st.slider(
            "创意程度 (Temperature)",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="0=严谨按知识库回答，1=平衡，2=更有创意"
        )
        
        max_tokens = st.slider(
            "最大回复长度 (Max Tokens)",
            min_value=100,
            max_value=2000,
            value=300,
            step=50,
            help="控制AI回复的最大字数"
        )
        
        top_p = st.slider(
            "多样性 (Top P)",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.05,
            help="控制词语选择的多样性"
        )
    
    st.divider()
    
    # 使用统计
    st.subheader("📊 使用统计")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("本轮对话次数", len(st.session_state.messages) // 2)
    with col2:
        st.metric("累计Token", st.session_state.total_tokens)
    
    # 重置按钮
    if st.button("🔄 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.rerun()
    
    st.divider()
    st.caption("💡 阿里云百炼新用户送100万Token")
    st.caption("🔗 dashscope.console.aliyun.com")

# ========== 主界面 ==========
st.title("🤖 AI客服助手")
st.markdown("由阿里云通义千问驱动 · 支持知识库 · 多轮对话")

# ========== 对话区 ==========
st.subheader("💬 对话记录")

# 显示历史消息
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])
    elif message["role"] == "system":
        # 系统消息不显示
        pass

# ========== 输入区 ==========
st.divider()

# 快捷问题
st.caption("💡 快捷问题：")
cols = st.columns(4)
with cols[0]:
    if st.button("📦 查询物流", use_container_width=True):
        quick_question = "你好，我想查一下我的快递到哪了？"
        st.session_state.user_input = quick_question
with cols[1]:
    if st.button("🔄 申请退货", use_container_width=True):
        quick_question = "我买的衣服尺码不合适，想退货怎么操作？"
        st.session_state.user_input = quick_question
with cols[2]:
    if st.button("💰 优惠咨询", use_container_width=True):
        quick_question = "最近有什么优惠活动吗？优惠券可以叠加使用吗？"
        st.session_state.user_input = quick_question
with cols[3]:
    if st.button("🕐 营业时间", use_container_width=True):
        quick_question = "你们几点下班？周末有人回复吗？"
        st.session_state.user_input = quick_question

# 输入框
user_input = st.chat_input("输入顾客的问题...")

# ========== 处理用户输入 ==========
if user_input:
    # 显示用户消息
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # 保存到历史
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 验证
    if not api_key:
        with st.chat_message("assistant", avatar="🤖"):
            st.error("❌ 请先在左侧边栏输入阿里云百炼的API-KEY")
            st.info("💡 获取方式：dashscope.console.aliyun.com → API-KEY管理")
    
    else:
        # 构建完整系统提示词（客服设定 + 知识库）
        full_system_prompt = system_prompt
        
        if knowledge_base.strip():
            full_system_prompt += f"\n\n【店铺知识库，请根据以下信息回答顾客问题】\n{knowledge_base}"
        
        # 构建消息列表
        messages = [{"role": "system", "content": full_system_prompt}]
        
        # 添加历史消息（最近10轮，避免token过长）
        history = st.session_state.messages[-20:]
        messages.extend(history)
        
        # 调用API
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                timeout=30.0
            )
            
            with st.spinner("🤔 AI正在思考中..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p
                )
            
            # 获取回复
            reply = response.choices[0].message.content
            
            # 显示回复
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(reply)
                
                # 显示详细信息（可折叠）
                with st.expander("📊 查看调用详情"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("模型", model)
                    with col2:
                        st.metric("输入Token", response.usage.prompt_tokens if response.usage else "N/A")
                    with col3:
                        st.metric("输出Token", response.usage.completion_tokens if response.usage else "N/A")
                    with col4:
                        st.metric("总Token", response.usage.total_tokens if response.usage else "N/A")
            
            # 保存回复
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # 累计Token
            if response.usage:
                st.session_state.total_tokens += response.usage.total_tokens
            
            # 重新运行以刷新界面
            st.rerun()
            
        except Exception as e:
            error_msg = str(e)
            
            with st.chat_message("assistant", avatar="🤖"):
                if "401" in error_msg or "Authentication" in error_msg:
                    st.error("❌ API密钥认证失败")
                    st.info("""
                    **请检查：**
                    1. 密钥是否以 `sk-` 开头
                    2. 密钥是否来自 **dashscope.console.aliyun.com**（不是阿里云通用AccessKey）
                    3. 密钥是否已过期或被删除
                    4. 去百炼平台重新创建一个新密钥
                    """)
                    
                elif "402" in error_msg or "Insufficient" in error_msg or "余额不足" in error_msg:
                    st.error("❌ 账户余额不足或免费额度用完")
                    st.info("""
                    **解决方案：**
                    1. 新用户去阿里云百炼领取免费额度
                    2. 充值（费用很低）
                    3. 切换到 `qwen-turbo` 模型（成本最低）
                    """)
                    
                elif "404" in error_msg:
                    st.error(f"❌ 模型未找到：{model}")
                    st.info("请尝试切换到其他模型")
                    
                elif "429" in error_msg:
                    st.error("❌ 请求过于频繁，请稍后再试")
                    
                elif "timeout" in error_msg.lower():
                    st.error("❌ 请求超时，请检查网络连接")
                    
                else:
                    st.error(f"❌ 出错了：{error_msg}")
                    st.info("💡 复制上方错误信息，发给AI助手询问解决方法")

# ========== 底部信息 ==========
st.divider()
st.caption("🤖 AI客服助手 v3.0 | 阿里云百炼 · 通义千问 | 支持知识库 · 多轮对话 | 数据仅本次会话有效")