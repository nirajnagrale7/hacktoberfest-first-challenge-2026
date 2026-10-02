from app import build_prompt, create_fallback_plan, normalize_allergies


def test_normalize_allergies():
    assert normalize_allergies("Peanuts, dairy , gluten ") == ["peanuts", "dairy", "gluten"]


def test_build_prompt_includes_constraints():
    profile = {
        "name": "Ava",
        "allergies": ["peanuts", "dairy"],
        "budget": "40",
        "days": 3,
        "pantry": "rice, eggs, spinach, chickpeas, onion",
        "likes": ["vegetarian", "quick meals"],
        "schedule": "busy weekday dinners",
    }

    prompt = build_prompt(profile)

    assert "Ava" in prompt
    assert "peanuts" in prompt.lower()
    assert "dairy" in prompt.lower()
    assert "3-day" in prompt
    assert "rice" in prompt


def test_create_fallback_plan_has_useful_details():
    profile = {
        "name": "Ava",
        "allergies": ["peanuts", "dairy"],
        "budget": "40",
        "days": 3,
        "pantry": "rice, eggs, spinach",
        "likes": ["vegetarian", "quick meals"],
        "schedule": "busy weekday dinners",
    }

    plan = create_fallback_plan(profile)

    assert "Ava" in plan
    assert "peanuts" in plan.lower()
    assert "overnight oats" in plan.lower()
    assert "spinach" in plan.lower()
