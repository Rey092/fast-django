# -*- coding: utf-8 -*-
"""Telegram logger."""
import aiogram
import aiogram.utils.markdown as fmt
from django.conf import settings


async def log_to_telegram(msg):
    """Log to telegram."""
    await aiogram.Bot(settings.TELEGRAM_BOT_TOKEN).send_message(
        settings.TELEGRAM_CHAT_ID,
        text=fmt.text(
            fmt.hbold("Похоже, что что-то пошло не так!"),
            fmt.text("- - - - -"),
            fmt.hcode(f"{msg[-500:]}"),
            sep="\n",
        ),
        parse_mode="HTML",
    )
