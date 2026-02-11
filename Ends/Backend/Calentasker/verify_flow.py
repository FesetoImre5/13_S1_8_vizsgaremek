import os
import django

# Setup Django standalone BEFORE other imports that might use settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Calentasker.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

def test_registration_flow():
    client = APIClient()
    
    # 1. Register a new user
    print("1. Registering new user 'flow_test_user'...")
    register_data = {
        'username': 'flow_test_user',
        'email': 'flow@test.com',
        'password': 'password123',
        'first_name': 'Flow',
        'last_name': 'Test'
    }
    
    # Clean up if exists
    User.objects.filter(username='flow_test_user').delete()
    
    response = client.post('/api/users/', register_data)
    
    if response.status_code != status.HTTP_201_CREATED:
        print(f"FAILED: Registration failed. {response.data}")
        return

    user = User.objects.get(username='flow_test_user')
    print("   User created.")

    # 2. Check is_active
    print(f"2. Checking is_active status... (Expected: False, Actual: {user.is_active})")
    if user.is_active:
        print("FAILED: User should be inactive after registration!")
        return
    else:
        print("   SUCCESS: User is inactive.")

    # 3. Try to login (Should fail)
    print("3. Attempting login before verification...")
    # Using the standard auth endpoint if exists, or just checking authentication
    # Assuming /api-token-auth/ or similar, but let's check standard django login behavior via client.login
    # Actually, let's try to get a token if using DRF TokenAuth
    
    # If using rest_framework.authtoken
    from rest_framework.authtoken.models import Token
    # Usually obtaining a token requires a view. Let's try to authenticate using a standard view request
    
    # We can use force_authenticate to test permissions, but here we want to test IF they can login.
    # Let's try to obtain an auth token via the standard DRF connect if configured, 
    # OR simpler: check if `authenticate` returns None.
    from django.contrib.auth import authenticate
    auth_user = authenticate(username='flow_test_user', password='password123')
    
    if auth_user is not None:
        # Django's default ModelBackend prevents inactive users from authenticating? 
        # Actually ModelBackend verify that user.is_active is True? 
        # Yes, standard ModelBackend rejects inactive users if 'reject_inactive_user' is True (default).
        # Let's verify specifically.
        print("FAILED: authenticate() returned a user. Inactive users should not be able to authenticate.")
        return
    else:
        print("   SUCCESS: Valid credentials but inactive user -> Login failed (as expected).")

    # 4. Activate User
    print("4. Activating user...")
    # Generate valid token (simulating clicking the link)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    activate_data = {
        'uid': uid,
        'token': token
    }
    
    response = client.post('/api/users/activate/', activate_data)
    
    if response.status_code == status.HTTP_200_OK:
        print("   Activation successful.")
        user.refresh_from_db()
        print(f"   User is_active: {user.is_active}")
        if not user.is_active:
             print("FAILED: User is still inactive after activation!")
             return
    else:
        print(f"FAILED: Activation endpoint returned {response.status_code}: {response.data}")
        return

    # 5. Try to login again (Should succeed)
    print("5. Attempting login after verification...")
    auth_user = authenticate(username='flow_test_user', password='password123')
    
    if auth_user is not None:
        print("   SUCCESS: Login successful.")
    else:
        print("FAILED: Login failed even after activation.")

    print("\n--- TEST COMPLETED SUCCESSFULLY ---")

if __name__ == '__main__':
    test_registration_flow()
