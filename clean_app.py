import streamlit as st

# Title and Instructions
st.title("Clean Language Facilitator")
st.markdown("Use this tool to maintain the 'Clean' structure during a session.")

# 1. Capture the User's exact words
subject_x = st.text_input("Enter the client's exact word/metaphor (X):", placeholder="e.g., a heavy mist")
subject_y = st.text_input("Enter a second word/metaphor if comparing (Y):", placeholder="e.g., a cold wind")

# 2. Categorized Question Bank
questions = {
    "1. Developing (Attributes)": [
        "And is there anything else about [X]?",
        "And what kind of [X] is that [X]?",
        "And whereabouts is [X]?",
        "And does [X] have a size or a shape?",
        "And that [X] is like what?"
    ],
    "2. Relationship/Space": [
        "And is there a relationship between [X] and [Y]?",
        "And is [X] the same or different to [Y]?",
        "And what happens to [Y] when [X] happens?"
    ],
    "3. Time & Sequence": [
        "And what happens just before [X]?",
        "And then what happens?",
        "And where could [X] come from?"
    ],
    "4. Intention & Change": [
        "And what would you like to have happen?",
        "And what needs to happen for [X] to [Y]?",
        "And can [X] [Y]?"
    ]
}

# 3. Interactive Selection
stage = st.selectbox("Select the Staging Logic:", list(questions.keys()))
selected_q = st.selectbox("Choose a Clean Question:", questions[stage])

# 4. Logic to inject words into the question
final_question = selected_q.replace("[X]", f"**{subject_x}**").replace("[Y]", f"**{subject_y}**")

st.divider()

# 5. The Output
if subject_x:
    st.subheader("Your Clean Question:")
    st.write(final_question)
    st.caption("Tip: Use your 'Clean Voice'—slower, deeper, and rhythmic.")
else:
    st.info("Enter a word above to generate the question.")
