import streamlit as st
from datetime import datetime
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Clean Language Facilitator PRO", layout="wide")

# --- AGGRESSIVE CSS FOR MINI-BUTTONS ---
st.markdown("""
    <style>
    button[kind="secondary"] div[data-testid="stMarkdownContainer"] p {
        font-size: 10px !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
    }
    button[kind="secondary"] {
        padding: 0px 5px !important;
        height: 24px !important;
        min-height: 24px !important;
        border-radius: 4px !important;
    }
    .ask-box {
        border-radius: 10px;
        padding: 15px;
        background-color: #f0f2f6;
        color: #31333F;
        margin-bottom: 10px;
    }
    /* Style for the visual map symbols */
    .map-symbol {
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background-color: #2196F3;
        color: white;
        font-weight: bold;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'desired_outcome' not in st.session_state:
    st.session_state.desired_outcome = ""

# Define Expanded Global Questions (The Clean 20)
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
    st.info("Ask: 'And what would you like to have happen?'")
    initial_input = st.text_input("Client's Response:")
    if st.button("Set Outcome") and initial_input:
        st.session_state.desired_outcome = initial_input; st.rerun()

elif len(st.session_state.history) == 0:
    st.subheader("2. Categorize Opening")
    st.write(f"Client said: **{st.session_state.desired_outcome}**")
    cat = st.radio("Type:", ["Outcome", "Problem", "Remedy"], horizontal=True)
    if st.button("Start Modeling"):
        st.session_state.history.append({"question": "Opening", "answer": st.session_state.desired_outcome, "pro_type": cat, "is_metaphor": False, "category": "Developing (Sensory)", "x_pos": 50, "y_pos": 50})
        st.rerun()

else:
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Active Session", "🖼️ Symbolic Landscape", "🗺️ Visual Map", "📚 Reference: Clean 20 & PRO"])

    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.subheader("Question Builder")
            subject_x = st.text_input("Metaphor/Word (X):")
            subject_y = st.text_input("Reference Word (Y):")
            
            st.write("**Quick Sensory:**")
            q_cols = st.columns(4)
            q_cols[0].button("📍 Loc", on_click=set_question, args=("And whereabouts is [X]?", "Spatial & Relationship"))
            q_cols[1].button("📏 Size", on_click=set_question, args=("And does [X] have a size or a shape?", "Developing (Sensory)"))
            q_cols[2].button("🎨 Kind", on_click=set_question, args=("And what kind of [X] is that [X]?", "Developing (Sensory)"))
            q_cols[3].button("⏳ Time", on_click=set_question, args=("And what happens just before [X]?", "Time & Sequence"))

            stage = st.selectbox("Category:", list(QUESTIONS.keys()), key="active_cat")
            options = QUESTIONS[stage]
            
            if st.session_state.active_q not in options:
                current_q_index = 0
            else:
                current_q_index = options.index(st.session_state.active_q)

            selected_q = st.selectbox("Question:", options, index=current_q_index, key="q_selector")
            st.session_state.active_q = selected_q
            
            final_q = selected_q.replace("[X]", f"'{subject_x}'").replace("[Y]", f"'{subject_y}'").replace("[Pinned Outcome]", f"'{st.session_state.desired_outcome}'")

        with col2:
            st.subheader("Log Response")
            border_color = "#2196F3" if "Sensory" in stage or "Spatial" in stage else "#FF9800"
            if "Transitioning" in stage: border_color = "#F44336"
            
            st.markdown(f'''<div class="ask-box" style="border: 2px solid {border_color};">
                <strong style="color:{border_color};">ASK:</strong><br>
                <span style="font-size: 1.1em; font-weight: 500;">{final_q}</span></div>''', unsafe_allow_html=True)
            
            client_response = st.text_area("Client Response:", height=150)
            
            # Manual Mapping Input (Optional)
            st.caption("Map Position (0-100)")
            map_cols = st.columns(2)
            map_x = map_cols[0].slider("Left-Right", 0, 100, 50)
            map_y = map_cols[1].slider("Up-Down", 0, 100, 50)

            log_col1, log_col2, log_col3 = st.columns([2, 1, 1])
            with log_col1: pro_type = st.radio("PRO:", ["Outcome", "Problem", "Remedy"], horizontal=True)
            with log_col2: is_meta_choice = st.radio("Metaphor?", ["No", "Yes"], horizontal=True)
            with log_col3:
                st.write(" "); st.write(" ")
                if st.button("Log Entry") and client_response:
                    st.session_state.history.append({
                        "question": final_q, 
                        "answer": client_response, 
                        "pro_type": pro_type, 
                        "is_metaphor": (is_meta_choice == "Yes"), 
                        "category": stage,
                        "x_pos": map_x,
                        "y_pos": map_y,
                        "label": subject_x if subject_x else client_response[:10]
                    })
                    st.rerun()

    with tab2:
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
        st.subheader("🗺️ Symbolic Map")
        st.caption("Visualizing the 'Whereabouts' of symbols in the landscape.")
        
        # Prepare data for scatter plot
        map_items = [item for item in st.session_state.history if item.get('is_metaphor')]
        if not map_items:
            st.info("Symbols tagged as 'Metaphor' will appear here on a spatial grid.")
        else:
            chart_data = pd.DataFrame([
                {"x": item['x_pos'], "y": item['y_pos'], "Symbol": item.get('label', 'Unknown')} 
                for item in map_items
            ])
            st.scatter_chart(chart_data, x="x", y="y", color="Symbol", size=200)
            
            st.divider()
            st.write("**Key Locations Identified:**")
            for item in map_items:
                st.write(f"• **{item.get('label')}**: X:{item['x_pos']} | Y:{item['y_pos']}")

    with tab4:
        st.header("The Clean 20 Questions")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Developing & Spatial")
            st.markdown("""
            - **Attributes:** And is there anything else about [X]?
            - **Attributes:** And what kind of [X] is that [X]?
            - **Size/Shape:** And does [X] have a size or a shape?
            - **Location:** And whereabouts is [X]?
            - **Metaphor:** And that [X] is like what?
            - **Relationship:** And is there a relationship between [X] and [Y]?
            - **Position:** And whereabouts is [X] in relation to [Y]?
            - **Boundary:** And is [X] inside or outside?
            - **Space:** And what is between [X] and [Y]?
            - **Material:** And what is [X] made of?
            """)
        with c2:
            st.subheader("Time, Intent & Capacity")
            st.markdown("""
            - **Sequence:** And what happens just before [X]?
            - **Sequence:** And then what happens?
            - **Source:** And where could that [X] come from?
            - **Duration:** And how long does [X] last?
            - **Intention:** And what does [X] want?
            - **Intention:** And what is the intention of [X]?
            - **Necessary Conditions:** And what needs to happen for [X]?
            - **Possibility:** And can [X] happen?
            - **Interaction:** And when [X], what happens to [Y]?
            - **Outcome Link:** And what happens to [X] when [Pinned Outcome]?
            """)
        
        st.divider()
        st.header("The Comprehensive PRO Model")
        
        p1, p2, p3 = st.columns(3)
        with p1:
            st.error("### P - Problem")
            st.markdown("**Focus:** Unwanted states.\n\n**Strategy:** Shift to Outcome.\n\n**Question:** *'And when [Problem], what would you like to have happen?'*")
        with p2:
            st.warning("### R - Remedy")
            st.markdown("**Focus:** Conceptual fixes.\n\n**Strategy:** Move time forward.\n\n**Question:** *'And when [Remedy], then what happens?'*")
        with p3:
            st.success("### O - Outcome")
            st.markdown("**Focus:** Desired states.\n\n**Strategy:** Model the system using the **Clean 20** questions above.")
