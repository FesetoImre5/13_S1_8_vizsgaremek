import os
import django
from django.conf import settings
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Calentasker.settings')
django.setup()

print("Current EMAIL_BACKEND:", settings.EMAIL_BACKEND)
print("Sending test email...")

try:
    send_mail(
        'Test Subject',
        'Test Message',
        'webmaster@localhost',
        ['test@example.com'],
        fail_silently=False,
    )
    print("Email sent successfully (check console output above if using ConsoleBackend).")
except Exception as e:
    print(f"Error sending email: {e}")
