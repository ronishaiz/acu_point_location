import streamlit as st

from pages_backend.practice.syndrome_practice import (
    generate_random_question,
    get_syndrome_organ_options,
)


st.set_page_config(
    page_title="Syndrome Practice",
    page_icon="🧠",
)

st.title("🧠 Syndrome Practice")

if "syndrome_practice_question" not in st.session_state:
    st.session_state.syndrome_practice_question = None
if "syndrome_practice_score" not in st.session_state:
    st.session_state.syndrome_practice_score = {"correct": 0, "total": 0}
if "syndrome_practice_answered" not in st.session_state:
    st.session_state.syndrome_practice_answered = False
if "syndrome_practice_organs" not in st.session_state:
    all_organ_options = get_syndrome_organ_options()
    st.session_state.syndrome_practice_organs = [option["value"] for option in all_organ_options]

st.subheader("Organ Filter")
organ_options = get_syndrome_organ_options()
organ_values = [option["value"] for option in organ_options]
selected_organs = st.multiselect(
    "Practice syndromes from these organs:",
    options=organ_values,
    default=[organ for organ in st.session_state.syndrome_practice_organs if organ in organ_values],
    format_func=lambda value: next(option["label"] for option in organ_options if option["value"] == value),
)
st.session_state.syndrome_practice_organs = selected_organs

st.subheader("Question Types")
col1, col2 = st.columns(2)
with col1:
    include_syndrome_to_eight_principles = st.checkbox("Syndrome → Eight Principles", value=True)
    include_syndrome_to_treatment_principle = st.checkbox("Syndrome → Treatment Principle", value=True)
    include_syndrome_to_etiology = st.checkbox("Syndrome → Etiology", value=True)
    include_syndrome_to_pulse = st.checkbox("Syndrome → Pulse", value=True)
with col2:
    include_symptom_cluster_to_syndrome = st.checkbox("Symptoms → Syndrome", value=True)
    include_pulse_to_syndrome = st.checkbox("Pulse → Syndrome", value=True)
    include_tongue_to_syndrome = st.checkbox("Tongue → Syndrome", value=True)
    include_syndrome_to_tongue = st.checkbox("Syndrome → Tongue", value=True)

selected_types = []
if include_syndrome_to_eight_principles:
    selected_types.append("syndrome_to_eight_principles")
if include_syndrome_to_treatment_principle:
    selected_types.append("syndrome_to_treatment_principle")
if include_symptom_cluster_to_syndrome:
    selected_types.append("symptom_cluster_to_syndrome")
if include_pulse_to_syndrome:
    selected_types.append("pulse_to_syndrome")
if include_tongue_to_syndrome:
    selected_types.append("tongue_to_syndrome")
if include_syndrome_to_etiology:
    selected_types.append("syndrome_to_etiology")
if include_syndrome_to_pulse:
    selected_types.append("syndrome_to_pulse")
if include_syndrome_to_tongue:
    selected_types.append("syndrome_to_tongue")

if st.button("Generate Question"):
    if not selected_organs:
        st.warning("Please select at least one organ.")
    elif not selected_types:
        st.warning("Please select at least one question type.")
    else:
        try:
            st.session_state.syndrome_practice_question = generate_random_question(
                question_types=selected_types,
                selected_organs=selected_organs,
            )
            st.session_state.syndrome_practice_answered = False
        except ValueError as error:
            st.error(str(error))

if st.session_state.syndrome_practice_question:
    question = st.session_state.syndrome_practice_question

    st.subheader("Question")
    st.markdown(f"### {question.question}")

    st.subheader("Answer")
    selected_answer = st.radio(
        "Choose the correct answer:",
        question.choices,
        key="syndrome_answer_radio",
    )

    if st.button("Submit Answer"):
        st.session_state.syndrome_practice_answered = True

    if st.session_state.syndrome_practice_answered:
        is_correct = selected_answer == question.correct_answer
        if is_correct:
            st.success("✅ Correct!")
            st.session_state.syndrome_practice_score["correct"] += 1
        else:
            st.error(f"❌ Incorrect! The correct answer is: **{question.correct_answer}**")

        st.session_state.syndrome_practice_score["total"] += 1

    st.divider()
    st.subheader("Score")
    score = st.session_state.syndrome_practice_score
    st.metric(
        "Accuracy",
        f"{score['correct']}/{score['total']}",
        f"{round(100 * score['correct'] / score['total'], 1)}%" if score["total"] > 0 else "0%",
    )

    if st.button("Reset Score"):
        st.session_state.syndrome_practice_score = {"correct": 0, "total": 0}
        st.rerun()
else:
    st.info("👈 Click 'Generate Question' to start practicing.")
