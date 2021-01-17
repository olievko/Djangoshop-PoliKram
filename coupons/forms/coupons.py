from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            "class": "w3-input w3-border",
            "placeholder": "Введіть код",
        }),
        )
