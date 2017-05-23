from django.contrib.auth.backends import ModelBackend
from django.forms.fields import email_re
from django.contrib.auth.models import Users

class EmailBackend(ModelBackend):
    """
    Authenticate against django.contrib.auth.models.User
    """

    def authenticate(self, **credentials):
        return 'username' in credentials and \ 
            self.authenticate_by_username_or_email(**credentials)

    def authenticate_by_username_or_email(self, username=None, password=None):
        try:
            user = Users.objects.get(email=username)
        except Users.DoesNotExist:
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                user = None
        if user:
            return user if user.check_password(password) else None
        else:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
