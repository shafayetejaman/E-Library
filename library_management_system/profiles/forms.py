from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class UserChangeFormClass(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ["username", "email"]
    
