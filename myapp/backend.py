class LoginBackend:

    def authenticate(self, username=None, password=None, model=None):

        lookup_model = Users

        try:
            user = lookup_model.objects.get(username=username)
        except Exception, e:
            return None
    return user