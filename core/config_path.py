from pathlib import Path

BASE_PATH = Path().cwd()

ENV_PATH = BASE_PATH / '.env'

I18N_PATH = BASE_PATH / 'core' / 'i18n'

CONFIRM_EMAIL_HTML_PATH = BASE_PATH / 'templates' / 'confirm_email.html'
