from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required. Add a valid email address.")

    class Meta:
        model   = Account
        fields  = ("email", "username", "password1", "password2")

    def clean_email(self):
        """
        This method will get the email and check either its exist or not.
        if already exist, return error.
        if not return the email.
        """
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return email  
        raise forms.ValidationError(f"Email {email} is already in use.")  

    def clean_username(self):
        """
        This method will get the username and check either its exist or not.
        if already exist, return error.
        if not return the username.
        """
        username = self.cleaned_data['username'].lower()
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return username  
        raise forms.ValidationError(f"Username {username} is already in use.") 

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        required=True
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        required=True
    )


    
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('profile_image', 'email', 'username', 'hide_email')

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        # Exclude the current user while checking for duplicates
        if Account.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"Email {email} is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        # Exclude the current user while checking for duplicates
        if Account.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"Username {username} is already in use.")
        return username

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)

        account.username        = self.cleaned_data['username']
        account.email           = self.cleaned_data['email']
        account.profile_image   = self.cleaned_data['profile_image']
        account.hide_email      = self.cleaned_data['hide_email']

        if commit:
            account.save()
        return account

