# pylint: disable=missing-docstring
import shutil
import string
from json import dumps
from os import environ, getenv, makedirs
from os.path import dirname, isdir, join
from unittest.mock import Mock

import pytest
from ovos_plugin_manager.skills import find_skill_plugins
from ovos_utils.fakebus import FakeBus
from skill_meal_plan import MealPlanSkill


@pytest.fixture(scope="session")
def test_skill(test_skill_id="skill-meal-plan.mikejgray", bus=FakeBus()):
    # Get test skill
    bus.emitter = bus.ee
    bus.run_forever()
    skill_entrypoint = getenv("TEST_SKILL_ENTRYPOINT")
    if not skill_entrypoint:
        skill_entrypoints = list(find_skill_plugins().keys())
        assert test_skill_id in skill_entrypoints
        skill_entrypoint = test_skill_id

    skill = MealPlanSkill(skill_id=test_skill_id, bus=bus)
    skill.speak = Mock()
    skill.speak_dialog = Mock()
    skill.play_audio = Mock()
    yield skill
    shutil.rmtree(join(dirname(__file__), "skill_fs"), ignore_errors=False)


@pytest.fixture(scope="function")
def reset_skill_mocks(test_skill):
    # Reset mocks before each test
    test_skill.speak.reset_mock()
    test_skill.speak_dialog.reset_mock()
    test_skill.play_audio.reset_mock()


class TestRandomnessSkill:
    test_fs = join(dirname(__file__), "skill_fs")
    data_dir = join(test_fs, "data")
    conf_dir = join(test_fs, "config")
    environ["XDG_DATA_HOME"] = data_dir
    environ["XDG_CONFIG_HOME"] = conf_dir
    if not isdir(test_fs):
        makedirs(data_dir)
        makedirs(conf_dir)

    with open(join(conf_dir, "mycroft.conf"), "w", encoding="utf-8") as f:
        f.write(dumps({"Audio": {"backends": {"ocp": {"active": False}}}}))

    def test_skill_is_a_valid_plugin(self, test_skill):
        assert "skill-meal-plan.mikejgray" in find_skill_plugins()

    def test_list_meals(self, test_skill):
        test_skill.meals = "Spaghetti and meatballs,Toasted sandwiches and tomato soup,Chicken noodle soup,Peanut butter and jelly sandwiches"
        test_skill.ask_yesno = Mock(return_value="yes")
        test_skill.handle_list_meals(None)
        test_skill.speak_dialog.assert_called()
        test_skill.speak_dialog.assert_called_with(
            "list.meals",
            {
                "meals": "Spaghetti and meatballs, Toasted sandwiches and tomato soup, Chicken noodle soup, Peanut butter and jelly sandwiches"
            },
        )

    def test_list_default_meals(self, test_skill):
        test_skill.ask_yesno = Mock(return_value="yes")
        test_skill.handle_list_meals(None)
        test_skill.speak_dialog.assert_called()
        test_skill.ask_yesno.assert_not_called()
        test_skill.speak_dialog.assert_called_with(
            "list.meals",
            {
                "meals": "Spaghetti and meatballs, Toasted sandwiches and tomato soup, Chicken noodle soup, Peanut butter and jelly sandwiches"
            },
        )

    def test_long_list_of_meals(self, test_skill):
        test_skill.ask_yesno = Mock(return_value="yes")
        test_skill.meals = ",".join(list(string.printable))
        test_skill.handle_list_meals(None)
        assert test_skill.speak_dialog.called is True
        test_skill.ask_yesno.assert_called()
        test_skill.speak_dialog.assert_called_with(
            "list.meals",
            {
                "meals": "0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, !, \", #, $, %, &, ', (, ), *, +, , , -, ., /, :, ;, <, =, >, ?, @, [, \\, ], ^, _, `, {, |, }, ~, , \t, \n, \r, \x0b, \x0c"
            },
        )


if __name__ == "__main__":
    pytest.main()
