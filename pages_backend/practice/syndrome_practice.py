import random
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Set

from backend.syndromes.syndrome import ALL_SYNDROMES, Syndrome


MAX_CHOICES = 4


@dataclass
class SyndromeQuestion:
    question: str
    correct_answer: str
    choices: List[str]
    question_type: Literal[
        "syndrome_to_eight_principles",
        "syndrome_to_treatment_principle",
        "symptom_cluster_to_syndrome",
        "pulse_to_syndrome",
        "tongue_to_syndrome",
        "syndrome_to_etiology",
        "syndrome_to_pulse",
        "syndrome_to_tongue",
    ]


def get_syndrome_organ_options() -> List[dict]:
    counts_by_organ: Dict[str, int] = {}
    for syndrome in ALL_SYNDROMES:
        organ_value = syndrome.organ.value
        counts_by_organ[organ_value] = counts_by_organ.get(organ_value, 0) + 1

    return [
        {
            "value": organ,
            "label": f"{organ} ({count})",
        }
        for organ, count in sorted(counts_by_organ.items())
    ]


def filter_syndromes_by_organs(selected_organs: List[str]) -> List[Syndrome]:
    selected_set = set(selected_organs)
    return [
        syndrome
        for syndrome in ALL_SYNDROMES
        if syndrome.organ.value in selected_set
    ]


def _resolve_syndrome_pool(selected_organs: Optional[List[str]] = None) -> List[Syndrome]:
    syndrome_pool = filter_syndromes_by_organs(selected_organs) if selected_organs else ALL_SYNDROMES
    if not syndrome_pool:
        raise ValueError("No syndromes found for the selected organs")
    return syndrome_pool


def _sample_distractors(candidates: List[str], correct_answer: str, max_distractors: int = 3) -> List[str]:
    unique_candidates = [candidate for candidate in dict.fromkeys(candidates) if candidate != correct_answer]
    if not unique_candidates:
        return []

    sample_size = min(max_distractors, len(unique_candidates))
    return random.sample(unique_candidates, sample_size)


def _format_eight_principles(syndrome: Syndrome) -> str:
    principles = syndrome.diagnosis.eight_principles
    parts = []
    if principles.intenal_external:
        parts.append(principles.intenal_external.value)
    if principles.full_empty:
        parts.append(principles.full_empty.value)
    if principles.hot_cold:
        parts.append(principles.hot_cold.value)
    if principles.yin_yang:
        parts.append(principles.yin_yang.value)

    return " | ".join(parts)


def _format_pulse(syndrome: Syndrome) -> str:
    pulse = syndrome.diagnosis.pulse
    if not pulse:
        return "No pulse data"

    parts = []
    if pulse._speed:
        parts.append(f"Speed: {pulse._speed.value}")
    if pulse._depth:
        parts.append(f"Depth: {pulse._depth.value}")
    if pulse._strength:
        parts.append(f"Strength: {pulse._strength.value}")
    if pulse._quality:
        parts.append("Quality: " + ", ".join([quality.value for quality in pulse._quality]))
    if pulse._positions:
        positions = [
            "/".join([position.yin_yang.value, position.jiao.value, position.left_right.value])
            for position in pulse._positions
        ]
        parts.append("Positions: " + ", ".join(positions))

    return " | ".join(parts)


def _format_tongue(syndrome: Syndrome) -> str:
    tongue = syndrome.diagnosis.tongue
    if not tongue:
        return "No tongue data"

    parts = []
    if tongue.body_color:
        parts.append(f"Body Color: {tongue.body_color.value}")
    if tongue.body_shapes:
        parts.append("Body Shapes: " + ", ".join([shape.value for shape in tongue.body_shapes]))
    if tongue.coating_color:
        parts.append(f"Coating Color: {tongue.coating_color.value}")
    if tongue.coating_thickness:
        parts.append(f"Coating Thickness: {tongue.coating_thickness.value}")
    if tongue.moisture:
        parts.append(f"Moisture: {tongue.moisture.value}")
    if tongue.region:
        parts.append(f"Region: {tongue.region.value}")

    return " | ".join(parts)


