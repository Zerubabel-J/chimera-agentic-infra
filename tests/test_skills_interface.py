"""
Tests for skill module interfaces.

Validates that all skills in skills/ conform to the expected structure
and accept/return the correct data shapes per specs/technical.md.

These tests define the INTERFACE CONTRACT that every skill must follow.
Written BEFORE implementation (TDD approach).
"""

import importlib

import pytest


class TestSkillModuleStructure:
    """Every skill must be a proper Python package with required components"""

    @pytest.mark.parametrize("skill_name", [
        "fetch_trends",
        "generate_content",
        "evaluate_content",
    ])
    def test_skill_package_is_importable(self, skill_name):
        """Each skill must be importable as skills.<name>"""
        module = importlib.import_module(f"skills.{skill_name}")
        assert module is not None

    @pytest.mark.parametrize("skill_name", [
        "fetch_trends",
        "generate_content",
        "evaluate_content",
    ])
    def test_skill_has_models_module(self, skill_name):
        """Each skill must have a models.py defining its Pydantic contracts"""
        models = importlib.import_module(f"skills.{skill_name}.models")
        assert models is not None

    @pytest.mark.parametrize("skill_name", [
        "fetch_trends",
        "generate_content",
        "evaluate_content",
    ])
    def test_skill_has_service_module(self, skill_name):
        """Each skill must have a service.py containing the main logic"""
        service = importlib.import_module(f"skills.{skill_name}.service")
        assert service is not None


class TestFetchTrendsInterface:
    """Validates fetch_trends skill interface per specs/technical.md Section 1.1"""

    def test_service_has_fetch_trends_function(self):
        """fetch_trends skill must expose a fetch_trends() function"""
        from skills.fetch_trends.service import fetch_trends
        assert callable(fetch_trends)

    def test_fetch_trends_accepts_required_params(self):
        """fetch_trends must accept: agent_id, platform, niche"""
        import inspect

        from skills.fetch_trends.service import fetch_trends

        sig = inspect.signature(fetch_trends)
        param_names = list(sig.parameters.keys())
        assert "agent_id" in param_names
        assert "platform" in param_names
        assert "niche" in param_names

    def test_fetch_trends_returns_trend_result(self):
        """fetch_trends must return a TrendResult object"""
        from skills.fetch_trends.models import TrendResult
        from skills.fetch_trends.service import fetch_trends

        result = fetch_trends(
            agent_id="test-agent",
            platform="twitter",
            niche="fashion",
        )
        assert isinstance(result, TrendResult)


class TestGenerateContentInterface:
    """Validates generate_content skill interface per specs/technical.md Section 1.2"""

    def test_service_has_generate_function(self):
        """generate_content skill must expose a generate() function"""
        from skills.generate_content.service import generate
        assert callable(generate)

    def test_generate_returns_generated_content(self):
        """generate must return a GeneratedContent object"""
        from skills.generate_content.models import GeneratedContent
        from skills.generate_content.service import generate

        result = generate(
            agent_id="test-agent",
            trend_topic="Ethiopian Fashion",
            platform="twitter",
        )
        assert isinstance(result, GeneratedContent)


class TestEvaluateContentInterface:
    """Validates evaluate_content skill interface per specs/technical.md Section 1.3"""

    def test_service_has_evaluate_function(self):
        """evaluate_content skill must expose an evaluate() function"""
        from skills.evaluate_content.service import evaluate
        assert callable(evaluate)

    def test_evaluate_returns_judge_decision(self):
        """evaluate must return a JudgeDecision object"""
        from skills.evaluate_content.models import JudgeDecision
        from skills.evaluate_content.service import evaluate

        result = evaluate(
            content_id="test-content-001",
            text="Test tweet about fashion",
            platform="twitter",
        )
        assert isinstance(result, JudgeDecision)

    def test_judge_verdict_is_valid_enum(self):
        """verdict must be one of: APPROVE, REVIEW, REJECT"""
        from skills.evaluate_content.service import evaluate

        result = evaluate(
            content_id="test-content-001",
            text="Test tweet about fashion",
            platform="twitter",
        )
        assert result.verdict in ("APPROVE", "REVIEW", "REJECT")
