import pytest
from unittest.mock import patch
from tech_news.analyzer.reading_plan import ReadingPlanService


def mock_find_news():
    return [
        {"title": "Notícia 1", "reading_time": 4},
        {"title": "Notícia 2", "reading_time": 3},
        {"title": "Notícia 3", "reading_time": 10},
        {"title": "Notícia 4", "reading_time": 15},
        {"title": "Notícia 5", "reading_time": 12},
    ]


def test_reading_plan_group_news():
    with pytest.raises(
       ValueError, match="Valor 'available_time' deve ser maior que zero"):
        ReadingPlanService.group_news_for_available_time(0)

    with patch('tech_news.analyzer.reading_plan.find_news', mock_find_news):
        result = ReadingPlanService.group_news_for_available_time(10)

        expected_readable = [
            {
                "unfilled_time": 3,
                "chosen_news": [("Notícia 1", 4), ("Notícia 2", 3)]
            },
            {
                "unfilled_time": 0,
                "chosen_news": [("Notícia 3", 10)]
            }
        ]
        assert result["readable"] == expected_readable

        expected_unreadable = [
            ("Notícia 4", 15),
            ("Notícia 5", 12)
        ]
        assert result["unreadable"] == expected_unreadable
