"""邮件发送：console 模式打印到日志（开发），smtp 模式真实发信（生产）"""
import logging

from app.core.config import (
    MAIL_MODE,
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USER,
)

logger = logging.getLogger("adoruworld.mailer")


async def send_verification_email(to_email: str, code: str) -> None:
    subject = "AdoruWorld 注册验证码"
    body = (
        f"你的注册验证码是：{code}\n\n"
        f"10 分钟内有效。如果不是你本人操作，请忽略这封邮件。"
    )

    if MAIL_MODE == "smtp":
        await _send_via_smtp(to_email, subject, body)
    else:
        # 开发模式：验证码直接进后端日志，不依赖任何邮箱配置
        logger.warning("📧 [console 模式] 验证码邮件 → %s | 验证码: %s", to_email, code)


async def _send_via_smtp(to_email: str, subject: str, body: str) -> None:
    from aiosmtplib import SMTP

    message = (
        f"From: {SMTP_FROM}\r\n"
        f"To: {to_email}\r\n"
        f"Subject: {subject}\r\n"
        f"Content-Type: text/plain; charset=utf-8\r\n\r\n"
        f"{body}"
    )
    async with SMTP(hostname=SMTP_HOST, port=SMTP_PORT, use_tls=True) as smtp:
        await smtp.login(SMTP_USER, SMTP_PASSWORD)
        await smtp.sendmail(SMTP_FROM, [to_email], message)
    logger.info("📧 验证码邮件已发送至 %s", to_email)
