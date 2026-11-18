# AI IT Helpdesk Triage System

An automated IT support triage tool that classifies incoming support tickets, generates professional email responses using the Claude AI API, and sends them via Gmail — with human approval at every step.

## Features

- **Keyword-based ticket classification** — matches tickets to categories (password reset, printer, new starter, video conferencing, network)
- **AI-generated responses** — Claude (Haiku) writes personalised, professional email replies based on the ticket content and knowledge base solution
- **Human-in-the-loop** — IT engineer reviews and approves every response before it is sent
- **Gmail integration** — approved responses are sent directly via Gmail API
- **CSV audit log** — every ticket is logged with timestamp, category, approval status, and whether email was sent

## Tech Stack

- Python 3
- [Anthropic Claude API](https://www.anthropic.com/) — `claude-haiku-4-5` model
- Gmail API (OAuth 2.0)
- `python-dotenv` for secure API key management

## Project Structure

```
it-helpdesk-triage/
├── classifier.py        # Main program — classify, generate, approve, send
├── gmail_sender.py      # Gmail API authentication and email sending
├── knowledge_base.json  # IT solutions database
├── sample_tickets.txt   # Example support tickets for testing
├── .env                 # API key (not committed)
├── credentials.json     # Google OAuth credentials (not committed)
└── token.json           # Google auth token (not committed)
```

## Setup

1. Clone the repo
2. Install dependencies:

pip3 install anthropic python-dotenv google-auth-oauthlib google-auth-httplib2 google-api-python-client

3. Create `.env` file with your Anthropic API key:

ANTHROPIC_API_KEY=your-key-here

4. Add `credentials.json` from Google Cloud Console (Gmail API, OAuth Desktop app)
5. Run:

python3 classifier.py

On first run, a browser window will open to authorise Gmail access.

## How It Works

1. Tickets are loaded from `sample_tickets.txt`
2. Each ticket is classified by keyword matching against `knowledge_base.json`
3. Claude generates a professional email response using the ticket text and suggested solution
4. The IT engineer reviews the draft and approves or rejects it
5. If approved, the email is sent via Gmail API and the result is logged to `ticket_log.csv`

## Author

Damian Ciasnocha — IT Technician | Jamf Pro | Python automation