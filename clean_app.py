import streamlit as st
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- INITIALIZE STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'desired_outcome' not in st.session_state:
    st.session_state.desired_outcome = ""

# --- SIDEBAR: PINNED OUTCOME, HISTORY & DOWNLOAD ---
with st.sidebar:
    st.title("🎯 Pinned Outcome")
    if st.session_state.desired_outcome:
        st.success(f"**{st.session_state.desired_outcome}**")
        if st.button("Reset Session"):
            st.session_state.history = []
            st.session_state.desired_outcome = ""
            st.rerun()
    
    st.divider()
    
    # DOWNLOAD LOGIC
    if st.session_state.history:
        st.header("📥 Export Session")
        
        # Format the transcript text
        transcript = f"CLEAN LANGUAGE SESSION - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        transcript += f"PINNED OUTCOME: {st.session_state.desired_outcome}\n"
        transcript += "="*40 + "\n\n"
        
        for i, item in enumerate(st.session_state.history):
            transcript += f"{i+1}. [{item['pro_type']}]\n"
            transcript += f"   Q: {item['question']}\n"
            transcript += f"   A: {item['answer']}\n\n"
        
        st.download_button(
            label="Download .txt Transcript",
            data=transcript,
            file_name=f"clean_session_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
        
        st.divider()
        st.header("📝 History")
        for item in reversed(st.session_state.history):
            st.caption(f"{item['pro_type']}")
            st.write(f"**Q:** {item['question']}")
            st.write(f"**A:** {item['answer']}")
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
    cat = st.radio("Identify Response Type:", ["Outcome (Develop this)", "Problem (Transition this)", "Remedy (Move time forward)"])
    
    st.divider()
    if "Outcome" in cat:
        st.success("✅ **Action:** Model this. Suggested: 'And is there anything else about that [Outcome]?'")
    elif "Problem" in cat:
        st.error("⚠️ **Action:** Do NOT model the problem. Ask: 'And when [Problem], what would you like to have happen?'")
    else:
        st.warning("🔄 **Action:** This is a fix. Ask: 'And when [Remedy], then what happens?'")
    
    if st.button("Start Modeling"):
        st.session_state.history.append({"question": "Initial", "answer": st.session_state.desired_outcome, "pro_type": cat})
        st.rerun()

# STAGE 3: THE ENGINE
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Question Builder")
        subject_x = st.text_input("Metaphor/Word (X):")
        subject_y = st.text_input("Reference Word (Y) - Optional:")
        
        questions = {
            "Developing (Outcomes)": [
                "And is there anything else about [X]?",
                "And what kind of [X] is that [X]?",
                "And whereabouts is [X]?",
                "And does [X] have a size or a shape?"
            ],
            "Relationship (Space)": [
                "And is there a relationship between