def _pulse_signature(syndrome: Syndrome) -> Set[str]:
    pulse = syndrome.diagnosis.pulse
    if not pulse:
        return set()

    signature: Set[str] = set()
    if pulse._speed:
        signature.add(f"speed:{pulse._speed.value}")
    if pulse._depth:
        signature.add(f"depth:{pulse._depth.value}")
    if pulse._strength:
        signature.add(f"strength:{pulse._strength.value}")
    for quality in pulse._quality or []:
        signature.add(f"quality:{quality.value}")
    for position in pulse._positions or []:
        signature.add(f"position:{position.yin_yang.value}/{position.jiao.value}/{position.left_right.value}")
    return signature


def _tongue_signature(syndrome: Syndrome) -> Set[str]:
    tongue = syndrome.diagnosis.tongue
    if not tongue:
        return set()

    signature: Set[str] = set()
    if tongue.body_color:
        signature.add(f"body_color:{tongue.body_color.value}")
    for shape in tongue.body_shapes or []:
        signature.add(f"body_shape:{shape.value}")
    if tongue.coating_color:
        signature.add(f"coating_color:{tongue.coating_color.value}")
    if tongue.coating_thickness:
        signature.add(f"coating_thickness:{tongue.coating_thickness.value}")
    if tongue.moisture:
        signature.add(f"moisture:{tongue.moisture.value}")
    if tongue.region:
        signature.add(f"region:{tongue.region.value}")
    return signature


def _jaccard_similarity(a: Set[str], b: Set[str]) -> float:
    union = a.union(b)
    if not union:
        return 0.0
    return len(a.intersection(b)) / len(union)


def _select_low_similarity_distractors(
    correct_syndrome: Syndrome,
    candidates: List[Syndrome],
    signature_builder,
    threshold: float = 0.55,
) -> List[Syndrome]:
    correct_signature = signature_builder(correct_syndrome)
    scored_candidates = []

    for candidate in candidates:
        if candidate.name == correct_syndrome.name:
            continue
        similarity = _jaccard_similarity(correct_signature, signature_builder(candidate))
        scored_candidates.append((similarity, candidate))

    # Prefer distractors under threshold to avoid near-duplicates.
    low_similarity = [candidate for similarity, candidate in scored_candidates if similarity <= threshold]
    if len(low_similarity) >= (MAX_CHOICES - 1):
        return random.sample(low_similarity, MAX_CHOICES - 1)

    # If data is sparse, backfill with the least similar choices.
    scored_candidates.sort(key=lambda item: item[0])
    least_similar = [candidate for _, candidate in scored_candidates]
    return least_similar[: max(0, MAX_CHOICES - 1)]


def generate_syndrome_to_eight_principles_question(syndrome_pool: List[Syndrome]) -> SyndromeQuestion:
    syndromes_with_principles = [s for s in syndrome_pool if s.diagnosis.eight_principles]
    if len(syndromes_with_principles) < 2:
        raise ValueError("Not enough syndromes with eight-principles data")

    syndrome = random.choice(syndromes_with_principles)
    correct_answer = _format_eight_principles(syndrome)

    distractor_pool = [
        _format_eight_principles(other)
        for other in syndromes_with_principles
        if other.name != syndrome.name
    ]
    choices = [correct_answer] + _sample_distractors(distractor_pool, correct_answer)
    random.shuffle(choices)

    return SyndromeQuestion(
        question=f"Which eight-principles pattern matches **{syndrome.name}**?",
        correct_answer=correct_answer,
        choices=choices,
        question_type="syndrome_to_eight_principles",
    )


def generate_syndrome_to_treatment_principle_question(syndrome_pool: List[Syndrome]) -> SyndromeQuestion:
    syndromes_with_treatment = [s for s in syndrome_pool if s.treatment.principle]
    if len(syndromes_with_treatment) < 2:
        raise ValueError("Not enough syndromes with treatment-principle data")

    syndrome = random.choice(syndromes_with_treatment)
    correct_answer = syndrome.treatment.principle

    distractor_pool = [
        other.treatment.principle
        for other in syndromes_with_treatment
        if other.name != syndrome.name and other.treatment.principle
    ]
    choices = [correct_answer] + _sample_distractors(distractor_pool, correct_answer)
    random.shuffle(choices)

    return SyndromeQuestion(
        question=f"What is the treatment principle for **{syndrome.name}**?",
        correct_answer=correct_answer,
        choices=choices,
        question_type="syndrome_to_treatment_principle",
    )


