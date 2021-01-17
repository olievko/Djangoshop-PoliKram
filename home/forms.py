from django import forms
from django.forms import ModelForm
from django.forms import Textarea, TextInput
from django.utils.translation import ugettext_lazy as _
from home.models import ContactMessage


class ContactForm(ModelForm):

    cc_myself = forms.BooleanField(
                label='Отримати копію',
                widget=forms.CheckboxInput(attrs={"class": ""}), required=False)

    class Meta:
        model = ContactMessage
        fields = ['contact_name', 'email', 'subject', 'comment']
        labels = {
            'contact_name': '',
            'email': '',
            'subject': '',
            'comment': '',
        }
        widgets = {
            'contact_name': TextInput(attrs={'class': 'w3-input w3-border', 'placeholder': _("Ім'я та Прізвище")}),
            'subject': TextInput(attrs={'class': 'w3-input w3-border', 'placeholder': _('Тема повідомлення')}),
            'email': TextInput(attrs={'class': 'w3-input w3-border', 'placeholder': _('Ваша електронна пошта')}),
            'comment': Textarea(attrs={'class': 'w3-input w3-border', 'placeholder': _('Повідомлення')}),
        }
