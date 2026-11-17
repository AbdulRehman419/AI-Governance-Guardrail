import datetime
import re
from profanityfilter.profanityfilter import ProfanityFilter

# 1. Initialize cloned library (automatically loads data/badwords.txt)
pf = ProfanityFilter()
pf.append_words(["idiot", "stupid", "hate", "racist", "scam", "violence"])

# 2. Improvisation A: PII Detection (Data Privacy check)
def check_pii(text):
    email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|@[a-zA-Z0-9-]+\.[a-zA-Z]+)'
    phone_pattern = r'\b\d{10,11}\b'

    detected = []
    if re.search(email_pattern, text):
        detected.append("PII: Email / Handle Leak")
    if re.search(phone_pattern, text):
        detected.append("PII: Phone Number Leak")
    return detected

# 3. Improvisation B: Compliance Audit Logging
def log_audit(text, status, violations):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reasons = "; ".join(violations) if violations else "None"
    with open("audit_log.csv", "a", encoding="utf-8") as f:
        f.write(f'"{timestamp}","{text}","{status}","{reasons}"\n')

# 4. Governance Evaluation Pipeline
def evaluate_ai_response(text):
    violations = []

    # Uses the cloned repository's core profanity detection method
    if pf.is_profane(text):
        violations.append("Toxicity / Prohibited Language")

    # Uses our improvised PII governance check
    pii_violations = check_pii(text)
    if pii_violations:
        violations.extend(pii_violations)

    if violations:
        print("\n[AI GOVERNANCE ALERT] Blocked!")
        for v in violations:
            print(f" - {v}")
        log_audit(text, "BLOCKED", violations)
    else:
        print("\n[AI GOVERNANCE CHECK] Passed: Safe to display.")
        log_audit(text, "PASSED", [])

def main():
    try:
        with open("audit_log.csv", "x", encoding="utf-8") as f:
            f.write("Timestamp,Evaluated Text,Status,Violations\n")
    except FileExistsError:
        pass

    print("=" * 45)
    print("      AI GOVERNANCE GUARDRAIL SYSTEM         ")
    print("=" * 45)

    while True:
        user_input = input("\nEnter AI text to audit (or 'exit'): ")
        if user_input.strip().lower() == "exit":
            print("Guardrail system terminated.")
            break
        evaluate_ai_response(user_input)

if __name__ == "__main__":
    main()