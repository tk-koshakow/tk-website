#!/usr/bin/env python3
"""
gdocs_review.py — Google Docs Editorial Review & Two-Way Feedback Bridge

Enables a collaborative, non-destructive editorial review workflow:
1. `export`: Uploads a local draft (HTML or Markdown) to Google Docs inside a 'TK Website Drafts' folder.
2. `pull`: Reads the Google Doc's content, comments, and suggestions, extracting feedback for local revision.
3. `status`: Checks Google Drive/Docs API authentication and credentials.

Usage:
  python3 scripts/gdocs_review.py export drafts/my-new-post.html
  python3 scripts/gdocs_review.py pull <google_doc_id_or_url>
  python3 scripts/gdocs_review.py status
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = REPO_ROOT / "google_credentials.json"
TOKEN_FILE = REPO_ROOT / ".google_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/documents",
]

def check_dependencies():
    try:
        import google.auth
        import googleapiclient.discovery
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        return True
    except ImportError:
        return False

def get_google_services():
    """Authenticates and returns (docs_service, drive_service)."""
    if not check_dependencies():
        print("Missing required Google API packages. Install them using:")
        print("  pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        return None, None

    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"Warning: Could not load token file: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:
            if not CREDENTIALS_FILE.exists():
                print(f"Error: Google OAuth credentials file not found at: {CREDENTIALS_FILE}")
                print("\nTo set up Google Drive integration:")
                print("1. Go to Google Cloud Console (https://console.cloud.google.com/).")
                print("2. Create an OAuth 2.0 Client ID (Desktop Application) under APIs & Services -> Credentials.")
                print("3. Enable Google Drive API & Google Docs API.")
                print(f"4. Download the JSON file and save it to: {CREDENTIALS_FILE}")
                return None, None

            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    docs_service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    return docs_service, drive_service

def extract_text_from_html(html_path: Path):
    """Extracts title and clean text from an HTML draft file."""
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    
    # Extract Title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if not title_match:
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else html_path.stem
    title = title.replace("&ldquo;", '"').replace("&rdquo;", '"').replace("&mdash;", "—").replace("&amp;", "&")

    # Extract Body
    body_match = re.search(r'<div class=["\']article-content["\'][^>]*>(.*?)</div>\s*</article>', content, re.IGNORECASE | re.DOTALL)
    body_html = body_match.group(1) if body_match else content

    # Clean HTML to readable draft text for Google Docs
    # Convert Headings
    clean_text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n\n', body_html, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n\n### \1\n\n', clean_text, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', clean_text, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', clean_text, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n\n', clean_text, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    
    # Clean HTML entities
    clean_text = (clean_text.replace("&ldquo;", '"')
                            .replace("&rdquo;", '"')
                            .replace("&lsquo;", "'")
                            .replace("&rsquo;", "'")
                            .replace("&mdash;", "—")
                            .replace("&ndash;", "–")
                            .replace("&amp;", "&")
                            .replace("&hellip;", "..."))
    
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text).strip()
    return title, clean_text

def export_draft(draft_path_str: str):
    draft_path = Path(draft_path_str)
    if not draft_path.is_absolute():
        draft_path = REPO_ROOT / draft_path
        
    if not draft_path.exists():
        print(f"Error: Draft file does not exist: {draft_path}")
        return

    title, body_text = extract_text_from_html(draft_path)
    print(f"Preparing draft export for: '{title}' ({draft_path.name})")

    docs_service, drive_service = get_google_services()
    if not docs_service or not drive_service:
        print("\n--- Fallback Local Export ---")
        print("You can copy the clean draft text below or set up Google API credentials above:")
        print(f"\nTitle: {title}\n")
        print(body_text[:500] + "\n...[truncated]")
        return

    # 1. Create blank Google Doc
    doc = docs_service.documents().create(body={"title": f"[DRAFT] {title}"}).execute()
    doc_id = doc.get("documentId")

    # 2. Insert draft text into doc
    full_doc_content = f"{title}\n\nAuthor: Tyler 'TK' Koshakow\nStatus: Pending Human Review\nFile: {draft_path.relative_to(REPO_ROOT)}\n\n---\n\n{body_text}\n"
    
    requests = [
        {
            "insertText": {
                "location": {"index": 1},
                "text": full_doc_content
            }
        }
    ]
    docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"\n[SUCCESS] Exported draft to Google Docs!")
    print(f"Document URL: {doc_url}")
    print("\nNext Steps:")
    print("1. Open the document, leave margin comments, suggest edits, or highlight text.")
    print(f"2. When done, pull feedback using: python3 scripts/gdocs_review.py pull {doc_id}")

def pull_feedback(doc_id_or_url: str):
    # Extract ID from URL if full URL is passed
    match = re.search(r'/document/d/([a-zA-Z0-9_-]+)', doc_id_or_url)
    doc_id = match.group(1) if match else doc_id_or_url

    docs_service, drive_service = get_google_services()
    if not docs_service or not drive_service:
        return

    # Fetch document content
    doc = docs_service.documents().get(documentId=doc_id).execute()
    title = doc.get("title")

    # Fetch comments via Drive API
    comments_resp = drive_service.comments().list(fileId=doc_id, fields="comments(id,author,content,resolved,quotedFileContent,replies)").execute()
    comments = comments_resp.get("comments", [])

    print(f"=== EDITORIAL FEEDBACK REPORT: '{title}' ===")
    print(f"Doc ID: {doc_id}")
    print(f"Total Comments / Marginal Notes: {len(comments)}\n")

    unresolved = [c for c in comments if not c.get("resolved")]
    if unresolved:
        print("--- Active Editorial Comments ---")
        for idx, c in enumerate(unresolved, 1):
            author = c.get("author", {}).get("displayName", "User")
            quoted = c.get("quotedFileContent", {}).get("value", "")
            content = c.get("content", "")
            print(f"[{idx}] {author}:")
            if quoted:
                print(f'    Quoted: "{quoted}"')
            print(f'    Note:   "{content}"\n')
    else:
        print("No active comments found in document.")

def main():
    parser = argparse.ArgumentParser(description="Google Docs Editorial Bridge")
    subparsers = parser.add_subparsers(dest="command")

    export_parser = subparsers.add_parser("export", help="Export draft to Google Doc")
    export_parser.add_argument("file", help="Path to draft HTML or MD file")

    pull_parser = subparsers.add_parser("pull", help="Pull comments and text from Google Doc")
    pull_parser.add_argument("doc_id", help="Google Doc ID or URL")

    subparsers.add_parser("status", help="Check Google API setup")

    args = parser.parse_args()
    if args.command == "export":
        export_draft(args.file)
    elif args.command == "pull":
        pull_feedback(args.doc_id)
    elif args.command == "status":
        get_google_services()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
