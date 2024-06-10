from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       UserCreationForm, UsernameField)
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.template import loader

from core.tasks import async_send_mail


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


class PasswordResetFormWithAsyncEmail(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name,
                                                 context)
        else:
            html_email = None
        return async_send_mail.delay(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_email,
        )
