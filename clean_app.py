import streamlit as st
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- INITIALIZE STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'desired_outcome' not in st.session_state:
    st.session_state.desired_outcome = ""

# --- SIDEBAR: PINNED OUTCOME & EXPORT ---
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
        st.header("📥 Export Session")
        transcript = f"CLEAN LANGUAGE SESSION - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        transcript += f"PINNED OUTCOME: {st.session_state.desired_outcome}\n"
        transcript += "="*40 + "\n\n"
        for i, item in enumerate(st.session_state.history):
            m_tag = " [SYMBOL]" if item.get('is_metaphor') else ""
            transcript += f"{i+1}. [{item['pro_type']}] {m_tag}\n   Q: {item['question']}\n   A: {item['answer']}\n\n"
        
        st.download_button("Download .txt Transcript", transcript, f"session_{datetime.now().strftime('%Y%m%d')}.txt")
        
        st.divider()
        st.header("📝 History")
        for item in reversed(st.session_state.history):
            label = "🔮 Metaphor" if item.get('is_metaphor') else "💬 Concept"
            st.caption(f"{item['pro_type']} | {label}")
            st.write(f"**Q:** {item['question']}")
            st.write(f"**A:** {item['answer']}")
            st.divider()

# --- MAIN INTERFACE ---
st.title("Clean Language Facilitator")

if not st.session_state.desired_outcome:
    st.subheader("1. The Opening")
    st.info("Ask: 'And what would you like to have happen?'")
    initial_input = st.text_input("Client's Response:")
    if st.button("Set Outcome") and initial_input:
        st.session_state.desired_outcome = initial_input
        st.rerun()

elif len(st.session_state.history) == 0:
    st.subheader("2. Categorize the Response")
    st.write(f"The client said: **\"{st.session_state.desired_outcome}\"**")
    cat = st.radio("Type:", ["Outcome", "Problem", "Remedy"], horizontal=True)
    if st.button("Start Modeling"):
        st.session_state.history.append({"question": "Initial", "answer": st.session_state.desired_outcome, "pro_type": cat, "is_metaphor": False})
        st.rerun()

else:
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.subheader("Question Builder")
        subject_x = st.text_input("Metaphor/Word (X):")
        subject_y = st.text_input("Reference Word (Y):")
        
        questions = {
            "Developing (Outcomes)": ["And is there anything else about [X]?", "And what kind of [X] is that [X]?", "And whereabouts is [X]?", "And does [X] have a size or a shape?"],
            "Relationship (Space)": ["And is there a relationship between [X] and [Y]?", "And when [X], what happens to [Y]?", "And whereabouts is [X] in relation to [Y]?"],
            "Transitioning (Problems)": ["And when [X], what would you like to have happen?", "And what needs to happen for [Pinned Outcome]?"],
            "Moving Time (Remedies)": ["And when [X], then what happens?", "And what happens just before [X]?"]
        }
        
        stage = st.selectbox("Category:", list(questions.keys()))
        selected_q = st.selectbox("Question:", questions[stage])
        
        final_q = selected_q.replace("[X]", f"'{subject_x}'").replace("[Y]", f"'{subject_y}'").replace("[Pinned Outcome]", f"'{st.session_state.desired_outcome}'")

    with col2:
        st.subheader("Log Response")
        st.markdown(f"**ASK:** `{final_q}`")
        client_response = st.text_area("Client Response:", height=200)
        
        # --- ALIGNED LOGGING ROW ---
        log_col1, log_col2, log_col3 = st.columns([2, 1, 1])
        with log_col1:
            pro_type = st.radio("PRO:", ["Outcome", "Problem", "Remedy"], horizontal=True)
        with log_col2:
            # We use a radio button here instead of a checkbox so it aligns with the PRO radio buttons
            is_meta_choice = st.radio("Is Metaphor?", ["No", "Yes"], horizontal=True)
        with log_col3:
            st.write(" ") # Padding to push button down
            st.write(" ")
            log_btn = st.button("Log Entry")
        
        if log_btn and client_response:
            st.session_state.history.append({
                "question": final_q, 
                "answer": client_response, 
                "pro_type": pro_type,
                "is_metaphor": (is_meta_choice == "Yes")
            })
            st.rerun()
