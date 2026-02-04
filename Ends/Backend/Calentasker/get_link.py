import os
import django
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Calentasker.settings')
django.setup()

User = get_user_model()

# Get the latest user
try:
    user = User.objects.last()
    if not user:
        with open('link.txt', 'w') as f:
            f.write("No users found.")
    else:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f"http://localhost:5173/verify-email/{uid}/{token}"
        
        with open('link.txt', 'w') as f:
            f.write(f"User: {user.username}\nLink: {verification_url}")
except Exception as e:
    with open('link.txt', 'w') as f:
        f.write(f"Error: {e}")
