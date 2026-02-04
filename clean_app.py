import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Clean Language Facilitator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Session State Initialization (The "Memory")
if 'history' not in st.session_state:
    st.session_state.history = []

# 2. Sidebar: History & Export
with st.sidebar:
    st.header("📝 Session History")
    
    # Generate Transcript for Download
    transcript_text = "CLEAN LANGUAGE SESSION TRANSCRIPT\n"
    transcript_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    transcript_text += "="*40 + "\n\n"
    
    for i, item in enumerate(st.session_state.history):
        transcript_text += f"{i+1}. Question: {item['question']}\n"
        transcript_text += f"   Answer: {item['answer']}\n"
        if item['notes']:
            transcript_text += f"   Notes: {item['notes']}\n"
        transcript_text += "-"*20 + "\n"

    st.download_button(
        label="📥 Download Session (.txt)",
        data=transcript_text,
        file_name=f"clean_session_{datetime.now().strftime('%y%m%d_%H%M')}.txt",
        mime="text/plain"
    )

    if st.button("🗑️ Clear Session"):
        st.session_state.history = []
        st.rerun()
    
    st.divider()
    
    # Visual History Feed
    for item in reversed(st.session_state.history):
        st.caption(f"Q: {item['question']}")
        st.write(f"A: {item['answer']}")
        if item['notes']:
            st.info(f"Note: {item['notes']}")
        st.divider()

# 3. Main Interface
st.title("Clean Language Facilitator")
st.markdown("Developed by James Lawley and Penny Tompkins")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Setup Metadata")
    subject_x = st.text_input("Current Metaphor/Word (X):", placeholder="e.g., 'a heavy knot'")
    subject_y = st.text_input("Reference Word (Y) - Optional:", placeholder="e.g., 'the blue light'")

    # Full Question Bank organized by Lawley & Tompkins' Staging logic
    questions = {
        "Developing (Attributes)": [
            "And is there anything else about [X]?",
            "And what kind of [X] is that [X]?",
            "And that [X] is like what?",
            "And does [X] have a size or a shape?",
            "And does [X] have a color?",
            "And how old is [X]?"
        ],
        "Developing (Location)": [
            "And whereabouts is [X]?",
            "And is [X] on the inside or the outside?",
            "And is [X] to the front or the back?",
            "And is [X] to the left or the right?",
            "And how far away is [X]?"
        ],
        "Space & Relationship": [
            "And is there a relationship between [X] and [Y]?",
            "And is [X] the same or different to [Y]?",
            "And what happens to [Y] when [X] happens?",
            "And what is [X] to [Y]?"
        ],
        "Time & Sequence": [
            "And what happens just before [X]?",
            "And then what happens?",
            "And where could [X] come from?"
        ],
        "Desired Outcome": [
            "And what would you like to have happen?",
            "And what needs to happen for [X] to [Y]?",
            "And can [X] [Y]?"
        ]
    }

    stage = st.selectbox("Current Stage:", list(questions.keys()))
    selected_q_template = st.selectbox("Select Question:", questions[stage])
    
    # Format the prompt
    final_q = selected_q_template.replace("[X]", f"'{subject_x}'").replace("[Y]", f"'{subject_y}'")

with col2:
    st.subheader("2. Facilitate & Record")
    st.warning(f"**READ ALOUD:** {final_q}")
    
    client_answer = st.text_area("Client's response:", height=150)
    fac_notes = st.text_input("Observation Notes (gestures, pauses, shifts):")
    
    if st.button("➕ Log Entry"):
        if subject_x and client_answer:
            st.session_state.history.append({
                "question": final_q,
                "answer": client_answer,
                "notes": fac_notes
            })
            st.rerun()
        else:
            st.error("Please enter both the subject (X) and the client's answer.")
