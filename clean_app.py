import streamlit as st
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- REFINED CSS FOR MINI-BUTTONS ---
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
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'desired_outcome' not in st.session_state:
    st.session_state.desired_outcome = ""
if 'active_q' not in st.session_state:
    st.session_state.active_q = "And is there anything else about [X]?"

# --- SIDEBAR ---
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
        st.download_button("Download .txt", transcript, f"session_{datetime.now().strftime('%Y%m%d')}.txt")

        st.divider()
        if st.button("↩️ Undo Last Entry"):
            if st.session_state.history:
                st.session_state.history.pop()
                st.rerun()

    if st.button("🗑️ Clear All"):
        st.session_state.history = []
        st.rerun()

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
        st.session_state.history.append({
            "question": "And what would you like to have happen?", 
            "answer": st.session_state.desired_outcome, 
            "pro_type": cat, 
            "is_metaphor": False
        })
        st.rerun()

else:
    tab1, tab2, tab3 = st.tabs(["🚀 Active Session", "🖼️ Symbolic Landscape", "📚 Reference: Clean 12 & PRO"])

    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.subheader("Question Builder")
            subject_x = st.text_input("Metaphor/Word (X):")
            subject_y = st.text_input("Reference Word (Y):")
            
            st.write("**Quick Sensory Attributes:**")
            q_cols = st.columns(4)
            if q_cols[0].button("📍 Location"): st.session_state.active_q = "And whereabouts is [X]?"
            if q_cols[1].button("📏 Size/Shape"): st.session_state.active_q = "And does [X] have a size or a shape?"
            if q_cols[2].button("🎨 Texture"): st.session_state.active_q = "And what kind of [X] is that [X]?"
            if q_cols[3].button("⏳ Time"): st.session_state.active_q = "And what happens just before [X]?"

            questions = {
                "Developing (Outcomes)": ["And is there anything else about [X]?", "And what kind of [X] is that [X]?", "And whereabouts is [X]?", "And does [X] have a size or a shape?"],
                "Relationship (Space)": ["And is there a relationship between [X] and [Y]?", "And when [X], what happens to [Y]?", "And whereabouts is [X] in relation to [Y]?"],
                "Transitioning (Problems)": ["And when [X], what would you like to have happen?", "And what needs to happen for [Pinned Outcome]?"],
                "Moving Time (Remedies/Intent)": ["And when [X], then what happens?", "And what happens just before [X]?", "And what does [X] want?", "And what is the intention of [X]?"]
            }
            
            stage = st.selectbox("Category:", list(questions.keys()))
            current_options = questions[stage]
            if st.session_state.active_q not in current_options and "[X]" in st.session_state.active_q:
                current_options = [st.session_state.active_q] + current_options
            
            selected_q = st.selectbox("Question:", current_options, index=0)
            final_q = selected_q.replace("[X]", f"'{subject_x}'").replace("[Y]", f"'{subject_y}'").replace("[Pinned Outcome]", f"'{st.session_state.desired_outcome}'")

        with col2:
            st.subheader("Log Response")
            border_color = "#2196F3" 
            if "Transitioning" in stage: border_color = "#F44336"
            if "Moving" in stage: border_color = "#FF9800"
            
            st.markdown(f"""<div style="border: 2px solid {border_color}; padding:15px; border-radius:10px; background-color: #f0f2f6; color: #31333F;">
                <strong style="color:{border_color};">ASK:</strong><br>
                <span style="font-size: 1.15em; font-family: sans-serif; font-weight: 500;">{final_q}</span></div>""", unsafe_allow_html=True)
            
            st.write("")
            client_response = st.text_area("Client Response:", height=150)
            log_col1, log_col2, log_col3 = st.columns([2, 1, 1])
            with log_col1: pro_type = st.radio("PRO:", ["Outcome", "Problem", "Remedy"], horizontal=True)
            with log_col2: is_meta_choice = st.radio("Is Metaphor?", ["No", "Yes"], horizontal=True)
            with log_col3:
                st.write(" "); st.write(" ")
                if st.button("Log Entry") and client_response:
                    st.session_state.history.append({"question": final_q, "answer": client_response, "pro_type": pro_type, "is_metaphor": (is_meta_choice == "Yes")})
                    st.rerun()

    with tab2:
        st.subheader("The Symbolic Landscape")
        metaphors = [item for item in st.session_state.history if item.get('is_metaphor')]
        if not metaphors: st.info("Tag a response as 'Yes' for 'Is Metaphor?' to see it here.")
        else:
            m_cols = st.columns(3)
            for i, item in enumerate(metaphors):
                with m_cols[i % 3]: st.success(f"🔮 {item['answer'][:60]}...")
        st.divider()
        st.subheader("Full Session Transcript")
        for item in reversed(st.session_state.history):
            label = "🔮 Metaphor" if item.get('is_metaphor') else "💬 Concept"
            st.caption(f"{item['pro_type']} | {label}")
            st.write(f"**Q:** {item['question']}"); st.write(f"**A:** {item['answer']}"); st.divider()

    with tab3:
        st.header("The Clean 12 Questions")
        st.caption("Developed by Penny Tompkins & James Lawley")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Developing Questions")
            st.markdown("""
            * **Attributes:** And is there anything else about [X]?
            * **Attributes:** And what kind of [X] is that [X]?
            * **Location:** And whereabouts is [X]?
            * **Metaphor:** And that [X] is like what?
            * **Relationship:** And is there a relationship between [X] and [Y]?
            * **Relationship:** And whereabouts is [X] in relation to [Y]?
            """)
        with c2:
            st.subheader("Moving Time & Space")
            st.markdown("""
            * **Sequence:** And what happens just before [X]?
            * **Sequence:** And then what happens? / And what happens next?
            * **Source:** And where could that [X] come from?
            * **Intention:** And what does [X] want to have happen?
            * **Necessary Conditions:** And what needs to happen for [X] to [Y]?
            * **Necessary Conditions:** And can [X] [Y]?
            """)
        
        st.divider()
        st.header("The PRO Model Logic")
        
        p1, p2, p3 = st.columns(3)
        with p1:
            st.error("**P - Problem**")
            st.write("What is unwanted.")
            st.info("**Question:** 'And when [Problem], what would you like to have happen?'")
        with p2:
            st.warning("**R - Remedy**")
            st.write("A 'fix' or conceptual solution.")
            st.info("**Question:** 'And when [Remedy], then what happens?'")
        with p3:
            st.success("**O - Outcome**")
            st.write("A desired state or metaphor.")
            st.info("**Question:** 'And is there anything else about [Outcome]?'")

        st.divider()
        st.header("💡 Facilitator Tip: The Pivot")
        st.write("To move a client from a **Concept** (Remedy/Outcome) to a **Metaphor**, use the 'Like What' question:")
        st.success("**'And [Concept] is like what?'**")
        st.markdown("""
        1. **Wait** for the client to provide an image (e.g., 'It's like a heavy weight').
        2. **Tag** as Metaphor (🔮) in the logger.
        3. **Develop** the sensory qualities (Size, Shape, Location) of that image.
        """)
