# Gmail Automation Program

This tool sends the same subject and body to a list of recipients using your Gmail account.
Each recipient receives an individual email, rather than being included in CC or BCC.

## How do I use it?
1. Clone the repository
   ```bash
   git clone https://github.com/your-username/email-automator.git
   cd email-automator
   ```
2. Create a Google Cloud project, enable **Gmail API**, and download **OAuth Client (Desktop)** as `credentials.json` into this folder.
3. Install dependencies:
   ```bash
   python3 -m venv venv && source venv/bin/activate
   pip3 install -r requirements.txt
   ```
4. Edit `config.json` (subject, from_name, etc.). Put your recipients in `recipients.txt`, edit `body.txt` or use `body.html` with `"html": true`.
5. Run:
   ```bash
   python3 src/main.py
   ```
6. First run opens a browser for Google login. Afterwards, `token.json` caches your credentials.

## Additional Notes
- Each recipient gets an individual email (no CC/BCC).
- To switch Google accounts, delete `token.json` and run again.
