from django.contrib.auth import models as auth_models


class ModelBackend(auth_models.ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = auth_models.User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except ValueError:
            pass
        except auth_models.User.DoesNotExist:
            pass
