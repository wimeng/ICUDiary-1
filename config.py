"""ICU Diary development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b"\xd3\xea\xf5#\xcf-\x0b\x85k\xc5'\xe8=i\xd90-s\t\xaal\x14Uz"
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
ICUDIARY_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = ICUDIARY_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/icudiary.sqlite3
DATABASE_FILENAME = ICUDIARY_ROOT/'var'/'icudiary.sqlite3'
