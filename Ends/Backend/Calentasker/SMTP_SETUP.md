# Setting Up Real Emails (SMTP)

Currently, the project is configured to print emails to the **console** for development debugging. To send **real emails**, you need to update `settings.py` with SMTP credentials.

## 1. Environment Variables
**NEVER** commit your passwords to code. Use environment variables.

Create a `.env` file in your backend root (where `manage.py` is):
```ini
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## 2. Update settings.py
Replace the existing `EMAIL_BACKEND` configuration with this:

```python
import os

# Remove this line:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Add this block:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

## 3. Gmail Specifics (App Passwords)
If you use Gmail:
1.  Go to your Google Account > Security.
2.  Enable **2-Step Verification**.
3.  Go to **App Passwords** (search for it).
4.  Create a new app password (name it "Django" or "Calentasker").
5.  Use that 16-character password in your `.env` file.
