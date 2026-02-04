import streamlit as st
from datetime import datetime
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- INITIALIZE STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'desired_outcome' not in st.session_state:
    st.session_state.desired_outcome = ""

# --- ANALYTICS LOGIC ---
def get_metaphor_cloud(history):
    stop_words = {"the", "and", "a", "to", "of", "in", "is", "it", "that", "i", "was", "for", "on", "are", "with", "as", "be", "at", "my", "me", "like", "you", "have"}
    all_text = " ".join([item['answer'] for item in history]).lower()
    words = re.findall(r'\w+', all_text)
    counts = {}
    for w in words:
        if w not in stop_words and len(w) > 2:
            counts[w] = counts.get(w, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10])

pro_counts = {"Outcome": 0, "Problem": 0, "Remedy": 0}
for item in st.session_state.history:
    if "Outcome" in item['pro_type']: pro_counts["Outcome"] += 1
    elif "Problem" in item['pro_type']: pro_counts["Problem"] += 1
    elif "Remedy" in item['pro_type']: pro_counts["Remedy"] += 1
total_logs = sum(pro_counts.values())

# --- SIDEBAR: ANALYTICS & PINNED OUTCOME ---
with st.sidebar:
    st.title("🎯 Pinned Outcome")
    if st.session_state.desired_outcome:
        st.success(f"**{st.session_state.desired_outcome}**")
        if st.button("Reset Session"):
            st.session_state.history = []
            st.session_state.desired_outcome = ""
            st.rerun()
    
    st.divider()
    st.header("📊 Session Balance")
    if total_logs > 0:
        st.caption(f"Outcome ({int((pro_counts['Outcome']/total_logs)*100)}%)")
        st.progress(pro_counts["Outcome"]/total_logs)
        st.caption(f"Problem ({int((pro_counts['Problem']/total_logs)*100)}%)")
        st.progress(pro_counts["Problem"]/total_logs)
        
        st.divider()
        st.header("☁️ Metaphor Cloud")
        cloud = get_metaphor_cloud(st.session_state.history)
        for word, count in cloud.items():
            size = 14 + (count * 2)
            st.markdown(f"<span style='font-size:{size}px; opacity:{min(1.0, 0.4 + count/10)};'>{word}</span>", unsafe_allow_html=True)
    
    st.divider()
    transcript = f"Outcome: {st.session_state.desired_outcome}\n\n"
    for item in st.session_state.history:
        transcript += f"[{item['pro_type']}] {item['question']} -> {item['answer']}\n"
    st.download_button("📥 Download Transcript", data=transcript, file_name="clean_session.txt")

# --- MAIN INTERFACE ---
st.title("Clean Language Facilitator")

if not st.session_state.desired_outcome:
    st.subheader("1. Start the Session")
    st.warning("And what would you like to have happen?")
    initial_outcome = st.text_input("Client's response:", key="init_out")
    if st.button("Initialize") and initial_outcome:
        st.session_state.desired_outcome = initial_outcome
        st.session_state.history.append({"question": "Start", "answer": initial_outcome, "pro_type": "Outcome"})
        st.rerun()
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Question Builder")
        subject_x = st.text_input("Metaphor/Word (X):")
        questions = {
            "Developing (Outcomes)": ["And what kind of [X] is that?", "And is there anything else about [X]?", "And whereabouts is [X]?"],
            "Transitioning (Problems)": ["And when [X], what would you like to have happen?", "And what needs to happen for [Pinned]?"],
            "Moving Time (Remedies)": ["And when [X], then what happens?", "And what happens just before [X]?"]
        }
        stage = st.selectbox("Stage:", list(questions.keys()))
        selected_q = st.selectbox("Question:", questions[stage])
        final_q = selected_q.replace("[X]", f"'{subject_x}'").replace("[Pinned]", f"'{st.session_state.desired_outcome}'")

    with col2:
        st.subheader("Log Response")
        st.markdown(f"**ASK:** `{final_q}`")
        client_response = st.text_area("Client Response:")
        pro_type = st.radio("Category:", ["Outcome", "Problem", "Remedy"], horizontal=True)
        if st.button("Log and Analyze"):
            if client_response:
                st.session_state.history.append({"question": final_q, "answer": client_response, "pro_type": pro_type})
                st.rerun()
