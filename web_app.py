from flask import Flask, render_template_string, request

from app import create_fallback_plan, generate_plan, validate_profile

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Open Meal Buddy</title>
    <style>
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f5f7f4;
        color: #1d2a1f;
      }
      .wrap {
        max-width: 820px;
        margin: 40px auto;
        padding: 24px;
      }
      .card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 12px 35px rgba(29,42,31,0.08);
      }
      h1 {
        margin-top: 0;
        color: #224b2e;
      }
      form {
        display: grid;
        gap: 14px;
      }
      .row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 14px;
      }
      label {
        display: block;
        font-weight: 600;
        margin-bottom: 6px;
      }
      input, textarea {
        width: 100%;
        box-sizing: border-box;
        padding: 10px 12px;
        border-radius: 10px;
        border: 1px solid #cfe0d0;
        font-size: 1rem;
      }
      textarea {
        min-height: 80px;
        resize: vertical;
      }
      button {
        background: #2d7a4f;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 18px;
        font-weight: 700;
        cursor: pointer;
      }
      .result {
        margin-top: 24px;
        white-space: pre-wrap;
        background: #f2f8f4;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #dfeee2;
        line-height: 1.6;
      }
      .tag {
        display: inline-block;
        background: #eaf6ee;
        color: #234d35;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.84rem;
        font-weight: 700;
        margin-bottom: 12px;
      }
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="card">
        <div class="tag">Open Meal Buddy</div>
        <h1>Meal plans for people you care about</h1>
        <form method="post">
          <div class="row">
            <div>
              <label>Name</label>
              <input name="name" value="{{ values.get('name', '') }}" placeholder="Ava" />
            </div>
            <div>
              <label>Days</label>
              <input name="days" type="number" min="1" max="7" value="{{ values.get('days', 3) }}" />
            </div>
          </div>
          <div class="row">
            <div>
              <label>Budget (USD)</label>
              <input name="budget" value="{{ values.get('budget', '40') }}" placeholder="40" />
            </div>
            <div>
              <label>Allergies</label>
              <input name="allergies" value="{{ values.get('allergies', '') }}" placeholder="peanuts, dairy" />
            </div>
          </div>
          <div>
            <label>Pantry</label>
            <textarea name="pantry" placeholder="rice, eggs, spinach, chickpeas, onion">{{ values.get('pantry', '') }}</textarea>
          </div>
          <div>
            <label>Preferences</label>
            <textarea name="likes" placeholder="vegetarian, quick meals">{{ values.get('likes', '') }}</textarea>
          </div>
          <div>
            <label>Schedule notes</label>
            <textarea name="schedule" placeholder="busy weekday dinners">{{ values.get('schedule', '') }}</textarea>
          </div>
          <button type="submit">Generate plan</button>
        </form>

        {% if result %}
        <div class="result">{{ result }}</div>
        {% endif %}
      </div>
    </div>
  </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    values = {}
    result = ""

    if request.method == "POST":
        values = {
            "name": request.form.get("name", "Friend"),
            "days": request.form.get("days", "3"),
            "budget": request.form.get("budget", "40"),
            "allergies": request.form.get("allergies", ""),
            "pantry": request.form.get("pantry", ""),
            "likes": request.form.get("likes", ""),
            "schedule": request.form.get("schedule", ""),
        }

        profile = {
            "name": values["name"],
            "days": values["days"],
            "budget": values["budget"],
            "allergies": values["allergies"],
            "pantry": values["pantry"],
            "likes": values["likes"],
            "schedule": values["schedule"],
        }

        try:
            validated = validate_profile(profile)
            result = generate_plan(validated)
        except ValueError as exc:
            result = f"Invalid input: {exc}"
        except RuntimeError:
            result = create_fallback_plan(profile)

    return render_template_string(HTML_TEMPLATE, values=values, result=result)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
