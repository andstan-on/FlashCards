from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget



User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['question', 'answer']
        widgets = {
            'answer': CKEditorUploadingWidget(),
        }




