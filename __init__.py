# pylint: disable=missing-module-docstring,attribute-defined-outside-init,broad-exception-caught,invalid-name
from random import choice

from ovos_bus_client.message import Message
from ovos_utils.parse import match_one
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill

INITIAL_MEALS = (
    "Spaghetti and meatballs,Toasted sandwiches and tomato soup,"
    "Chicken noodle soup,Peanut butter and jelly sandwiches"
)


class MealPlanSkill(OVOSSkill):
    """A skill to help plan meals."""

    def __init__(self, *args, bus=None, skill_id="", **kwargs):
        OVOSSkill.__init__(self, *args, bus=bus, skill_id=skill_id, **kwargs)

    @property
    def _core_lang(self):
        """Backwards compatibility for older versions."""
        return self.core_lang

    @property
    def _secondary_langs(self):
        """Backwards compatibility for older versions."""
        return self.secondary_langs

    @property
    def _native_langs(self):
        """Backwards compatibility for older versions."""
        return self.native_langs

    @property
    def meals(self):
        """Get the list of meals from the settings file. Comma-separated string."""
        meals = self.settings.get("meals", INITIAL_MEALS)
        meals = meals.replace(", ", ",").replace(" ,", ",")
        return meals

    @meals.setter
    def meals(self, value):
        self.settings["meals"] = value

    def _remove_meal(self, meal: str) -> str:
        """Remove a meal from our list of meals."""
        meals = self.meals.split(",")
        meals.remove(meal)
        return ",".join(meals)

    @intent_handler("plan.meal.intent")
    def handle_plan_meal(self, _: Message):
        """Handler for initial intent."""
        self.speak_dialog("plan.meal", data={"meal": choice(self.meals.split(","))})

    @intent_handler("add.meal.intent")
    def handle_add_meal(self, _: Message):
        """Wait for a response and add it to meals.json"""
        new_meal = self.get_response("add.meal")
        try:
            self.log.info(f"Adding a new meal: {new_meal}")
            if new_meal:
                self.meals = f"{self.meals},{new_meal}"
                self.speak_dialog("meal.added")
        except Exception as err:
            self.log.exception(err)
            self.speak_dialog("failed.to.add.meal")

    @intent_handler("remove.meal.intent")
    def handle_remove_meal(self, _: Message):
        """Handler for removing a meal from our options."""
        meal_to_remove = self.get_response("remove.meal")
        try:
            best_guess = match_one(meal_to_remove, self.meals)[0]
            self.log.info(f"Confirming we should remove {best_guess}")
            confirm = self.ask_yesno("confirm.remove.meal", {"meal": best_guess})
            if confirm == "yes":
                self.meals = self._remove_meal(best_guess)
                self.speak_dialog("meal.removed")
            else:
                self.acknowledge()
        except Exception as err:
            self.log.exception(err)
            self.speak_dialog("failed.to.remove.meal")

    @intent_handler("list.meal.intent")
    def handle_list_meals(self, _: Message):
        """List all the meals we have. If there are more than 15, ask for confirmation."""
        num_meals = len(self.meals)
        if num_meals > 15:
            confirm = self.ask_yesno("confirm.list.meals", {"num_meals": num_meals})
            if confirm == "no":
                self.speak_dialog("skip.list.meals")
                return
        self.speak_dialog(
            "list.meals.dialog", {"meals": ", ".join(self.meals.split(","))}
        )