def generate_symptom_cluster_to_syndrome_question(syndrome_pool: List[Syndrome]) -> SyndromeQuestion:
    syndromes_with_symptoms = [s for s in syndrome_pool if s.diagnosis.symptoms]
    if len(syndromes_with_symptoms) < 2:
        raise ValueError("Not enough syndromes with symptoms data")

    syndrome = random.choice(syndromes_with_symptoms)
    symptom_source = syndrome.diagnosis.key_symptoms or syndrome.diagnosis.symptoms
    symptom_count = min(4, len(symptom_source))
    symptom_count = max(2, symptom_count)
    chosen_symptoms = random.sample(symptom_source, symptom_count) if len(symptom_source) >= symptom_count else symptom_source

    question_symptoms = "\n".join([f"- {symptom}" for symptom in chosen_symptoms])

    correct_answer = syndrome.name
    distractor_pool = [
        other.name
        for other in syndromes_with_symptoms
        if other.name != syndrome.name
    ]
    choices = [correct_answer] + _sample_distractors(distractor_pool, correct_answer)
    random.shuffle(choices)

    return SyndromeQuestion(
        question=f"Which syndrome best matches this symptom cluster?\n\n{question_symptoms}",
        correct_answer=correct_answer,
        choices=choices,
        question_type="symptom_cluster_to_syndrome",
    )


def generate_pulse_to_syndrome_question(syndrome_pool: List[Syndrome]) -> SyndromeQuestion:
    syndromes_with_pulse = [s for s in syndrome_pool if s.diagnosis.pulse]
    if len(syndromes_with_pulse) < 2:
        raise ValueError("Not enough syndromes with pulse data")

    syndrome = random.choice(syndromes_with_pulse)
    correct_answer = syndrome.name

    distractor_syndromes = _select_low_similarity_distractors(
        correct_syndrome=syndrome,
        candidates=syndromes_with_pulse,
        signature_builder=_pulse_signature,
    )

    choices = [correct_answer] + [candidate.name for candidate in distractor_syndromes]
    random.shuffle(choices)

    return SyndromeQuestion(
        question=f"Which syndrome is most consistent with this pulse pattern?\n\n{_format_pulse(syndrome)}",
        correct_answer=correct_answer,
        choices=choices,
        question_type="pulse_to_syndrome",
    )


def generate_tongue_to_syndrome_question(syndrome_pool: List[Syndrome]) -> SyndromeQuestion:
    syndromes_with_tongue = [s for s in syndrome_pool if s.diagnosis.tongue]
    if len(syndromes_with_tongue) < 2:
        raise ValueError("Not enough syndromes with tongue data")

    syndrome = random.choice(syndromes_with_tongue)
    correct_answer = syndrome.name

    distractor_syndromes = _select_low_similarity_distractors(
        correct_syndrome=syndrome,
        candidates=syndromes_with_tongue,
        signature_builder=_tongue_signature,
    )

    choices = [correct_answer] + [candidate.name for candidate in distractor_syndromes]
    random.shuffle(choices)

    return SyndromeQuestion(
        question=f"Which syndrome is most consistent with this tongue presentation?\n\n{_format_tongue(syndrome)}",
        correct_answer=correct_answer,
        choices=choices,
        question_type="tongue_to_syndrome",
    )


def generate_syndrome_to_etiology_question(syndrome_pool: List[Syndrome]) -> SyndromeQuestion:
    syndromes_with_etiology = [s for s in syndrome_pool if s.etiology]
    if len(syndromes_with_etiology) < 2:
        raise ValueError("Not enough syndromes with etiology data")

    syndrome = random.choice(syndromes_with_etiology)
    correct_answer = random.choice(syndrome.etiology)

    all_etiologies = []
    for other in syndromes_with_etiology:
        all_etiologies.extend(other.etiology)

    choices = [correct_answer] + _sample_distractors(all_etiologies, correct_answer)
    random.shuffle(choices)

    return SyndromeQuestion(
        question=f"Which etiology is associated with **{syndrome.name}**?",
        correct_answer=correct_answer,
        choices=choices,
        question_type="syndrome_to_etiology",
    )


