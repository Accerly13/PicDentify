from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import AdminUser

class AdminUserBackend(BaseBackend):
    def authenticate(self, request, username=None, user_key=None, password=None, **kwargs):
        try:
            admin_user = AdminUser.objects.get(user_key=user_key)
            if admin_user.check_password(password) or admin_user.password == password:
                # Create an instance of AdminUser to authenticate and log in
                user = admin_user
                return user
        except AdminUser.DoesNotExist:
            return None