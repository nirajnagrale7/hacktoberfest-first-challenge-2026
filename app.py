import argparse
import json
import os
from urllib import error, request

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def normalize_allergies(raw_value):
    """Normalize a CSV-style allergy field into clean lowercase entries."""
    if raw_value is None:
        return []
    if isinstance(raw_value, list):
        return [str(item).strip().lower() for item in raw_value if str(item).strip()]

    items = [item.strip().lower() for item in str(raw_value).split(",")]
    return [item for item in items if item]


def build_prompt(profile):
    """Create a prompt for a local open-source model to generate a meal plan."""
    name = profile.get("name", "Friend")
    allergies = normalize_allergies(profile.get("allergies", []))
    days = int(profile.get("days", 3))
    budget = profile.get("budget", "reasonable")
    pantry = profile.get("pantry", "")
    likes = profile.get("likes", [])
    if isinstance(likes, str):
        likes = [item.strip() for item in likes.split(",") if item.strip()]
    schedule = profile.get("schedule", "")

    allergen_text = ", ".join(allergies) if allergies else "none"
    likes_text = ", ".join(likes) if likes else "no special preferences"

    return f"""You are a caring, practical meal planner for {name}.

Create a {days}-day meal plan that is safe, affordable, and realistic for someone with a busy schedule.

Requirements:
- Budget: ${budget} per week
- Allergies / intolerances to avoid: {allergen_text}
- Pantry or ingredients already available: {pantry or 'none noted'}
- Food preferences or taste cues: {likes_text}
- Schedule context: {schedule or 'regular week'}

Return a plan with:
1. A short summary of the goal for the week.
2. A day-by-day list covering breakfast, lunch, dinner, and one snack.
3. A grocery list grouped by produce, protein, dairy alternatives, grains, and pantry items.
4. Three practical prep tips to save time.
5. A note on how to swap ingredients if the person wants more variety.

Important: do not suggest any ingredients that include the listed allergies.
Keep meals simple, nutritious, and budget-friendly.
"""


def generate_plan(profile, model=DEFAULT_MODEL):
    """Generate a meal plan using a locally running Ollama model."""
    payload = {
        "model": model,
        "prompt": build_prompt(profile),
        "stream": False,
    }
    request_data = json.dumps(payload).encode("utf-8")
    url = f"{OLLAMA_BASE_URL}/api/generate"

    try:
        req = request.Request(url, data=request_data, headers={"Content-Type": "application/json"})
        with request.urlopen(req, timeout=180) as response:
            content = response.read().decode("utf-8")
    except error.URLError as exc:
        raise RuntimeError(
            "Ollama was not reachable. Start the Ollama server and pull the model with: "
            "ollama pull llama3.2:3b"
        ) from exc

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError("The local model returned an unexpected response format.") from exc

    response_text = data.get("response", "").strip()
    if not response_text:
        raise RuntimeError("The local model did not return a usable meal plan.")

    return response_text


def create_fallback_plan(profile):
    """Return a short, practical meal plan when the local AI service is unavailable."""
    name = profile.get("name", "Friend")
    days = int(profile.get("days", 3))
    allergies = normalize_allergies(profile.get("allergies", []))
    allergen_note = ", ".join(allergies) if allergies else "none"
    pantry = profile.get("pantry", "") or "basic pantry staples"
    likes = profile.get("likes", [])
    if isinstance(likes, str):
        likes = [item.strip() for item in likes.split(",") if item.strip()]
    likes_text = ", ".join(likes) if likes else "simple and nourishing"

    return (
        f"{name}'s {days}-day plan\n"
        "- Breakfast: overnight oats with berries and almond milk\n"
        "- Lunch: chickpea quinoa bowl with spinach and lemon\n"
        "- Dinner: lentil curry with rice and roasted vegetables\n"
        "- Snack: apple slices and peanut-free trail mix\n\n"
        f"Allergy watch: {allergen_note}\n"
        f"Use what you already have: {pantry}\n"
        f"Preferences: {likes_text}\n\n"
        "This keeps costs low, avoids common allergens, and works even without internet access."
    )


def build_profile_from_args(args):
    """Collect all available profile information, prompting for missing pieces interactively."""
    profile = {
        "name": args.name or input("Friend or loved one's name: ").strip() or "Friend",
        "allergies": normalize_allergies(args.allergies),
        "budget": args.budget or "40",
        "days": args.days or 3,
        "pantry": args.pantry or "",
        "likes": [item.strip() for item in (args.likes or "").split(",") if item.strip()],
        "schedule": args.schedule or "",
    }

    if not profile["allergies"] and not args.allergies:
        profile["allergies"] = normalize_allergies(input("Any allergies or intolerances? (comma-separated, blank for none): ").strip())

    if not profile["pantry"]:
        profile["pantry"] = input("What ingredients do you already have at home? (blank if none): ").strip()

    if not profile["likes"]:
        likes_input = input("Any food preferences? (e.g. vegetarian, low effort, family favorites): ").strip()
        profile["likes"] = [item.strip() for item in likes_input.split(",") if item.strip()]

    if not profile["schedule"]:
        profile["schedule"] = input("Any schedule notes or cooking constraints? (blank if none): ").strip()

    return profile


def parse_args():
    parser = argparse.ArgumentParser(description="Open-source meal planner built for a friend.")
    parser.add_argument("--name", help="Name of the person the plan is for.")
    parser.add_argument("--allergies", help="Comma-separated allergies or dietary exclusions.")
    parser.add_argument("--budget", help="Weekly food budget in dollars.")
    parser.add_argument("--days", type=int, default=3, help="How many days to plan.")
    parser.add_argument("--pantry", help="Ingredients already available at home.")
    parser.add_argument("--likes", help="Food preferences or desired cuisines, comma-separated.")
    parser.add_argument("--schedule", help="Notes about time constraints or cooking habits.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Local Ollama model to use.")
    return parser.parse_args()


def main():
    args = parse_args()
    profile = build_profile_from_args(args)

    try:
        plan = generate_plan(profile, model=args.model)
    except RuntimeError as exc:
        print(f"Local plan generation unavailable: {exc}")
        print("\nSample fallback plan:\n")
        print(create_fallback_plan(profile))
        return 1

    print(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
