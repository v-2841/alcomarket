from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class EmailAndUsernameAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="Email или имя пользователя",
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    error_messages = {
        "invalid_login":
            "Пожалуйста, введите правильные имя пользователя и пароль.",
        "inactive":
            "Ваша учетная запись неактивна. Свяжитесь с администратором.",
    }

    def clean_username(self):
        username = self.data['username']
        is_email = '@' in username
        query = {'email__iexact' if is_email else 'username__iexact': username}
        try:
            user = User.objects.get(**query)
            self.confirm_login_allowed(user)
        except ObjectDoesNotExist:
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )
        return user.username
