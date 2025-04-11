import streamlit as st
import openai
import requests
from datetime import datetime, date

from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
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

    user_input = prompt.strip()
    response = ""

    if user_input == "":
        response = "Bạn nói nhỏ quá, nói lại nha!"
    elif "hello" in user_input.lower():
        response = f"Hello {username}"
    elif "btvn" in user_input.lower():
        response = (
            "1. Toán: Phiếu trên Teams  \n"
            "2. Văn: Phiếu trên Teams  \n"
            "3. TA: Làm từ đầu đến Task 7 trang 4 ĐC  \n"
            "4. KHTN: Làm hết phần TN trong ĐC"
        )
    elif "today" in user_input.lower():
        response = date.today().strftime("%B %d, %Y")
    elif "now" in user_input.lower():
        now = datetime.now()
        response = now.strftime("%H:%M:%S")
    elif "bye" in user_input.lower():
        response = f"Bye {username}"
    elif user_input.lower().startswith("tìm :"):
        query = user_input[5:].strip()
        response = google_search(query)
    else:
        response = ask_openai(user_input)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
