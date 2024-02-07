# pylint: disable=missing-docstring
import pytest
from ovos_plugin_manager.skills import find_skill_plugins


def test_skill_is_a_valid_plugin():
    assert "skill-meal-plan.mikejgray" in find_skill_plugins().keys()


if __name__ == "__main__":
    pytest.main()
