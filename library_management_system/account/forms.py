from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)


        if commit:
            user.save()
            current_date = datetime.now()
            account_no = current_date.strftime("%Y%m%d")+str(user.id)
            UserAccount.objects.create(user=user, account_no=int(account_no))

        return user
