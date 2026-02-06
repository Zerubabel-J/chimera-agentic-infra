"""
Tests for the fetch_trends skill.

Spec Reference: FR-A01 (specs/functional.md)
Contract: TrendResult (specs/technical.md Section 1.1)

These tests define the CONTRACT that any implementation of fetch_trends
must satisfy. They are intentionally written BEFORE implementation (TDD).
"""

from datetime import datetime, timedelta, timezone

import pytest


class TestTrendResultContract:
    """Validates that TrendResult matches the API contract in specs/technical.md"""

    def test_trend_result_has_required_fields(self):
        """TrendResult must contain: topics, agent_id, fetch_timestamp, platform, topic_count"""
        from skills.fetch_trends.models import TrendResult

        result = TrendResult(
            topics=[],
            agent_id="test-agent-001",
            fetch_timestamp=datetime.now(timezone.utc),
            platform="twitter",
            topic_count=0,
        )
        assert hasattr(result, "topics")
        assert hasattr(result, "agent_id")
        assert hasattr(result, "fetch_timestamp")
        assert hasattr(result, "platform")
        assert hasattr(result, "topic_count")

    def test_trend_topic_has_required_fields(self):
        """Each TrendTopic must have: name, category, engagement_score, source_url,
        source_platform, fetched_at"""
        from skills.fetch_trends.models import TrendTopic

        topic = TrendTopic(
            name="Test Trend",
            category="fashion",
            engagement_score=0.85,
            source_url="https://example.com",
            source_platform="twitter",
            fetched_at=datetime.now(timezone.utc),
        )
        assert topic.name == "Test Trend"
        assert topic.category == "fashion"
        assert topic.engagement_score == 0.85
        assert topic.source_url == "https://example.com"

    def test_engagement_score_must_be_between_0_and_1(self):
        """Per specs/technical.md: engagement_score is float (0.0 - 1.0)"""
        from skills.fetch_trends.models import TrendTopic

        # Valid scores should work
        valid_topic = TrendTopic(
            name="Test",
            category="tech",
            engagement_score=0.5,
            source_url="https://example.com",
            source_platform="twitter",
            fetched_at=datetime.now(timezone.utc),
        )
        assert valid_topic.engagement_score == 0.5

        # Score > 1.0 should be rejected
        with pytest.raises(ValueError):
            TrendTopic(
                name="Test",
                category="tech",
                engagement_score=1.5,
                source_url="https://example.com",
                source_platform="twitter",
                fetched_at=datetime.now(timezone.utc),
            )

        # Score < 0.0 should be rejected
        with pytest.raises(ValueError):
            TrendTopic(
                name="Test",
                category="tech",
                engagement_score=-0.1,
                source_url="https://example.com",
                source_platform="twitter",
                fetched_at=datetime.now(timezone.utc),
            )

    def test_category_must_be_valid_enum(self):
        """Per specs/technical.md: category is enum with defined values"""
        from skills.fetch_trends.models import TrendTopic

        valid_categories = ["fashion", "tech", "politics", "entertainment",
                           "sports", "business", "other"]

        for cat in valid_categories:
            topic = TrendTopic(
                name="Test",
                category=cat,
                engagement_score=0.5,
                source_url="https://example.com",
                source_platform="twitter",
                fetched_at=datetime.now(timezone.utc),
            )
            assert topic.category == cat

        # Invalid category should be rejected
        with pytest.raises(ValueError):
            TrendTopic(
                name="Test",
                category="invalid_category",
                engagement_score=0.5,
                source_url="https://example.com",
                source_platform="twitter",
                fetched_at=datetime.now(timezone.utc),
            )

    def test_topic_count_matches_actual_topics(self):
        """topic_count must reflect the actual number of topics returned"""
        from skills.fetch_trends.models import TrendResult, TrendTopic

        topics = [
            TrendTopic(
                name=f"Trend {i}",
                category="tech",
                engagement_score=0.5,
                source_url="https://example.com",
                source_platform="twitter",
                fetched_at=datetime.now(timezone.utc),
            )
            for i in range(3)
        ]

        result = TrendResult(
            topics=topics,
            agent_id="test-agent",
            fetch_timestamp=datetime.now(timezone.utc),
            platform="twitter",
            topic_count=3,
        )
        assert result.topic_count == len(result.topics)


class TestTrendFetcherBehavior:
    """Validates the behavioral requirements from FR-A01 acceptance criteria"""

    def test_fetcher_returns_max_10_topics(self):
        """FR-A01: Fetch top 10 trending topics"""
        from skills.fetch_trends.service import fetch_trends

        result = fetch_trends(
            agent_id="test-agent",
            platform="twitter",
            niche="fashion",
        )
        assert len(result.topics) <= 10

    def test_fetcher_discards_stale_data(self):
        """FR-A01: Stale data (older than 8 hours) is automatically discarded"""
        from skills.fetch_trends.service import fetch_trends

        result = fetch_trends(
            agent_id="test-agent",
            platform="twitter",
            niche="fashion",
            max_age_hours=8,
        )
        cutoff = datetime.now(timezone.utc) - timedelta(hours=8)
        for topic in result.topics:
            assert topic.fetched_at >= cutoff
