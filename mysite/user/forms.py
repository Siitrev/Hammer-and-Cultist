from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'username',
                'email',
                'password1',
                'password2'
            ),
            Submit('submit', 'Register', css_class='button white'),
        )
        self.helper["username"].update_attributes(css_class="dupa")
    
    class Meta:
        model = User
        fields = ("username","email","password1","password2")
    
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise ValidationError("Email is already taken!")
        return data
    
    def save(self, commit=True):
        user = super(NewUserForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    