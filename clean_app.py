import streamlit as st
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- CSS FOR MINI-BUTTONS ---
st.markdown("""
    <style>
    div[data-testid="column"] button {
        font-size: 10px !important;
        padding: 1px 5px !important;
        min-height: 25px !important;
        height: 25px !important;
        line-height: 1 !important;
        border-radius: 4px !important;
    }
    div[data-testid="column"] button p {
        font-size: 10px !important;
        margin: 0 !important;
    }
    /* Style for the Ask box to ensure readability */
    .ask-box {
        border-radius: 10px;
        padding: 15px;
        background-color: #f0f2f6;
        color: #31333F;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'desired_outcome' not in st.session_state:
    st.session_state.desired_outcome = ""

# Define Global Questions
QUESTIONS = {
    "Developing (Outcomes)": ["And is there anything else about [X]?", "And what kind of [X] is that [X]?", "And whereabouts is [X]?", "And does [X] have a size or a shape?"],
    "Relationship (Space)": ["And is there a relationship between [X] and [Y]?", "And when [X], what happens to [Y]?", "And whereabouts is [X] in relation to [Y]?"],
    "Transitioning (Problems)": ["And when [X], what would you like to have happen?", "And what needs to happen for [Pinned Outcome]?"],
    "Moving Time (Remedies/Intent)": ["And when [X], then what happens?", "And what happens just before [X]?", "And what does [X] want?", "And what is the intention of [X]?"]
}

# Fix: Initialize selection states only if they don't exist
if 'active_cat' not in st.session_state:
    st.session_state.active_cat = "Developing (Outcomes)"
if 'active_q' not in st.session_state:
    st.session_state.active_q = QUESTIONS["Developing (Outcomes)"][0]

# Callback for Quick Buttons
def set_question(q_text, category):
    st.session_state.active_q = q_text
    st.session_state.active_cat = category

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎯 Pinned Outcome")
    if st.session_state.desired_outcome:
        st.success(f"**{st.session_state.desired_outcome}**")
        
    st.divider()
    
    if st.session_state.history:
        st.header("📥 Session Control")
        transcript = f"CLEAN LANGUAGE SESSION - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        transcript += f"PINNED OUTCOME: {st.session_state.desired_outcome}\n"
        transcript += "="*40 + "\n\n"
        for i, item in enumerate(st.session_state.history):
            m_tag = " [SYMBOL]" if item.get('is_metaphor') else ""
            transcript += f"{i+1}. [{item['pro_type']}] {m_tag}\n   Q: {item['question']}\n   A: {item['answer']}\n\n"
        
        st.download_button("Download Transcript (.txt)", transcript, f"session_{datetime.now().strftime('%Y%m%d')}.txt")
        
        if st.button("↩️ Undo Last Entry"):
            if st.session_state.history:
                st.session_state.history.pop()
                st.rerun()

    if st.button("🗑️ Reset Full Session"):
        st.session_state.history = []
        st.session_state.desired_outcome = ""
        st.rerun()

# --- MAIN INTERFACE ---
if not st.session_state.desired_outcome:
    st.subheader("1. The Opening")
    st.info("Ask: 'And what would you like to have happen?'")
    initial_input = st.text_input("Client's Response:")
    if st.button("Set Outcome") and initial_input:
        st.session_state.desired_outcome = initial_input; st.rerun()

elif len(st.session_state.history) == 0:
    st.subheader("2. Categorize Opening")
    st.write(f"Client said: **{st.session_state.desired_outcome}**")
    cat = st.radio("Type:", ["Outcome", "Problem", "Remedy"], horizontal=True)
    if st.button("Start Modeling"):
        st.session_state.history.append({"question": "And what would you like to have happen?", "answer": st.session_state.desired_outcome, "pro_type": cat, "is_metaphor": False, "category": "Developing (Outcomes)"})
        st.rerun()

else:
    tab1, tab2, tab3 = st.tabs(["🚀 Active Session", "🖼️ Symbolic Landscape", "📚 Reference: Clean 12 & PRO"])

    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.subheader("Question Builder")
            subject_x = st.text_input("Metaphor/Word (X):")
            subject_y = st.text_input("Reference Word (Y):")
            
            st.write("**Quick Sensory:**")
            q_cols = st.columns(4)
            q_cols[0].button("📍 Loc", on_click=set_question, args=("And whereabouts is [X]?", "Developing (Outcomes)"))
            q_cols[1].button("📏 Size", on_click=set_question, args=("And does [X] have a size or a shape?", "Developing (Outcomes)"))
            q_cols[2].button("🎨 Kind", on_click=set_question, args=("And what kind of [X] is that [X]?", "Developing (Outcomes)"))
            q_cols[3].button("⏳ Time", on_click=set_question, args=("And what happens just before [X]?", "Moving Time (Remedies/Intent)"))

            # Categories and Questions
            stage = st.selectbox("Category:", list(QUESTIONS.keys()), key="active_cat")
            options = QUESTIONS[stage]
            
            # Validation: Ensure current active question exists in the chosen category's options
            if st.session_state.active_q not in options:
                current_q_index = 0
            else:
                current_q_index = options.index(st.session_state.active_q)

            selected_q = st.selectbox("Question:", options, index=current_q_index, key="q_selector")
            # Update state if manually changed in dropdown
            st.session_state.active_q = selected_q
            
            final_q = selected_q.replace("[X]", f"'{subject_x}'").replace("[Y]", f"'{subject_y}'").replace("[Pinned Outcome]", f"'{st.session_state.desired_outcome}'")

        with col2:
            st.subheader("Log Response")
            border_color = "#2196F3" if "Developing" in stage else "#FF9800"
            if "Transitioning" in stage: border_color = "#F44336"
            
            st.markdown(f'''<div class="ask-box" style="border: 2px solid {border_color};">
                <strong style="color:{border_color};">ASK:</strong><br>
                <span style="font-size: 1.1em; font-weight: 500;">{final_q}</span></div>''', unsafe_allow_html=True)
            
            st.write("")
            client_response = st.text_area("Client Response:", height=150)
            log_col1, log_col2, log_col3 = st.columns([2, 1, 1])
            with log_col1: pro_type = st.radio("PRO:", ["Outcome", "Problem", "Remedy"], horizontal=True)
            with log_col2: is_meta_choice = st.radio("Metaphor?", ["No", "Yes"], horizontal=True)
            with log_col3:
                st.write(" "); st.write(" ")
                if st.button("Log Entry") and client_response:
                    st.session_state.history.append({"question": final_q, "answer": client_response, "pro_type": pro_type, "is_metaphor": (is_meta_choice == "Yes"), "category": stage})
                    st.rerun()

    with tab2:
        st.subheader("📊 Session Balance Audit")
        total_qs = len(st.session_state.history)
        if total_qs > 1:
            cats = [item.get('category', 'Developing (Outcomes)') for item in st.session_state.history]
            dev_p = (cats.count("Developing (Outcomes)") / total_qs)
            rel_p = (cats.count("Relationship (Space)") / total_qs)
            c1, c2 = st.columns(2)
            c1.metric("Developing %", f"{int(dev_p*100)}%")
            c2.metric("Relationship %", f"{int(rel_p*100)}%")
        
        st.divider()
        st.subheader("🖼️ Symbolic Landscape")
        metaphors = [item for item in st.session_state.history if item.get('is_metaphor')]
        if metaphors:
            m_cols = st.columns(3)
            for i, item in enumerate(metaphors):
                with m_cols[i % 3]: st.success(f"🔮 {item['answer'][:60]}...")
        
        st.divider()
        st.subheader("Full Transcript")
        for item in reversed(st.session_state.history):
            st.caption(f"{item['pro_type']} | {'🔮 Metaphor' if item['is_metaphor'] else '💬 Concept'}")
            st.write(f"**Q:** {item['question']}")
            st.write(f"**A:** {item['answer']}")
            st.divider()

    with tab3:
        st.header("The Clean 12 Questions")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Developing")
            st.markdown("- **Attributes:** And is there anything else about [X]?\n- **Attributes:** And what kind of [X] is that [X]?\n- **Location:** And whereabouts is [X]?\n- **Metaphor:** And that [X] is like what?\n- **Relationship:** And is there a relationship between [X] and [Y]?\n- **Relationship:** And whereabouts is [X] in relation to [Y]?")
        with c2:
            st.subheader("Moving Time/Space")
            st.markdown("- **Sequence:** And what happens just before [X]?\n- **Sequence:** And then what happens?\n- **Source:** And where could that [X] come from?\n- **Intention:** And what does [X] want to have happen?\n- **Conditions:** And what needs to happen for [X]?\n- **Conditions:** And can [X] [Y]?")
        
        st.divider()
        st.header("The Comprehensive PRO Model")
        
        p1, p2, p3 = st.columns(3)
        with p1:
            st.error("### P - Problem")
            st.markdown("**Definition:** Descriptions of what is wrong or unwanted.\n\n**Strategy:** Shift to Outcome.\n\n**Question:** *'And when [Problem], what would you like to have happen?'*")
        with p2:
            st.warning("### R - Remedy")
            st.markdown("**Definition:** Conceptual solutions ('I need to be calm').\n\n**Strategy:** Move time forward.\n\n**Question:** *'And when [Remedy], then what happens?'*")
        with p3:
            st.success("### O - Outcome")
            st.markdown("**Definition:** The desired state/metaphor.\n\n**Strategy:** Model the system.\n\n**Action:** Use Developing & Relationship questions.")
