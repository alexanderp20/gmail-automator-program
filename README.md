# Gmail Automator Software built for Amcom

Send the same subject/body to a list of emails using your Gmail account (OAuth2).

## How do I use it?
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
- To switch Google accounts, delete `token.json` and run again.
