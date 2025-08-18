import os, sys, time, base64
from pathlib import Path
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Project root = parent of src/
ROOT_DIR = Path(__file__).resolve().parent.parent
# Store OAuth files at project root so you never commit them in src/
CREDENTIALS_PATH = ROOT_DIR / "credentials.json"
TOKEN_PATH = ROOT_DIR / "token.json"


def auth_service():
    """Return an authenticated Gmail API service (stores token at project root)."""
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                sys.exit(f"Missing credentials.json at: {CREDENTIALS_PATH}")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds)


def load_emails(path: Path):
    """Load one email per line; ignore blanks and comments."""
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        sys.exit(f"Recipients file not found: {path}")
    emails = []
    for ln in raw.splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if "@" in s:
            emails.append(s)
    if not emails:
        sys.exit(f"No valid emails found in {path}")
    return emails


def make_msg(
    to: str,
    subject: str,
    body_text: str,
    *,
    from_name: Optional[str] = None,
    body_html: Optional[str] = None,
):
    """Build a message. If body_html is provided, send multipart/alternative."""
    subject = (subject or "").strip()
    if not subject:
        sys.exit("Subject must be a non-empty string")

    if body_html is not None:
        text_part = MIMEText(body_text or "", "plain", "utf-8")
        html_part = MIMEText(body_html, "html", "utf-8")
        msg = MIMEMultipart("alternative")
        msg.attach(text_part)
        msg.attach(html_part)
    else:
        body_text = (body_text or "").rstrip()
        if not body_text:
            sys.exit("Body must be a non-empty string")
        msg = MIMEText(body_text, "plain", "utf-8")

    msg["To"] = to
    msg["Subject"] = str(Header(subject, "utf-8"))
    if from_name:
        msg["From"] = str(Header(from_name, "utf-8"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw}


def send(service, to: str, subject: str, body_text: str, *,
         from_name: Optional[str] = None, body_html: Optional[str] = None):
    message = make_msg(to, subject, body_text, from_name=from_name, body_html=body_html)
    return service.users().messages().send(userId="me", body=message).execute()


def run_batch(
    *,
    recipients_path: Path,
    subject: str,
    body: str,
    html: bool,
    from_name: Optional[str],
    sleep: float,
    dry: bool,
):
    recipients = load_emails(recipients_path)
    service = auth_service()

    body_text = body or ""
    body_html = body if html else None

    total = len(recipients)
    for i, r in enumerate(recipients, 1):
        try:
            if dry:
                print(f"[{i}/{total}] (dry) would send to {r}")
            else:
                send(service, r, subject, body_text, from_name=from_name, body_html=body_html)
                print(f"[{i}/{total}] sent to {r}")
        except HttpError as e:
            print(f"[{i}/{total}] failed {r}: {e}", file=sys.stderr)
        time.sleep(max(0.0, float(sleep)))
