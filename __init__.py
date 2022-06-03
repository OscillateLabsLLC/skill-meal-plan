from json import loads, dump
from random import choice
from typing import Dict, List, Union

from mycroft import MycroftSkill, intent_file_handler


class MealPlan(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.meals: Union[List[str], None] = self.get_meals().get("meals")

    @intent_file_handler("plan.meal.intent")
    def handle_plan_meal(self, message):
        self.speak_dialog("plan.meal")
        self.speak(choice(self.meals))

    def get_meals(self) -> Dict[str, List[str]]:
        with open("/opt/mycroft/skills/meal-plan-skill/meals.json", "r") as f:
            return loads(f.read())

    @intent_file_handler("add.meal.intent")
    def add_meal(self):
        # Wait for a response and add it to meals.json, then call self.get_meals()
        new_meal = self.get_response("add.meal")
        try:
            self.meals.append(new_meal)  # TODO: Better error handling - what failed?
            with open("meals.json", "w") as f:
                self.log.debug({"meals": self.meals})
                f.write(dump({"meals": self.meals}, f))
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
            conf = self.get_response("Are you sure? You have more than 10 meals listed. This may take some time.")
            if conf.lower() not in (
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
