from json import loads, dump
from os.path import isfile
from random import choice
from typing import Dict, List, Union

from mycroft import MycroftSkill, intent_file_handler


class MealPlan(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.meals: Union[List[str], None] = self._get_meals().get("meals")
        self.meal_location = "~/.config/mycroft/skills/meal-plan-skill/meals.json"
        self.first_run = self._first_run()

    def _first_run(self) -> bool:
        return not isfile(self.meal_location)

    def _get_meals(self) -> Dict[str, List[str]]:
        if self.first_run is True:
            with open("./meals.json", "r") as f:
                with open(self.meal_location, "w") as file:
                    file.write(f.read())
                    meals = loads(f.read())
            self.first_run = False
        else:
            with open(self.meal_location, "w") as file:
                meals = loads(file.read())
        return meals

    def _save_meals(self) -> None:
        with open(self.meals_location, "w") as f:
            dump({"meals": self.meals}, f)
            self.log.info(f"Saved meals to {self.meals_location}")

    @intent_file_handler("plan.meal.intent")
    def handle_plan_meal(self, message):
        self.speak_dialog("plan.meal")
        self.speak(choice(self.meals))

    @intent_file_handler("add.meal.intent")
    def add_meal(self):
        # Wait for a response and add it to meals.json
        new_meal = self.get_response("add.meal")
        try:
            self.log.info(f"Adding a new meal: {new_meal}")
            self.meals.append(new_meal)  # TODO: Better error handling - what failed?
            self._save_meals()
            self.speak(f"Okay, I've added {new_meal} to your list of meals. Yum!")
        except Exception as e:
            self.log.exception(e)
            self.speak("I wasn't able to add that meal. I'm sorry.")

    @intent_file_handler("remove.meal.intent")
    def remove_meal(self):
        self.speak("I'm sorry, I can't remove meals yet, but I'm learning all the time.")  # TODO:

    @intent_file_handler("list.meal.intent")
    def list_meals(self):
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
