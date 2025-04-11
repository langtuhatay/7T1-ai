import streamlit as st
import openai
from datetime import date, datetime
import requests

openai.api_key = st.secrets["api_keys"]["openai"]

def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI thông minh, thân thiện, hiểu tiếng Việt."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Lỗi: {e}"

st.set_page_config(page_title="Chatbot Thông Minh", page_icon="💬")
st.title("💬 Chatbot T1 - Trợ lý AI")

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    name_input = st.text_input("Nhập tên của bạn để bắt đầu:")
    if name_input:
        st.session_state.username = name_input
        st.experimental_rerun()
    else:
        st.stop()

username = st.session_state.username

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Nhập tin nhắn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    you = prompt.strip()
    robot_brain = ""

    if you == "":
        robot_brain = "Tôi không nghe thấy gì cả, bạn thử lại nhé!"
    elif "hello" in you.lower():
        robot_brain = f"Xin chào {username}!"
    elif "btvn" in you.lower():
        robot_brain = (
            "1. Toán: Phiếu trên Teams  \n"
            "2. Văn: Phiếu trên Teams  \n"
            "3. TA: Làm từ đầu đến Task 7 trang 4 ĐC  \n"
            "4. KHTN: Làm hết phần TN trong ĐC"
        )
    elif "today" in you.lower():
        today = date.today()
        robot_brain = today.strftime("%d/%m/%Y")
    elif "now" in you.lower():
        now = datetime.now()
        robot_brain = now.strftime("%H:%M:%S")
    elif "bye" in you.lower():
        robot_brain = f"Tạm biệt {username}!"
    else:
        robot_brain = ask_openai(you)

    with st.chat_message("assistant"):
        st.markdown(robot_brain)

    st.session_state.messages.append({"role": "assistant", "content": robot_brain})
