import streamlit as st

from pages_backend.practice.herb_practice import generate_random_question


st.set_page_config(
    page_title="Herb Practice",
    page_icon="🌿",
)

st.title("🌿 Herb Practice")

# Initialize session state
if 'herb_practice_question' not in st.session_state:
    st.session_state.herb_practice_question = None
if 'herb_practice_score' not in st.session_state:
    st.session_state.herb_practice_score = {'correct': 0, 'total': 0}
if 'herb_practice_answered' not in st.session_state:
    st.session_state.herb_practice_answered = False

# Question type selection
st.subheader("Question Types")
col1, col2, col3 = st.columns(3)
with col1:
    include_herb_group = st.checkbox("Herb Group", value=True, key="herb_group_type")
with col2:
    include_focus_to_herb = st.checkbox("Focus Remark → Herb", value=True, key="focus_to_herb_type")
with col3:
    include_herb_to_focus = st.checkbox("Herb → Focus Remark", value=True, key="herb_to_focus_type")

selected_types = []
if include_herb_group:
    selected_types.append("herb_group")
if include_focus_to_herb:
    selected_types.append("focus_remark_to_herb")
if include_herb_to_focus:
    selected_types.append("herb_to_focus_remark")

# Generate new question button
if st.button("Generate Question", key="generate_question_btn"):
    if selected_types:
        st.session_state.herb_practice_question = generate_random_question(selected_types)
        st.session_state.herb_practice_answered = False
    else:
        st.warning("Please select at least one question type!")

# Display current question
if st.session_state.herb_practice_question:
    question = st.session_state.herb_practice_question

    st.subheader("Question")
    st.markdown(f"### {question.question}")

    st.subheader("Answer")
    selected_answer = st.radio(
        "Choose the correct answer:",
        question.choices,
        key="answer_radio"
    )

    # Submit answer button
    if st.button("Submit Answer", key="submit_answer_btn"):
        st.session_state.herb_practice_answered = True

    # Show feedback if answered
    if st.session_state.herb_practice_answered:
        is_correct = selected_answer == question.correct_answer

        if is_correct:
            st.success("✅ Correct!")
            st.session_state.herb_practice_score['correct'] += 1
        else:
            st.error(f"❌ Incorrect! The correct answer is: **{question.correct_answer}**")

        st.session_state.herb_practice_score['total'] += 1

    # Display score
    st.divider()
    st.subheader("Score")
    score = st.session_state.herb_practice_score
    st.metric(
        "Accuracy",
        f"{score['correct']}/{score['total']}",
        f"{round(100 * score['correct'] / score['total'], 1)}%" if score['total'] > 0 else "0%"
    )

    # Reset score button
    if st.button("Reset Score", key="reset_score_btn"):
        st.session_state.herb_practice_score = {'correct': 0, 'total': 0}
        st.rerun()
else:
    st.info("👈 Click 'Generate Question' to start practicing!")

