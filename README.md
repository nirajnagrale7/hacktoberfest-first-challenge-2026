# Open Meal Buddy

Open Meal Buddy is a local, friend-first meal planner powered by an open-source model from Ollama. It is built for a real-life use case: helping someone you care about eat well without stressing about allergies, budget, or the chaos of a busy week.

## Why this matters

This project is built around open innovation because it keeps the work on a laptop instead of sending personal data to a third-party API. The model can run locally, the prompts are transparent, and the tool can be changed or fine-tuned without paying for a closed service.

For a friend or loved one, that means:

- no personal dietary details go to a remote server
- no internet access is required once the model is installed
- the planner can be customized to allergies, budget, and pantry items
- it is free to run and easy to adapt for other family or health use cases

## What it does

The app creates a simple family-friendly meal plan from:

- the person's name
- allergies or food exclusions
- a weekly budget
- pantry ingredients already on hand
- preferences such as vegetarian, quick meals, or favorites
- schedule constraints

It returns:

- a short weekly summary
- a day-by-day meal plan
- a grocery list
- prep tips
- substitution ideas for variety

## How to run it

### Option 1: Local CLI

1. Install Ollama: https://ollama.com/download
2. Pull a local model:

   ```bash
   ollama pull llama3.2:3b
   ```

3. Start Ollama and verify the server is running on localhost:11434.
4. Run the planner:

   ```bash
   python app.py --name "Ava" --allergies "peanuts,dairy" --budget "40" --days 3 --pantry "rice, eggs, spinach, chickpeas, onion" --likes "vegetarian, quick meals" --schedule "busy weekday dinners"
   ```

### Option 2: Quick browser demo

```bash
pip install flask
python web_app.py
```

Then open http://localhost:5000 and fill in the form.

If you want a quick demo without the model, the app prints a fallback sample plan when the local model is unavailable.

## Hacktoberfest challenge fit

This project fits the weekend challenge because it solves a real problem for someone you love: a friend or roommate trying to eat well without triggering allergies or blowing the grocery budget.

The open-source AI is the core of the product because the app relies on a local model that runs on a laptop and keeps food preferences private.

## Example submission text

```md
## What I Built
I built Open Meal Buddy, a local meal-planning assistant for my roommate.

It helps plan affordable, allergy-safe meals from ingredients already at home, without sending private food preferences to a remote server.

## Demo
Run it locally with Ollama and a small open-weight model.

## Code
https://github.com/your-name/open-meal-buddy

## How I Built It
I used Ollama with the open-weight llama3.2:3b model and a lightweight Python app that builds a meal plan from allergies, pantry items, preferences, and schedule constraints.

## Why Does Open Innovation Matter?
This project works better with open AI because it can run entirely on a laptop. That keeps personal dietary data local, avoids API costs, and makes it easy to swap or fine-tune the model later.
```

## Project status

This is a small, practical prototype designed for the Hacktoberfest weekend challenge and for real use with a friend or family member.
