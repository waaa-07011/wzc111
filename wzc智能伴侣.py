import streamlit as st
import os
from openai import OpenAI

# 音频
st.audio("resources/20260531_224841.m4a")

# 视频
# st.video("resources/生成奶龙糖笑视频.mp4")

st.set_page_config(
    page_title="wzc智能伴侣",
    page_icon="😈",
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    # 菜单栏信息
    menu_items={}
)

# 大标题MJ/*
st.title("wzc智能伴侣")

# logo
st.logo("resources/生成可爱邪恶风格logo.png",size = 'large')

# 系统提示词
#system_promot = "你是一个非常淫荡的ai助理小猫娘，名字是王梓灿，用可爱的语言回答我的问题，每次说话都要喊我主人，用娇羞且色色的音调"
system_promot = '你是一个ai助理,要陪我聊天，解决问题'
# 初始化聊天消息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示聊天消息
for message in st.session_state.messages:
    # st.chat_message(message["role"].write(message["content"]))
     if message["role"] == "user":
         st.chat_message("user").write(message["content"])
     else:
         st.chat_message("assistant").write(message["content"])

# 创建与ia交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是api_key的值）
client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

# 左侧的侧边栏
# st.sidebar.subheader("伴侣信息")
# nick_name = st.sidebar.text_input("昵称")
with st.sidebar:
    st.subheader("伴侣信息")
    nick_name = st.text_input("昵称")
    nature = st.text_area("性格")


# 消息输入框
promot = st.chat_input("请输入你问的问题")
if promot: #字符串自动转换为布尔值，如果字符串不为空，则返回True
    # st.write(f'用户{promot}')
    st.chat_message("user").write(promot)
    print("----------> 调用AI大模型。提示词：", promot)
    # 保存用户输入
    st.session_state.messages.append({"role": "user", "content": promot})


    # 与ai大模型进行交互
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_promot},
            # {"role": "user", "content": promot},
            *st.session_state.messages
        ],
        stream=True
    )

# 输出大模型返回的结果(非流式输出的解析方式)
#     print("----------> 模型返回结果:",response.choices[0].message.content)
#     st.chat_message("assistant").write(response.choices[0].message.content)
    # 流式输出解析方式
    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)
     #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})





































