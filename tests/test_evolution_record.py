from uuid import UUID

import pytest
from pydantic import ValidationError

from stem_agent.schemas.enums import PromptSectionKey
from stem_agent.schemas.evolution_record import EvolutionRecord


def test_valid_evolution_record():
    evolution_record = EvolutionRecord(
        evolution_run_id=UUID(int=0),
        iteration=5,
        current_config_version=1,
        candidate_config_version=2,
        current_score=3.5,
        candidate_score=4.5,
        accepted=True,
        mutation_target=PromptSectionKey("quality_constraints"),
        mutation_reason="Coverage field was updated due to poor coverage of users requests.",
        evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
    )

    assert evolution_record.iteration == 5
    assert evolution_record.current_config_version == 1
    assert evolution_record.candidate_config_version == 2
    assert evolution_record.current_score == 3.5
    assert evolution_record.candidate_score == 4.5
    assert evolution_record.accepted is True
    assert evolution_record.mutation_target == PromptSectionKey.QUALITY_CONSTRAINTS
    assert evolution_record.mutation_reason == "Coverage field was updated due to poor coverage of users requests."
    assert evolution_record.evaluator_feedback == "The cycle was generally successful, but coverage of all aspects could be improved."
    assert evolution_record.score_delta == 1.0
    assert evolution_record.timestamp is not None

def test_valid_rejected_evolution_record():
    evolution_record = EvolutionRecord(
        evolution_run_id=UUID(int=0),
        iteration=4,
        current_config_version=3,
        candidate_config_version=4,
        current_score=3.5,
        candidate_score=2.5,
        accepted=False,
        mutation_target=PromptSectionKey.STRATEGY,
        mutation_reason="Strategy mutation was tested but reduced the overall score.",
        evaluator_feedback="The candidate answer became less focused and lost useful structure.",
    )

    assert evolution_record.accepted is False
    assert evolution_record.current_score == 3.5
    assert evolution_record.candidate_score == 2.5
    assert evolution_record.score_delta == -1.0
    assert evolution_record.mutation_target == PromptSectionKey.STRATEGY

def test_invalid_iteration_equals_zero():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=0,
            current_config_version=1,
            candidate_config_version=2,
            current_score=3.5,
            candidate_score=4.5,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_current_config_version_equals_zero():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=2,
            current_config_version=0,
            candidate_config_version=2,
            current_score=3.5,
            candidate_score=4.5,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_candidate_config_version_equals_zero():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=2,
            current_config_version=1,
            candidate_config_version=0,
            current_score=3.5,
            candidate_score=4.5,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_current_score_below_one():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=0.5,
            candidate_score=4.5,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_current_score_above_five():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=6,
            candidate_score=4.5,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_candidate_score_below_one():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=2,
            candidate_score=0.5,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_candidate_score_above_five():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=2,
            candidate_score=6,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_mutation_target():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=2,
            candidate_score=3,
            accepted=True,
            mutation_target="tool_choice",
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_mutation_reason_empty_string():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=2,
            candidate_score=3,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_mutation_reason_whitespace():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=2,
            candidate_score=3,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason=" ",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )

def test_invalid_evaluator_feedback_empty_string():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=2,
            candidate_score=3,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="",
        )

def test_invalid_evaluator_feedback_whitespace():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=2,
            current_score=2,
            candidate_score=3,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback=" ",
        )

def test_score_calculation():
    evolution_record = EvolutionRecord(
        evolution_run_id=UUID(int=0),
        iteration=3,
        current_config_version=1,
        candidate_config_version=2,
        current_score=2,
        candidate_score=3,
        accepted=True,
        mutation_target=PromptSectionKey("quality_constraints"),
        mutation_reason="Coverage field was updated due to poor coverage of users requests.",
        evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
    )
    assert evolution_record.score_delta == 1.0

def test_versions_constraint():
    with pytest.raises(ValidationError):
        EvolutionRecord(
            evolution_run_id=UUID(int=0),
            iteration=3,
            current_config_version=1,
            candidate_config_version=1,
            current_score=2,
            candidate_score=3,
            accepted=True,
            mutation_target=PromptSectionKey("quality_constraints"),
            mutation_reason="Coverage field was updated due to poor coverage of users requests.",
            evaluator_feedback="The cycle was generally successful, but coverage of all aspects could be improved.",
        )