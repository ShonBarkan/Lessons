import os
from datetime import datetime
import google.generativeai as genai

# Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

today = datetime.now().strftime("%Y-%m-%d")
filename = f"daily_mantra_{today}.txt"

prompt = "Generate a short, uplifting, positive mantra to start the day with a good mindset."
response = model.generate_content(prompt)
mantra = response.text.strip()

# Save mantra to file
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"🌞 Daily Mantra for {today}\n\n{mantra}")

print(f"Saved mantra to {filename}")
