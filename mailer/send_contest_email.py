"""Send contest schedule emails based on contests.json."""
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List
from datetime import datetime
import argparse

from .utils import load_contests, filter_next_24h, build_email_text


CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def send_email(smtp_cfg: dict, subject: str, body: str, to_addrs: List[str]):
    msg = MIMEMultipart()
    msg["From"] = smtp_cfg.get("from")
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    server = smtplib.SMTP(smtp_cfg["host"], smtp_cfg.get("port", 587), timeout=10)
    try:
        server.starttls()
        server.login(smtp_cfg["username"], smtp_cfg["password"])
        server.sendmail(smtp_cfg.get("from"), to_addrs, msg.as_string())
    finally:
        server.quit()


def main(contests_json_path: str = None, dry_run: bool = True):
    base = Path(__file__).parent.parent
    cj = base / "contests.json" if contests_json_path is None else Path(contests_json_path)
    data = load_contests(str(cj))
    upcoming = filter_next_24h(data.get("contests", []))
    body = build_email_text(upcoming)

    cfg = load_config()
    smtp = cfg.get("smtp")
    to_addrs = cfg.get("to", [])
    subject = cfg.get("subject", f"比赛提醒 - {datetime.now().strftime('%Y-%m-%d')}")

    if not smtp or not to_addrs:
        print("[INFO] SMTP 配置或收件人未设置，进入 dry-run 模式，打印邮件内容：\n")
        print("Subject:", subject)
        print("Body:\n", body)
        return

    if dry_run:
        print("[DRY RUN] 未实际发送，邮件将发送到:", to_addrs)
        print("Subject:", subject)
        print("Body:\n", body)
        return

    send_email(smtp, subject, body, to_addrs)
    print("邮件已发送（或尝试发送）。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--contests", help="contests.json path", default=None)
    parser.add_argument("--send", action="store_true", help="Actually send emails. If not provided runs dry-run")
    args = parser.parse_args()
    main(contests_json_path=args.contests, dry_run=not args.send)
