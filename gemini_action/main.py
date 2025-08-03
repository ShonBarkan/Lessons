import google.generativeai as genai
from datetime import datetime

# ==== CONFIG ====
GEMINI_API_KEY = "AIzaSyDf10DPyyUznL0KXSYb6geooZdgyhfsEZ8"

# ==== SETUP GEMINI ====
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ==== GENERATE MANTRA ====
prompt = "Generate a short, uplifting, positive mantra to start the day with a good mindset."
response = model.generate_content(prompt)
mantra = response.text.strip()

# ==== SAVE TO TEXT FILE ====
today = datetime.now().strftime("%Y-%m-%d")
filename = f"daily_mantra_{today}.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"🌞 Daily Mantra for {today}\n\n{mantra}")

print(f"✅ Mantra saved to: {filename}")
