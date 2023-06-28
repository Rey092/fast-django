# -*- coding: utf-8 -*-
"""Authentication entities."""

PASSWORD_CHECKS = [
    {
        "message": "Password must be from 8 to 30 characters long.",
        "regex": r"^(?=.{8,30})",
    },
    {
        "message": "At least one lowercase and uppercase characters.",
        "regex": r"(?=.*[a-z])(?=.*[A-Z])",
    },
    {
        "message": "At least one number.",
        "regex": r"(?=.*[0-9])",
    },
]
