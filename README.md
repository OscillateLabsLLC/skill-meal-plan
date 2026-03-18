# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/utensils.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Meal Plan

[![Status: Active](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/OscillateLabsLLC/.github/blob/main/SUPPORT_STATUS.md)

Suggests a meal for you to make

## Upgrading to 2.0

Version 2.0 changes the skill entry point from `skill-meal-plan.mikejgray` to `skill-meal-plan.oscillatelabsllc`. This means your saved settings (meal list) will not carry over automatically.

To migrate your settings, copy your settings file:

```bash
# Mycroft/OVOS
cp ~/.config/mycroft/skills/skill-meal-plan.mikejgray/settings.json \
   ~/.config/mycroft/skills/skill-meal-plan.oscillatelabsllc/settings.json

# Neon
cp ~/.config/neon/skills/skill-meal-plan.mikejgray/settings.json \
   ~/.config/neon/skills/skill-meal-plan.oscillatelabsllc/settings.json
```

## About

Suggests a meal for you to make, based on a short default list, but you can manage your own meals!

## Examples

- "What should I make for dinner?"
- "What should I eat?"
- "What should I eat tonight?"
- "I'm hungry"
- "What's for dinner?"

## Credits

Oscillate Labs

## Category

**Daily**
Productivity

## Tags

Food meal planning
Food
Meal
Planning
Meal planning