def generate_syndrome_to_pulse_question(syndrome_pool: List[Syndrome]) -> SyndromeQuestion:
    syndromes_with_pulse = [s for s in syndrome_pool if s.diagnosis.pulse]
    if len(syndromes_with_pulse) < 2:
        raise ValueError("Not enough syndromes with pulse data")

    syndrome = random.choice(syndromes_with_pulse)
    correct_answer = _format_pulse(syndrome)

    distractor_syndromes = _select_low_similarity_distractors(
        correct_syndrome=syndrome,
        candidates=syndromes_with_pulse,
        signature_builder=_pulse_signature,
    )
    distractors = [_format_pulse(candidate) for candidate in distractor_syndromes]

    choices = [correct_answer] + _sample_distractors(distractors, correct_answer)
    random.shuffle(choices)

    return SyndromeQuestion(
        question=f"Which pulse pattern best matches **{syndrome.name}**?",
        correct_answer=correct_answer,
        choices=choices,
        question_type="syndrome_to_pulse",
    )


def generate_syndrome_to_tongue_question(syndrome_pool: List[Syndrome]) -> SyndromeQuestion:
    syndromes_with_tongue = [s for s in syndrome_pool if s.diagnosis.tongue]
    if len(syndromes_with_tongue) < 2:
        raise ValueError("Not enough syndromes with tongue data")

    syndrome = random.choice(syndromes_with_tongue)
    correct_answer = _format_tongue(syndrome)

    distractor_syndromes = _select_low_similarity_distractors(
        correct_syndrome=syndrome,
        candidates=syndromes_with_tongue,
        signature_builder=_tongue_signature,
    )
    distractors = [_format_tongue(candidate) for candidate in distractor_syndromes]

    choices = [correct_answer] + _sample_distractors(distractors, correct_answer)
    random.shuffle(choices)

    return SyndromeQuestion(
        question=f"Which tongue presentation best matches **{syndrome.name}**?",
        correct_answer=correct_answer,
        choices=choices,
        question_type="syndrome_to_tongue",
    )


def generate_random_question(
    question_types: Optional[List[str]] = None,
    selected_organs: Optional[List[str]] = None,
) -> SyndromeQuestion:
    if not question_types:
        question_types = [
            "syndrome_to_eight_principles",
            "syndrome_to_treatment_principle",
            "symptom_cluster_to_syndrome",
            "pulse_to_syndrome",
            "tongue_to_syndrome",
            "syndrome_to_etiology",
            "syndrome_to_pulse",
            "syndrome_to_tongue",
        ]

    syndrome_pool = _resolve_syndrome_pool(selected_organs)

    generators = {
        "syndrome_to_eight_principles": generate_syndrome_to_eight_principles_question,
        "syndrome_to_treatment_principle": generate_syndrome_to_treatment_principle_question,
        "symptom_cluster_to_syndrome": generate_symptom_cluster_to_syndrome_question,
        "pulse_to_syndrome": generate_pulse_to_syndrome_question,
        "tongue_to_syndrome": generate_tongue_to_syndrome_question,
        "syndrome_to_etiology": generate_syndrome_to_etiology_question,
        "syndrome_to_pulse": generate_syndrome_to_pulse_question,
        "syndrome_to_tongue": generate_syndrome_to_tongue_question,
    }

    shuffled_types = question_types[:]
    random.shuffle(shuffled_types)

    errors = []
    for question_type in shuffled_types:
        generator = generators.get(question_type)
        if not generator:
            continue
        try:
            return generator(syndrome_pool)
        except ValueError as error:
            errors.append(str(error))

    raise ValueError(
        "Unable to generate a syndrome question with the current filters and question types. "
        + "; ".join(errors)
    )
