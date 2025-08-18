# Gmail Sender Starter Pack

Send the same subject/body to a list of emails using your Gmail account (OAuth2).

## Files
- `main.py` — entry point. Edit `config.json`, then run: `python main.py`
- `gmail_sender.py` — helper module with auth + send logic
- `config.json` — where you set subject/body/recipients file/etc
- `recipients.txt` — one email per line
- `body.txt` — plain text email body (default)
- `body.html` — optional HTML body if you set `"html": true`
- `requirements.txt` — pip requirements

## Quick Start
1. Create a Google Cloud project, enable **Gmail API**, and download **OAuth Client (Desktop)** as `credentials.json` into this folder.
2. Install deps:
   ```bash
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Edit `config.json` (subject, from_name, etc.). Put your recipients in `recipients.txt`, edit `body.txt` or use `body.html` with `"html": true`.
4. Run:
   ```bash
   python main.py
   ```
5. First run opens a browser for Google login. Afterwards, `token.json` caches your credentials.

## Notes
- Each recipient gets an individual email (no CC/BCC).
- Add a small `sleep` in `config.json` to be polite and avoid burst limits.
- To switch Google accounts, delete `token.json` and run again.
