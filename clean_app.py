import streamlit as st
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- CLEAN UI CSS ---
st.markdown("""
    <style>
    /* Force 10px font size for sensory buttons */
    button[kind="secondary"] div[data-testid="stMarkdownContainer"] p {
        font-size: 10px !important;
        font-weight: 700 !important;
        line-height: 1 !important;
        text-transform: uppercase;
    }
    button[kind="secondary"] {
        padding: 2px 5px !important;
        height: 26px !important;
        min-height: 26px !important;
        border-radius: 4px !important;
    }
    .ask-box {
        border-radius: 10px;
        padding: 15px;
        background-color: #f0f2f6;
        color: #31333F;
        margin-bottom: 15px;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'desired_outcome' not in st.session_state:
    st.session_state.desired_outcome = ""

# The Complete Clean 20 Logic
QUESTIONS = {
    "Developing (Sensory)": [
        "And is there anything else about [X]?", 
        "And what kind of [X] is that [X]?", 
        "And does [X] have a size or a shape?",
        "And what is the color of [X]?",
        "And what is [X] made of?",
        "And how heavy is [X]?",
        "And that [X] is like what? (Metaphor)"
    ],
    "Spatial & Relationship": [
        "And whereabouts is [X]?", 
        "And is there a relationship between [X] and [Y]?", 
        "And whereabouts is [X] in relation to [Y]?",
        "And is [X] inside or outside?",
        "And what is between [X] and [Y]?",
        "And when [X], what happens to [Y]?"
    ],
    "Time & Sequence": [
        "And what happens just before [X]?", 
        "And then what happens? / What happens next?", 
        "And how long does [X] last?",
        "And where could that [X] come from? (Source)"
    ],
    "Intent & Capacity": [
        "And what does [X] want?", 
        "And what is the intention of [X]?",
        "And what needs to happen for [X] to happen?",
        "And can [X] happen?",
        "And what happens to [X] when [Pinned Outcome]?"
    ]
}

if 'active_cat' not in st.session_state:
    st.session_state.active_cat = "Developing (Sensory)"
if 'active_q' not in st.session_state:
    st.session_state.active_q = QUESTIONS["Developing (Sensory)"][0]

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
            transcript += f"{i+1}. [{item['pro_type']}] \n   Q: {item['question']}\n   A: {item['answer']}\n\n"
        
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
    initial_input = st.text_input("Ask: 'And what would you like to have happen?'")
    if st.button("Set Outcome") and initial_input:
        st.session_state.desired_outcome = initial_input; st.rerun()

elif len(st.session_state.history) == 0:
    st.subheader("2. Categorize Opening")
    st.write(f"Client said: **{st.session_state.desired_outcome}**")
    cat = st.radio("Type:", ["Outcome", "Problem", "Remedy"], horizontal=True)
    if st.button("Start Modeling"):
        st.session_state.history.append({"question": "Opening", "answer": st.session_state.desired_outcome, "pro_type": cat, "is_metaphor": False, "category": "Developing (Sensory)"})
        st.rerun()

else:
    tab1, tab2, tab3 = st.tabs(["🚀 Active Session", "🖼️ Symbolic Landscape", "📚 Reference: Clean 20 & PRO"])

    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.subheader("Question Builder")
            subject_x = st.text_input("Metaphor/Word (X):")
            subject_y = st.text_input("Reference Word (Y):")
            
            st.write("**Quick Sensory Attributes:**")
            q_cols = st.columns(4)
            q_cols[0].button("📍 Loc", on_click=set_question, args=("And whereabouts is [X]?", "Spatial & Relationship"))
            q_cols[1].button("📏 Size", on_click=set_question, args=("And does [X] have a size or a shape?", "Developing (Sensory)"))
            q_cols[2].button("🎨 Kind", on_click=set_question, args=("And what kind of [X] is that [X]?", "Developing (Sensory)"))
            q_cols[3].button("⏳ Time", on_click=set_question, args=("And what happens just before [X]?", "Time & Sequence"))

            stage = st.selectbox("Category:", list(QUESTIONS.keys()), key="active_cat")
            options = QUESTIONS[stage]
            
            try: current_idx = options.index(st.session_state.active_q)
            except ValueError: current_idx = 0

            selected_q = st.selectbox("Question:", options, index=current_idx, key="q_selector")
            st.session_state.active_q = selected_q
            
            final_q = selected_q.replace("[X]", f"'{subject_x}'").replace("[Y]", f"'{subject_y}'").replace("[Pinned Outcome]", f"'{st.session_state.desired_outcome}'")

        with col2:
            st.subheader("Log Response")
            border_color = "#2196F3" if "Sensory" in stage or "Spatial" in stage else "#FF9800"
            if "Transitioning" in stage: border_color = "#F44336"
            
            st.markdown(f'''<div class="ask-box" style="border: 2px solid {border_color};">
                <strong style="color:{border_color};">ASK:</strong><br>
                <span style="font-size: 1.15em; font-weight: 500;">{final_q}</span></div>''', unsafe_allow_html=True)
            
            client_response = st.text_area("Client Response:", height=200)

            log_col1, log_col2, log_col3 = st.columns([2, 1, 1])
            with log_col1: pro_type = st.radio("PRO:", ["Outcome", "Problem", "Remedy"], horizontal=True)
            with log_col2: is_meta_choice = st.radio("Metaphor?", ["No", "Yes"], horizontal=True)
            with log_col3:
                st.write(" "); st.write(" ")
                if st.button("Log Entry") and client_response:
                    st.session_state.history.append({
                        "question": final_q, "answer": client_response, "pro_type": pro_type, 
                        "is_metaphor": (is_meta_choice == "Yes"), "category": stage
                    })
                    st.rerun()

    with tab2:
        st.subheader("🖼️ Symbolic Landscape")
        metaphors = [item for item in st.session_state.history if item.get('is_metaphor')]
        if metaphors:
            m_cols = st.columns(3)
            for i, item in enumerate(metaphors):
                with m_cols[i % 3]: st.success(f"🔮 {item['answer'][:120]}...")
        st.divider()
        st.subheader("Full Session Transcript")
        for item in reversed(st.session_state.history):
            st.caption(f"{item['pro_type']} | {'🔮 Metaphor' if item['is_metaphor'] else '💬 Concept'}")
            st.write(f"**Q:** {item['question']}")
            st.write(f"**A:** {item['answer']}")
            st.divider()

    with tab3:
        st.header("The Clean 20 Questions")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Developing & Spatial")
            st.markdown("- **Attributes:** And is there anything else about [X]?\n- **Attributes:** And what kind of [X] is that [X]?\n- **Size/Shape:** And does [X] have a size or a shape?\n- **Location:** And whereabouts is [X]?\n- **Metaphor:** And that [X] is like what?\n- **Relationship:** And is there a relationship between [X] and [Y]?\n- **Position:** And whereabouts is [X] in relation to [Y]?\n- **Boundary:** And is [X] inside or outside?\n- **Space:** And what is between [X] and [Y]?\n- **Material:** And what is [X] made of?")
        with c2:
            st.subheader("Time, Intent & Capacity")
            st.markdown("- **Sequence:** And what happens just before [X]?\n- **Sequence:** And then what happens?\n- **Source:** And where could that [X] come from?\n- **Duration:** And how long does [X] last?\n- **Intention:** And what does [X] want?\n- **Intention:** And what is the intention of [X]?\n- **Necessary Conditions:** And what needs to happen for [X]?\n- **Possibility:** And can [X] happen?\n- **Interaction:** And when [X], what happens to [Y]?\n- **Outcome Link:** And what happens to [X] when [Pinned Outcome]?")
        st.divider()
        st.header("The Comprehensive PRO Model")
        
        p1, p2, p3 = st.columns(3)
        with p1:
            st.error("### P - Problem")
            st.markdown("**Strategy:** Shift to Outcome.\n**Question:** *'And when [Problem], what would you like to have happen?'*")
        with p2:
            st.warning("### R - Remedy")
            st.markdown("**Strategy:** Move time forward.\n**Question:** *'And when [Remedy], then what happens?'*")
        with p3:
            st.success("### O - Outcome")
            st.markdown("**Strategy:** Model the system using the **Clean 20** questions.")
