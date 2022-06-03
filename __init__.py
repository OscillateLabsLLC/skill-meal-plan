from json import loads, dump
from os import path
from pathlib import Path
from random import choice
from typing import Dict, List, Union

from mycroft import MycroftSkill, intent_file_handler

INITIAL_MEALS = {"meals": ["Spaghetti and meatballs", "Toasted sandwiches and tomato soup", "Chicken noodle soup"]}


class MealPlan(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.meals_location = Path(Path.home()) / ".config/mycroft/skills/meal-plan-skill/meals.json"
        self.meals_location.touch(exist_ok=True)
        if path.getsize(self.meals_location) == 0:
            with open(self.meals_location, "w") as f:
                dump(INITIAL_MEALS, f)

    def initialize(self):
        self.meals_location = Path(Path.home()) / ".config/mycroft/skills/meal-plan-skill/meals.json"
        self.meals = self._get_meals().get("meals")
        self._save_meals()

    def _get_meals(self) -> Dict[str, List[str]]:
        with open(self.meals_location, "r") as file:
            meals = loads(file.read())
        return meals

    def _save_meals(self) -> None:
        with open(self.meals_location, "w") as f:
            dump({"meals": self.meals}, f)
            self.log.info(f"Saved meals to {self.meals_location}")

    @intent_file_handler("plan.meal.intent")
    def handle_plan_meal(self, message):
        self.meals = self._get_meals().get("meals")
        self.speak_dialog("plan.meal")
        self.speak(choice(self.meals))

    @intent_file_handler("add.meal.intent")
    def handle_add_meal(self):
        # Wait for a response and add it to meals.json
        new_meal = self.get_response("add.meal")
        try:
            self.log.info(f"Adding a new meal: {new_meal}")
            self.meals.append(new_meal)
            self._save_meals()
            self.speak(f"Okay, I've added {new_meal} to your list of meals. Yum!")
        except Exception as e:
            self.log.exception(e)
            self.speak("I wasn't able to add that meal. I'm sorry.")

    @intent_file_handler("remove.meal.intent")
    def handle_remove_meal(self):
        self.speak("I'm sorry, I can't remove meals yet, but I'm learning all the time.")  # TODO:

    @intent_file_handler("list.meal.intent")
    def handle_list_meals(self):
        self.meals = self._get_meals().get("meals")
        if len(self.meals) > 10:
            confirm = self.get_response("Are you sure? You have more than 10 meals listed. This may take some time.")
            if confirm.lower() not in (
                "yes",
                "absolutely",
                "that's fine",
                "i'm sure",
                "do it",
            ):
                self.speak("Okay, I won't bore you.")
                return
        self.speak("Okay, here are all your meal options:")
        self.speak(", ".join(self.meals))


def create_skill():
    return MealPlan()
