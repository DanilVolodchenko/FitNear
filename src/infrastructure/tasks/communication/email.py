from collections.abc import Sequence

from dishka.integrations.taskiq import FromDishka, inject

from src.infrastructure.communication.email import SMTPEmailSender
from src.infrastructure.resources.taskiq import redis_broker


@redis_broker.task
@inject(patch_module=True)
async def send_email_task(
    subject: str,
    sender: str,
    recipient: Sequence[str] | str,
    content: str,
    email_sender: FromDishka[SMTPEmailSender],
) -> None:
    await email_sender.send_text(subject, sender, recipient, content)
