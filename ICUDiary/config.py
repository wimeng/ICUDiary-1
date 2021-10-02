"""Insta485 development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\xf5\xca\x90\x16\xea\x8f\xf9r\x0f\x850\xb7\x9a \
                \x1c\xe8q\xe2Y\xf0n\x14O@\xf8'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
ICUDIARY_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = ICUDIARY_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = ICUDIARY_ROOT/'var'/'ICUDiary.sqlite3'