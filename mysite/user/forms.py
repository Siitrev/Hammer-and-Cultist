from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, Button



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
            Submit('submit', 'Register', css_class='btn btn-secondary mb-2'),
        )
    
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

    
class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    bio = forms.CharField(label="Bio", widget=forms.Textarea(attrs={"rows" : "20"}))
    avatar = forms.ImageField(label="Avatar", allow_empty_file=False, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('bio', css_class="resize-0"),
            Field('avatar'),
            Submit('submit', 'Update', css_class='btn btn-primary mb-2 d-inline'),
            Button('cancel', 'Cancel', css_id="cancel-btn", css_class='btn btn-danger mb-2 d-inline'),
        )