from collections.abc import Sequence
from email.message import EmailMessage
from typing import Any

import aiosmtplib

from config import SMTPConfig
from src.core.interfaces.communication import IEmailSender


class SMTPEmailSender(IEmailSender):
    def __init__(self, smtp_config: SMTPConfig) -> None:
        self._smtp_config = smtp_config

    async def send_text(
        self,
        subject: str,
        sender: str,
        recipients: str | Sequence[str],
        content: str,
        **kwargs: Any,
    ) -> None:
        async with aiosmtplib.SMTP(hostname=self._smtp_config.host, port=self._smtp_config.port) as smtp_client:
            email_message = EmailMessage()
            email_message['Subject'] = subject
            email_message['From'] = sender
            email_message['To'] = recipients
            email_message.set_content(content)

            await smtp_client.send_message(
                email_message,
                sender=sender,
                recipients=recipients,
            )
