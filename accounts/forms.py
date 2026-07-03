from django import forms
from .models import User

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['nom', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        user.role = 'utilisateur'
        user.statut = 'en attente'

        if commit:
            user.save()

        return user