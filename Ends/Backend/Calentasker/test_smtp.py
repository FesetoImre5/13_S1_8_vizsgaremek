import os
import django
from django.conf import settings
from django.core.mail import send_mail

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Calentasker.settings')
django.setup()

print(f"Testing Email Configuration...")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

try:
    send_mail(
        'SMTP Test',
        'If you received this, your SMTP configuration is correct!',
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER], # Send to self
        fail_silently=False,
    )
    print("SUCCESS: Email sent successfully!")
except Exception as e:
    print(f"FAILURE: {e}")
