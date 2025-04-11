import streamlit as st
import openai
import requests
from datetime import datetime, date

openai.api_key = st.secrets["OPENAI_API_KEY"]
google_api_key = st.secrets["GOOGLE_API_KEY"]
google_cx = st.secrets["GOOGLE_CX"]

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": google_api_key,
        "cx": google_cx,
        "q": query
    }
    res = requests.get(url, params=params)
    results = res.json()
    if "items" in results:
        return results["items"][0]["snippet"]
    return "Không tìm thấy kết quả trên internet."

def ask_openai(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=500,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Lỗi OpenAI: {e}"

st.set_page_config(page_title="Chatbot By Hoang Bao Lam", page_icon="💬")
st.title("💬 T1 Chatbot")

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    name_input = st.text_input("Nhập tên của bạn để bắt đầu:")
    if name_input:
        st.session_state.username = name_input
        st.rerun()
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
        robot_brain = "Bạn nói nhỏ quá, nói lại nha!"
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
        robot_brain = date.today().strftime("%B %d, %Y")
    elif "now" in you.lower():
        now = datetime.now()
        robot_brain = now.strftime("%H:%M:%S")
    elif "bye" in you.lower():
        robot_brain = f"Bye {username}"
    else:
        google_result = google_search(you)
        if google_result == "Không tìm thấy kết quả trên internet.":
            robot_brain = ask_openai(you)
        else:
            robot_brain = google_result

    with st.chat_message("assistant"):
        st.markdown(robot_brain)

    st.session_state.messages.append({"role": "assistant", "content": robot_brain})
