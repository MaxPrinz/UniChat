# Local Settings, not synced via Git
# Usage: copy settings_local_template.py to settings_local.py and adjust parameters

# see https://learndjango.com/tutorials/django-password-reset-tutorial
# see https://docs.djangoproject.com/en/3.1/topics/email/#smtp-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mailServerOfMyISP"
EMAIL_TIMEOUT = 60
