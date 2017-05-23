from django.conf import settings
from django.contrib.auth.models import check_password
from accounts.models import User

class UsernameAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self, username=None, password=None):
        """
        Authentication method
        """
        try:
            user = User.objects.get(eusername=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            user = Users.objects.get(pk=username))
            if user.is_active:
                return user
            return None
        except Users.DoesNotExist:
            return None