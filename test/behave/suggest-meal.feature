Feature: suggest-meal
  Scenario: Suggest a random meal 1
    Given an English speaking user
     When the user says "what should i make for dinner?"
     Then "meal-plan-skill" should reply with dialog from "plan.meal.dialog"
  Scenario: Suggest a random meal 2
    Given an English speaking user
      When the user says "what should i have for dinner?"
      Then "meal-plan-skill" should reply with dialog from "plan.meal.dialog"
  Scenario: Suggest a random meal 3
    Given an English speaking user
      When the user says "what should i eat for dinner?"
      Then "meal-plan-skill" should reply with dialog from "plan.meal.dialog"
  Scenario: Suggest a random meal 4
    Given an English speaking user
      When the user says "what should i eat?"
      Then "meal-plan-skill" should reply with dialog from "plan.meal.dialog"
  Scenario: Suggest a random meal 5
    Given an English speaking user
      When the user says "what should i eat tonight?"
      Then "meal-plan-skill" should reply with dialog from "plan.meal.dialog"
  Scenario: Suggest a random meal 6
    Given an English speaking user
      When the user says "i'm hungry"
      Then "meal-plan-skill" should reply with dialog from "plan.meal.dialog"
  Scenario: Suggest a random meal 7
    Given an English speaking user
      When the user says "what's for dinner?"
      Then "meal-plan-skill" should reply with dialog from "plan.meal.dialog"
