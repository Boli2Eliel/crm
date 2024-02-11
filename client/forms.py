from django import forms
from .models import Client, Comment, ClientFile


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'firm',
            'first_name',
            'name',
            'email',
            'phone_number',
            'description',
            'profile_picture',
        )
        widgets = {

            'description': forms.Textarea(attrs={'class': 'bg-gray-200'}),
        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-group'}),
        }
class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',)
