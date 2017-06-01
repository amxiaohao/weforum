from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.conf import settings


def signup_domain_validator(value):
    if '*' not in settings.ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index('@'):]
            if domain not in settings.ALLOWED_SIGNUP_DOMAINS:
                domain = value[value.index('@'):]
                raise ValidationError(
                    'Invalid dimain. Allowed domain on this forum: {0}'. \
                    format(','.join(settings.ALLOWED_SIGNUP_DOMAINS))
                )

        except Exception:
            raise ValidationError(
                'Invalid dimain. Allowed domain on this forum: {0}'. \
                format(','.join(settings.ALLOWED_SIGNUP_DOMAINS))
            )


def forbidden_username_validator(value):
    forbidden_usernames = ['admin', 'setting', 'settings', 'about', 'help',
                           'signin', 'signup', 'signout', 'login', 'registration',
                           'logout', 'administrator', 'accout', 'username',
                           'root', 'root', 'blog', 'blogs', 'user', 'users', 
                           'edit', 'mail', 'email', 'home', 'index', 'profile', 
                           'auth', 'authentication', 'config', 'delete', 'remove', 
                           'forum', 'forum', 'log', 'search', 'rss', 'support',
                           'status', 'static', 'media', 'html', 'css', 'js',
                           'article', 'articles']

    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a reserved word.')


def invalid_username_validator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')


def unique_email_validator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('Email has already exists.')


def unique_username_ignore_case_validator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('Username has already exists.')


class SignUpForm(forms.ModelForm):
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        label = 'Username',
        help_text='Usernames may contain alphanumeric, _ and . characters.')
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=True,
        label='Email')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        label='Password')
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        label='Confirm your password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(forbidden_username_validator)
        self.fields['username'].validators.append(invalid_username_validator)
        self.fields['username'].validators.append(
                unique_username_ignore_case_validator)
        self.fields['email'].validators.append(unique_email_validator)
        self.fields['email'].validators.append(signup_domain_validator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            raise forms.ValidationError('Password don\'t match.')
        return self.cleaned_data