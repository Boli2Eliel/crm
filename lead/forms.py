from django import forms
from .models import Lead, Comment, LeadFile


class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'firm',
            'first_name',
            'name',
            'email',
            'phone_number',
            'description',
            'priority',
            'status',
            'profile_picture',
        )
        widgets = {

            #'description': forms.TextInput(attrs={'class': 'bg-gray-200'}),

        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'bg-gray-200'}),
        }

class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile
        fields = ('file',)
