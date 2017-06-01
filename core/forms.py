from django import forms

from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        label='First name',
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        label='Last name',
        required=False)
    job_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label='Job title',
        required=False)
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label='Email',
        required=False)
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label='Url',
        required=False)
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label='Location',
        required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'job_title', 'email',
                  'url', 'location', ]


class ChangePasswordForm(forms.ModelForm):

    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Old password',
        required=True)
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='New password',
        required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm new password',
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            raise forms.ValidationError('Old password don\'t match')
        if new_password and new_password != confirm_password:
            raise forms.ValidationError('New password don\'t match')


class ProfileImageForm(forms.Form):
    image = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Select a image')