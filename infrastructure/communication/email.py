from collections.abc import Sequence
from email.message import EmailMessage

import aiosmtplib

from application.dto.communication import Message
from application.interfaces.communication import IMessageSender


class SMTPEmailSender(IMessageSender):
    async def send_message(self, message: Message) -> None:
        async with aiosmtplib.SMTP() as smtp_client:
            email_message = EmailMessage()
            email_message['From'] = message.sender
            email_message['To'] = message.recipients
            email_message['Subject'] = message.subject

            await smtp_client.send_message(
                email_message,
                sender=message.sender,
                recipients=message.recipients,
            )

    async def send_messages(self, messages: Sequence[Message]) -> None:
        pass
