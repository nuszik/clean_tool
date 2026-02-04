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

# --- SIDEBAR: ANALYTICS ---
with st.sidebar:
    st.title("🎯 Pinned Outcome")
    if st.session_state.desired_outcome:
        st.success(f"**{st.session_state.desired_outcome}**")
        if st.button("Reset Session"):
            st.session_state.history = []
            st.session_state.desired_outcome = ""
            st.rerun()
    
    st.divider()
    if st.session_state.history:
        st.header("☁️ Metaphor Cloud")
        cloud = get_metaphor_cloud(st.session_state.history)
        for word, count in cloud.items():
            size = 14 + (count * 2)
            st.markdown(f"<span style='font-size:{size}px; opacity:{min(1.0, 0.4 + count/10)};'>{word}</span>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

# --- MAIN INTERFACE ---
st.title("Clean Language Facilitator")

# STAGE 1: THE OPENING
if not st.session_state.desired_outcome:
    st.subheader("1. The Opening")
    st.info("Ask: 'And what would you like to have happen?'")
    initial_input = st.text_input("Client's Response:")
    if st.button("Set Outcome") and initial_input:
        st.session_state.desired_outcome = initial_input
        st.rerun()

# STAGE 2: THE PRO BRIDGE
elif len(st.session_state.history) == 0:
    st.subheader("2. Categorize the Response")
    st.write(f"The client said: **\"{st.session_state.desired_outcome}\"**")
    cat = st.radio("Is this a Problem, a Remedy, or an Outcome?", ["Outcome", "Problem", "Remedy"])
    
    st.divider()
    if "Outcome" in cat:
        st.success("✅ **Outcome:** Model this! Ask: *'And is there anything else about [Outcome]?'*")
    elif "Problem" in cat:
        st.error("⚠️ **Problem:** Do NOT model this. Transition to: *'What would you like to have happen?'*")
    else:
        st.warning("🔄 **Remedy:** This is a fix. Ask: *'And when [Remedy], then what happens?'*")
    
    if st.button("Start Modeling"):
        st.session_state.history.append({"question": "Initial", "answer": st.session_state.desired_outcome, "pro_type": cat})
        st.rerun()

# STAGE 3: THE ENGINE
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Question Builder")
        subject_x = st.text_input("Metaphor/Word (X):")
        
        questions = {
            "Developing (Outcomes)": [
                "And is there anything else about [X]?",
                "And what kind of [X] is
