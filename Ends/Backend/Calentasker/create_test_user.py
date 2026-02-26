import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Calentasker.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

try:
    user = User.objects.filter(email='user@test.com').first()
    if not user:
        user = User.objects.create_user(username='testuser1234', email='user@test.com', password='password123', first_name='Test', last_name='User')
        print(f"User {user.username} created.")
    else:
        user.username = 'testuser1234'
        user.set_password('password123')
        user.save()
        print("User already exists, password and username reset.")
except Exception as e:
    import traceback
    traceback.print_exc()
