from django.forms import EmailField, CharField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import ModelForm
from .models import Profile


class RegistrationForm(UserCreationForm):
    email = EmailField()
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
            ]


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = get_user_model()
        fields = "__all__"


class UpdateUserForm(ModelForm):
    email = EmailField()
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
