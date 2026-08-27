#!/usr/bin/env python3
"""
TK Website — Automated AEO/GEO Content Intelligence Email Dispatcher
Reads the latest pitch briefing markdown file and sends a formatted email via SMTP.
"""

import os
import sys
import glob
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_env():
    env_file = BASE_DIR / ".env"
    env_vars = {}
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip("'\"")
    return env_vars

def markdown_to_html(md_text):
    """
    Lightweight markdown-to-HTML converter with inline email styles.
    """
    html_lines = []
    in_code_block = False
    code_content = []
    
    lines = md_text.splitlines()
    for line in lines:
        # Code block handling
        if line.startswith("```"):
            if in_code_block:
                in_code_block = False
                escaped_code = "\n".join(code_content).replace("<", "&lt;").replace(">", "&gt;")
                html_lines.append(f'<div style="background-color: #f6f6f6; border-left: 3px solid #111111; padding: 14px; margin: 14px 0; font-family: ui-monospace, Menlo, Monaco, Consolas, monospace; font-size: 13px; line-height: 1.5; white-space: pre-wrap; color: #222222;">{escaped_code}</div>')
                code_content = []
            else:
                in_code_block = True
                code_content = []
            continue
        
        if in_code_block:
            code_content.append(line)
            continue
        
        # Blank line
        if not line.strip():
            html_lines.append('<div style="height: 10px;"></div>')
            continue
        
        # Headings
        if line.startswith("# "):
            title = line[2:].strip()
            html_lines.append(f'<h1 style="font-size: 24px; font-weight: 700; color: #111111; margin: 20px 0 10px 0; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; letter-spacing: -0.02em;">{title}</h1>')
            continue
        elif line.startswith("## "):
            h2 = line[3:].strip()
            html_lines.append(f'<h2 style="font-size: 19px; font-weight: 700; color: #111111; margin: 26px 0 8px 0; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; border-bottom: 1px solid #eaeaea; padding-bottom: 6px;">{h2}</h2>')
            continue
        elif line.startswith("### "):
            h3 = line[4:].strip()
            html_lines.append(f'<h3 style="font-size: 16px; font-weight: 600; color: #222222; margin: 18px 0 6px 0; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">{h3}</h3>')
            continue
        elif line.startswith("#### "):
            h4 = line[5:].strip()
            html_lines.append(f'<h4 style="font-size: 14px; font-weight: 600; color: #444444; margin: 14px 0 4px 0; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">{h4}</h4>')
            continue
        
        # Horizontal Rule
        if line.strip() in ("---", "***", "___"):
            html_lines.append('<hr style="border: none; border-top: 1px solid #eaeaea; margin: 24px 0;" />')
            continue
        
        # Blockquotes
        if line.startswith("> "):
            quote = line[2:].strip()
            # Inline formatting
            quote = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', quote)
            html_lines.append(f'<blockquote style="border-left: 3px solid #111111; padding-left: 12px; margin: 12px 0; color: #444444; font-style: italic; font-size: 14px; line-height: 1.6;">{quote}</blockquote>')
            continue
        
        # Unordered list items
        if line.startswith("- ") or line.startswith("* "):
            item = line[2:].strip()
            item = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" style="color: #111111; text-decoration: underline;">\1</a>', item)
            item = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item)
            html_lines.append(f'<li style="margin-bottom: 6px; color: #333333; font-size: 14px; line-height: 1.6;">{item}</li>')
            continue
        
        # Standard paragraph line
        para = line
        para = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" style="color: #111111; text-decoration: underline;">\1</a>', para)
        para = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', para)
        html_lines.append(f'<p style="margin: 0 0 10px 0; color: #333333; font-size: 14px; line-height: 1.6;">{para}</p>')
    
    body_content = "\n".join(html_lines)
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AEO & GEO Content Intelligence Briefing</title>
</head>
<body style="margin: 0; padding: 24px; background-color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #111111;">
  <div style="max-width: 620px; margin: 0 auto; background-color: #ffffff; padding: 10px 0;">
    <div style="font-family: ui-monospace, Menlo, Monaco, Consolas, monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #888888; margin-bottom: 12px;">
      TK Website // Intelligence Dispatch
    </div>
    {body_content}
    <div style="margin-top: 36px; padding-top: 16px; border-top: 1px solid #eaeaea; font-family: ui-monospace, Menlo, Monaco, Consolas, monospace; font-size: 11px; color: #888888;">
      Tyler "TK" Koshakow &bull; AEO, GEO, Enterprise Search Strategy &bull; koshakow@gmail.com
    </div>
  </div>
</body>
</html>"""
    return full_html

def send_email(subject, md_content):
    env = load_env()
    
    smtp_host = env.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(env.get("SMTP_PORT", "465"))
    smtp_user = env.get("SMTP_USER", "")
    smtp_pass = env.get("SMTP_PASS", "")
    recipient = env.get("RECIPIENT_EMAIL", smtp_user)
    
    if not smtp_user or not smtp_pass:
        print("Error: SMTP_USER or SMTP_PASS not set in .env", file=sys.stderr)
        sys.exit(1)
        
    html_content = markdown_to_html(md_content)
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f'Tyler "TK" Koshakow <{smtp_user}>'
    msg["To"] = recipient
    
    part1 = MIMEText(md_content, "plain", "utf-8")
    part2 = MIMEText(html_content, "html", "utf-8")
    
    msg.attach(part1)
    msg.attach(part2)
    
    print(f"Connecting to {smtp_host}:{smtp_port}...")
    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [recipient], msg.as_string())
    else:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [recipient], msg.as_string())
            
    print(f"Email successfully sent to {recipient}!")

def main():
    if len(sys.argv) > 1:
        target_file = Path(sys.argv[1])
    else:
        # Pick the latest briefing file in pitches/
        pitches_dir = BASE_DIR / "pitches"
        files = sorted(pitches_dir.glob("*.md"), key=os.path.getmtime, reverse=True)
        if not files:
            print("No pitch files found in pitches/ directory.", file=sys.stderr)
            sys.exit(1)
        target_file = files[0]
        
    print(f"Reading briefing file: {target_file}")
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract date for subject line
    date_match = re.search(r'\*\*Date:\*\*\s*(.+)', content)
    date_str = date_match.group(1).strip() if date_match else "Latest"
    subject = f"AEO & GEO Content Intelligence Briefing — {date_str}"
    
    send_email(subject, content)

if __name__ == "__main__":
    main()
