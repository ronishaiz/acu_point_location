import streamlit as st

from backend.herbs.herb import filter_herbs_by_groups, get_herb_group_options
from pages_backend.practice.herb_practice import (
    generate_random_question,
    get_semester_a_herb_group_values,
    get_semester_b_herb_group_values,
)


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
if 'herb_practice_group_labels' not in st.session_state:
    all_group_options = get_herb_group_options()
    st.session_state.herb_practice_group_labels = [opt['label'] for opt in all_group_options]

# Herb group selection
st.subheader("Herb Group Filter")
group_options = get_herb_group_options()
group_labels = [opt['label'] for opt in group_options]
label_to_value = {opt['label']: opt['value'] for opt in group_options}
value_to_label = {opt['value']: opt['label'] for opt in group_options}

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Semester B Herbs", key="semester_b_herbs_btn"):
        st.session_state.herb_practice_group_labels = [
            value_to_label[value]
            for value in get_semester_b_herb_group_values()
            if value in value_to_label
        ]
        st.rerun()
with col2:
    if st.button("Semester A Herbs", key="semester_a_herbs_btn"):
        st.session_state.herb_practice_group_labels = [
            value_to_label[value]
            for value in get_semester_a_herb_group_values()
            if value in value_to_label
        ]
        st.rerun()
with col3:
    if st.button("All Herbs", key="all_herbs_btn"):
        st.session_state.herb_practice_group_labels = group_labels
        st.rerun()

selected_group_labels = st.multiselect(
    "Practice herbs from these groups:",
    options=group_labels,
    key="herb_practice_group_labels",
)
selected_group_values = [label_to_value[label] for label in selected_group_labels if label in label_to_value]

herb_pool = filter_herbs_by_groups(selected_group_values) if selected_group_values else []
st.caption(f"Herbs in current filter: {len(herb_pool)}")

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
    if not selected_group_values:
        st.warning("Please select at least one herb group!")
    elif selected_types:
        st.session_state.herb_practice_question = generate_random_question(selected_types, selected_group_values)
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

