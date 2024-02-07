# pylint: disable=missing-docstring
import pytest
from ovos_plugin_manager.skills import find_skill_plugins


def test_skill_is_a_valid_plugin():
    skills = ",".join(find_skill_plugins().keys())
    assert "skill-meal-plan.mikejgray" in skills


if __name__ == "__main__":
    pytest.main()
