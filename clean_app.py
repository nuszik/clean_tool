import streamlit as st
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- INITIALIZE STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'desired_outcome' not in st.session_state:
    st.session_state.desired_outcome = ""

# --- SIDEBAR: PINNED OUTCOME & HISTORY ---
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
        st.header("📝 Session History")
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
        
        # DEFINED QUESTION DICTIONARY
        questions = {
            "Developing (Outcomes)": [
                "And is there anything else about [X]?",
                "And what kind of [X] is that [X]?",
                "And whereabouts is [X]?",
                "And does [X] have a size or a shape?"
            ],
            "Relationship (Space)": [
                "And is there a relationship between [X] and [Y]?",
                "And when [X], what happens to [Y]?",
                "And whereabouts is [X] in relation to [Y]?"
            ],
            "Transitioning (Problems)": [
                "And when [X], what would you like to have happen?",
                "And what needs to happen for [Pinned Outcome]?",
                "And can [Pinned Outcome] happen?"
            ],
            "Moving Time (Remedies)": [
                "And when [X], then what happens?",
                "And what happens just before [X]?"
            ]
        }
        
        stage = st.selectbox("Select Category:", list(questions.keys()))
        
        # HELPER TEXT
        if "Developing" in stage:
            st.help("Focus on Outcome metaphors to build the internal landscape.")
        elif "Relationship" in stage:
            st.help("Explore how different parts of the client's model interact.")
        elif "Transitioning" in stage:
            st.help("Bridges the gap from a Problem back to the Pinned Outcome.")
        elif "Moving" in stage:
            st.help("Moves the sequence forward to find the actual benefit of a Remedy.")

        selected_q = st.selectbox("Choose Question:", questions[stage])
        
        # String Replacement Logic
        final_q = selected_q.replace("[X]", f"'{subject_x}'")
        final_q = final_q.replace("[Y]", f"'{subject_y}'")
        final_q = final_q.replace("[Pinned Outcome]", f"'{st.session_state.desired_outcome}'")

    with col2:
        st.subheader("Log Response")
        st.markdown(f"**ASK:** `{final_q}`")
        client_response = st.text_area("Client Response:", height=150)
        pro_type = st.radio("Categorize Response:", ["Outcome", "Problem", "Remedy"], horizontal=True)
        
        if st.button("Log and Continue"):
            if client_response:
                st.session_state.history.append({
                    "question": final_q, 
                    "answer": client_response, 
                    "pro_type": pro_type
                })
                st.rerun()
