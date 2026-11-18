import json
import os
import anthropic
from dotenv import load_dotenv
from gmail_sender import send_email

# Load API key from .env file
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# =====================
# STEP 1: Load knowledge base
# =====================
with open("knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

# =====================
# STEP 2: Load sample tickets
# =====================
with open("sample_tickets.txt", "r") as f:
    raw_text = f.read()

tickets = raw_text.strip().split("---")

# =====================
# STEP 3: Classification function
# =====================
def classify_ticket(ticket_text):
    ticket_lower = ticket_text.lower()
    for category, data in knowledge_base.items():
        for keyword in data["keywords"]:
            if keyword in ticket_lower:
                return category, data["solution"]
    return "unknown", "No matching solution found. Please escalate to senior IT."

# =====================
# STEP 4: Generate AI response using Claude
# =====================
def generate_response(ticket_text, category, solution):
    prompt = f"""You are a helpful IT support engineer. 
A user has submitted the following support ticket:

{ticket_text}

The issue has been classified as: {category}
Suggested solution from knowledge base: {solution}

Write a professional, friendly email response to the user.
- Address them by name if mentioned in the ticket
- Briefly acknowledge their issue
- Provide clear step-by-step instructions
- Offer to follow up if the issue persists
- Sign off as 'IT Support Team'
Keep it concise and helpful."""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# =====================
# STEP 5: Process each ticket with human approval + Gmail send
# =====================

# Create CSV log file with headers if it doesn't exist
if not os.path.exists("ticket_log.csv"):
    with open("ticket_log.csv", "w") as log:
        log.write("timestamp,ticket_id,category,status,email_sent\n")

print("=" * 60)
print("IT HELPDESK TRIAGE SYSTEM — AI ASSISTED")
print("=" * 60)

for i, ticket in enumerate(tickets, 1):
    if ticket.strip():
        category, solution = classify_ticket(ticket)

        print(f"\n📋 TICKET {i}")
        print(f"Category: {category.upper()}")
        print(f"\nGenerating AI response...")

        response = generate_response(ticket, category, solution)

        print(f"\n--- DRAFT RESPONSE ---")
        print(response)
        print(f"----------------------")

        # Human approval step
        approval = input("\nApprove this response? (y/n): ")
        email_sent = "no"

        if approval.lower() == "y":
            to_address = input("Enter recipient email address: ")
            subject = f"Re: IT Support Ticket #{i} — {category.replace('_', ' ').title()}"
            try:
                send_email(to_address, subject, response)
                print(f"✅ Email sent to {to_address}")
                email_sent = "yes"
            except Exception as e:
                print(f"⚠️ Approved but email failed: {e}")
            status = "approved"
        else:
            print("❌ Response rejected — flagged for manual review.")
            status = "rejected"