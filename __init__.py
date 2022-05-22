from mycroft import MycroftSkill, intent_file_handler


class MealPlan(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('plan.meal.intent')
    def handle_plan_meal(self, message):
        self.speak_dialog('plan.meal')


def create_skill():
    return MealPlan()

