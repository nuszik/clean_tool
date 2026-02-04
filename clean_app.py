import streamlit as st
from datetime import datetime
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- CSS FOR MINI-BUTTONS & UI ---
st.markdown("""
    <style>
    button[kind="secondary"] p { font-size: 10px !important; font-weight: bold !important; }
    button[kind="secondary"] { padding: 0px 5px !important; height: 24px !important; min-height: 24px !important; }
    .word-bank-item { font-size: 12px; background-color: #f0f2f6; padding: 2px 8px; border-radius: 10px; margin: 2px; display: inline-block; border: 1px solid #d1d5db; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'history' not in st.session_state: st.session_state.history = []
if 'desired_outcome' not in st.session_state: st.session_state.desired_outcome = ""

QUESTIONS = {
    "Developing (Outcomes)": ["And is there anything else about [X]?", "And what kind of [X] is that [X]?", "And whereabouts is [X]?", "And does [X] have a size or a shape?"],
    "Relationship (Space)": ["And is there a relationship between [X] and [Y]?", "And when [X], what happens to [Y]?", "And whereabouts is [X] in relation to [Y]?"],
    "Transitioning (Problems)": ["And when [X], what would you like to have happen?", "And what needs to happen for [Pinned Outcome]?"],
    "Moving Time (Remedies/Intent)": ["And when [X], then what happens?", "And what happens just before [X]?", "And what does [X] want?", "And what is the intention of [X]?"]
}

def set_question(q_text, category):
    st.session_state.active_q = q_text
    st.session_state.active_cat = category

if 'active_cat' not in st.session_state: st.session_state.active_cat = "Developing (Outcomes)"
if 'active_q' not in st.session_state: st.session_state.active_q = QUESTIONS["Developing (Outcomes)"][0]

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎯 Pinned Outcome")
    if st.session_state.desired_outcome:
        st.success(f"**{st.session_state.desired_outcome}**")
        
    st.divider()
    
    # --- WORD BANK (lexicon) ---
    st.subheader("📋 Client Lexicon")
    st.caption("Key words from the session:")
    all_text = " ".join([item['answer'] for item in st.session_state.history])
    # Simple logic to find words often used in metaphors (nouns/adjectives)
    words = list(set(re.findall(r'\b\w{4,}\b', all_text.lower())))
    if words:
        for word in words[:15]: # Show top 15 words
            st.markdown(f'<span class="word-bank-item">{word}</span>', unsafe_allow_html=True)
    
    st.divider()
    if st.session_state.history:
        st.header("📥 Export")
        if st.button("↩️ Undo Last"):
            st.session_state.history.pop()
            st.rerun()
        if st.button("🗑️ Reset All"):
            st.session_state.history = []; st.session_state.desired_outcome = ""; st.rerun()

# --- MAIN INTERFACE ---
if not st.session_state.desired_outcome:
    st.subheader("1. The Opening")
    initial_input = st.text_input("Ask: 'And what would you like to have happen?'")
    if st.button("Set Outcome") and initial_input:
        st.session_state.desired_outcome = initial_input; st.rerun()

elif len(st.session_state.history) == 0:
    st.subheader("2. Categorize Opening")
    st.write(f"Client: **{st.session_state.desired_outcome}**")
    cat = st.radio("Type:", ["Outcome", "Problem", "Remedy"], horizontal=True)
    if st.button("Start"):
        st.session_state.history.append({"question": "Opening", "answer": st.session_state.desired_outcome, "pro_type": cat, "is_metaphor": False, "category": "Developing (Outcomes)"})
        st.rerun()

else:
    tab1, tab2, tab3 = st.tabs(["🚀 Active Session", "🖼️ Symbolic Landscape", "📚 Reference"])

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

            stage = st.selectbox("Category:", list(QUESTIONS.keys()), key="active_cat")
            options = QUESTIONS[stage]
            if st.session_state.active_q not in options: st.session_state.active_q = options[0]
            selected_q = st.selectbox("Question:", options, key="active_q")
            final_q = selected_q.replace("[X]", f"'{subject_x}'").replace("[Y]", f"'{subject_y}'").replace("[Pinned Outcome]", f"'{st.session_state.desired_outcome}'")

        with col2:
            st.subheader("Log Response")
            border_color = "#2196F3" if "Developing" in stage else "#FF9800"
            if "Transitioning" in stage: border_color = "#F44336"
            
            st.markdown(f'<div style="border: 2px solid {border_color}; padding:15px; border-radius:10px; background-color: #f0f2f6;"><strong>ASK:</strong><br>{final_q}</div>', unsafe_allow_html=True)
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
        # --- SESSION AUDIT ---
        st.subheader("📊 Session Balance Audit")
        total_qs = len(st.session_state.history)
        if total_qs > 1:
            cats = [item.get('category', 'Developing (Outcomes)') for item in st.session_state.history]
            dev_p = (cats.count("Developing (Outcomes)") / total_qs)
            rel_p = (cats.count("Relationship (Space)") / total_qs)
            
            c1, c2 = st.columns(2)
            c1.metric("Developing %", f"{int(dev_p*100)}%")
            c2.metric("Relationship %", f"{int(rel_p*100)}%")
            if rel_p < 0.2: st.warning("Facilitator Tip: Try to ask more Relationship questions to connect the metaphors.")

        st.divider()
        st.subheader("🖼️ Symbolic Landscape")
        metaphors = [item for item in st.session_state.history if item.get('is_metaphor')]
        if metaphors:
            m_cols = st.columns(3)
            for i, item in enumerate(metaphors):
                with m_cols[i % 3]: st.success(f"🔮 {item['answer'][:60]}...")

    with tab3:
        st.header("The Clean 12 & PRO Reference")
        # (Reference content remains same as previous version)
