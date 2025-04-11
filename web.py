import streamlit as st
from datetime import date, datetime
import requests

def search_duckduckgo(query):
    res = requests.get("https://api.duckduckgo.com/",
                       params={"q": query, "format": "json"})
    data = res.json()
    return data.get("AbstractText", "Không tìm thấy kết quả trên internet.")

st.set_page_config(page_title="Chatbot By Hoang Bao Lam", page_icon="💬")
st.title("💬 T1 Chatbot")

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
        robot_brain = "I can't hear you, try again"
    elif "hello" in you.lower():
        robot_brain = f"Hello {username}"
    elif "btvn" in you.lower():
        robot_brain = (
            "1. Toán: Phiếu trên Teams  \n"
            "2. Văn: Phiếu trên Teams  \n"
            "3. TA: Làm từ đầu đến Task 7 trang 4 ĐC  \n"
            "4. KHTN: Làm hết phần TN trong ĐC"
        )
    elif "today" in you.lower():
        today = date.today()
        robot_brain = today.strftime("%B %d, %Y")
    elif "now" in you.lower():
        now = datetime.now()
        robot_brain = now.strftime("%H hours %M minutes %S seconds")
    elif "bye" in you.lower():
        robot_brain = f"Bye {username}"
    else:
        robot_brain = search_duckduckgo(you)

    with st.chat_message("assistant"):
        st.markdown(robot_brain)

    st.session_state.messages.append({"role": "assistant", "content": robot_brain})
