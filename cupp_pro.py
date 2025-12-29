#!/usr/bin/env python3
"""
CUPP-PRO (Markov Edition)

Ethical password wordlist generator inspired by CUPP.
Generates weak to strong human-realistic passwords
and orders them using a Markov probability model.

NO cracking. NO attacks. NO exploitation.
"""

import itertools
import os
from datetime import datetime
from markov import MarkovScorer

# ================= GLOBAL DATA =================

YEAR = datetime.now().year
RECENT_YEARS = [str(y) for y in range(YEAR - 5, YEAR + 1)]

SYMBOLS = ["!", "@", "#"]
RELATIONS = ["love", "wife", "husband", "son", "daughter"]
SEASONS = ["Spring", "Summer", "Fall", "Winter"]

SAAS = ["Microsoft", "Google", "Teams", "Zoom", "Slack", "ChatGPT"]

COMMON_WEAK = [
    "password", "welcome", "admin",
    "user", "login", "test", "guest"
]

KEYBOARD = [
    "123456", "12345", "12345678",
    "qwerty", "qwerty123", "111111"
]

# ================= HELPERS =================

def ask(prompt):
    return [x.strip() for x in input(prompt).split(",") if x.strip()]

def cases(word):
    return {word.lower(), word.capitalize(), word.upper()}

def birth_parts(date):
    parts = set()
    if len(date) >= 4:
        parts.add(date[:4])      # 1995
        parts.add(date[2:4])     # 95
    if len(date) == 8:
        yyyy, mm, dd = date[:4], date[4:6], date[6:]
        parts.update([mm + dd, dd + mm, mm, dd])
    return parts

# ================= INPUT =================

def collect_profile():
    print("\n=== CUPP-PRO (Markov Edition) ===\n")
    words = []
    words += ask("Names / usernames: ")
    words += ask("Related names (family, partner): ")
    words += ask("Company / organization: ")
    words += ask("City / country: ")
    dates = ask("Birthdate(s) (YYYY or YYYYMMDD): ")
    return list(set(words)), dates

# ================= WEAK PASSWORDS =================

def weak_passwords(words):
    weak = set()

    for w in words:
        weak.add(w.lower())
        weak.add(w + "1")
        weak.add(w + "123")
        weak.add(w.lower() + "123")
        weak.add(w.lower() + "@123")

    for c in COMMON_WEAK:
        weak.add(c)
        weak.add(c + "1")
        weak.add(c + "123")
        weak.add(c + "@123")

    weak.update(KEYBOARD)
    return weak

# ================= GENERATION =================

def generate(words, dates):
    generated = set()

    # Weak layer
    generated.update(weak_passwords(words))

    # Name-based logic
    for w in words:
        for c in cases(w):
            generated.add(c)

        for y in RECENT_YEARS:
            for s in SYMBOLS:
                generated.add(f"{w}{y}{s}")

        for app in SAAS:
            generated.add(f"{w}@{app}")

        for r in RELATIONS:
            generated.add(f"{w}{r}!")

    # Name + name
    for a, b in itertools.permutations(words, 2):
        generated.add(a + b)
        generated.add(a + "_" + b)
        generated.add(a + "@" + b)

    # Date logic
    for d in dates:
        for p in birth_parts(d):
            for w in words:
                generated.add(f"{w}{p}")
                generated.add(f"{w}@{p}")

    # Seasonal
    for s in SEASONS:
        for y in RECENT_YEARS:
            generated.add(f"{s}{y}!")

    return list(generated)

# ================= MAIN =================

def main():
    os.makedirs("output", exist_ok=True)

    words, dates = collect_profile()
    passwords = generate(words, dates)

    scorer = MarkovScorer()
    scorer.train(passwords[:1000])

    ordered = sorted(
        set(passwords),
        key=lambda p: scorer.score(p),
        reverse=True
    )

    out_file = "output/final_wordlist.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        for pwd in ordered:
            f.write(pwd + "\n")

    print("\n[✓] Wordlist generated")
    print(f"[✓] Output file: {out_file}")
    print(f"[✓] Total passwords: {len(ordered)}")

if __name__ == "__main__":
    main()
