import streamlit as st
from datetime import datetime

# Setup the page
st.set_page_config(page_title="Clean Language Facilitator", layout="wide")

st.title("Clean Language Facilitator 3.0")

# 1. Session State Initialization
if 'history' not in st.session_state:
    st.session_state.history = []

# 2. Sidebar for History and Export
with st.sidebar:
    st.header("📝 Session History")
    
    # Create the text for the download file
    transcript_text = "CLEAN LANGUAGE SESSION TRANSCRIPT\n"
    transcript_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    transcript_text += "="*30 + "\n\n"
    
    for i, item in enumerate(st.session_state.history):
        transcript_text += f"{i+1}. Question: {item['question']}\n"
        transcript_text += f"   Answer: {item['answer']}\n\n"

    # Download Button
    st.download_button(
        label="📥 Download Transcript (.txt)",
        data=transcript_text,
        file_name=f"clean_session_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )

    if st.button("Clear All Data"):
        st.session_state.history = []
        st.rerun()
    
    st.divider()
    # Display the history visually in the sidebar
    for item in reversed(st.session_state.history):
        st.caption(f"Q: {item['question']}")
        st.write(f"A: {item['answer']}")
        st.divider()

# 3. Main Interface Logic
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Setup the Question")
    subject_x = st.text_input("Current Metaphor/Word (X):")
    subject_y = st.text_input("Second Word (Y) - if needed:")

    questions = {
        "Developing (Attributes)": [
            "And is there anything else about [X]?",
            "And what kind of [X] is that [X]?",
            "And whereabouts is [X]?",
            "And does [X] have a size or a shape?",
            "And that [X] is like what?"
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

    stage = st.selectbox("Select Staging:", list(questions.keys()))
    selected_q_template = st.selectbox("Choose Question:", questions[stage])
    
    # Process the question with inputs
    final_q = selected_q_template.replace("[X]", f"'{subject_x}'").replace("[Y]", f"'{subject_y}'")

with col2:
    st.subheader("2. Ask and Record")
    st.info(f"**Question to Ask:** \n\n {final_q}")
    
    client_answer = st.text_area("Type client's exact answer here:", height=150)
    
    if st.button("Log Answer & Next Step"):
        if subject_x and client_answer:
            st.session_state.history.append({
                "question": final_q,
                "answer": client_answer
            })
            st.success("Saved to history! Clear the 'X' box to start the next question.")
        else:
            st.error("Please provide both the subject (X) and the client's answer.")
