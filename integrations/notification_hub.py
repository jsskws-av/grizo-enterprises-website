"""
Notification Hub: Telegram Bot and SMTP Email Dispatcher
Delivers daily executive summaries, inventory replenishment alerts, and emergency stop notifications.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
import httpx

from config.settings import settings


class NotificationHub:
    def __init__(self):
        self.telegram_bot_token = settings.telegram_bot_token
        self.telegram_chat_id = settings.telegram_chat_id
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.recipient_email = settings.alert_recipient_email

    def send_telegram_alert(self, message: str) -> Dict[str, Any]:
        """Send urgent notification via Telegram Bot."""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return {"status": "SKIPPED", "reason": "Telegram credentials not configured"}

        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(url, json=payload)
                if res.status_code == 200:
                    return {"status": "SENT", "channel": "TELEGRAM"}
                return {"status": "FAILED", "channel": "TELEGRAM", "error": res.text}
        except Exception as e:
            return {"status": "ERROR", "channel": "TELEGRAM", "error": str(e)}

    def send_email_report(self, subject: str, html_body: str) -> Dict[str, Any]:
        """Send daily report or alert via SMTP."""
        if not self.smtp_host or not self.recipient_email:
            return {"status": "SKIPPED", "reason": "SMTP host or recipient not configured"}

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.smtp_user or "alerts@ecom-system.local"
            msg["To"] = self.recipient_email

            part = MIMEText(html_body, "html")
            msg.attach(part)

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15.0) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.sendmail(msg["From"], [self.recipient_email], msg.as_string())

            return {"status": "SENT", "channel": "EMAIL"}
        except Exception as e:
            return {"status": "ERROR", "channel": "EMAIL", "error": str(e)}

    def dispatch_alert(self, title: str, text: str):
        """Dispatch to all active notification channels."""
        tg_res = self.send_telegram_alert(f"🚨 *{title}*\n\n{text}")
        email_res = self.send_email_report(
            subject=f"[E-Com Alert] {title}",
            html_body=f"<h3>{title}</h3><p>{text.replace(chr(10), '<br>')}</p>"
        )
        return {"telegram": tg_res, "email": email_res}


notification_hub = NotificationHub()
