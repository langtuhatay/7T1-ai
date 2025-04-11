import streamlit as st
from datetime import date, datetime

st.set_page_config(page_title="Chatbot Lam Lai", page_icon="💬")
st.title("💬 Ứng dụng Chatbot với Streamlit")

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
        robot_brain = "I can't hear you, try again"
    elif "hello" in you.lower():
        robot_brain = "Hello Lam Lai"
    elif "btvn" in you.lower():
        robot_brain = """1. Toán: Phiếu trên Teams
                         2. Văn: Phiếu trên Teams
                         3. TA: Làm từ đầu đến Task 7 trang 4 ĐC
                         4. KHTN: Làm hết phần TN trong ĐC"""
    elif "today" in you.lower():
        today = date.today()
        robot_brain = today.strftime("%B %d, %Y")
    elif "now" in you.lower():
        now = datetime.now()
        robot_brain = now.strftime("%H hours %M minutes %S seconds")
    elif "bye" in you.lower():
        robot_brain = "Bye Lam Lai"
    else:
        robot_brain = "I'm fine thank you, and you?"

    with st.chat_message("assistant"):
        st.markdown(robot_brain)

    st.session_state.messages.append({"role": "assistant", "content": robot_brain})
