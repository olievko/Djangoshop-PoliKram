from django import forms
from ecomapp.models.shop import ProductReview


class ProductReviewForm(forms.ModelForm):
    """ Form class to submit a new ProductReview instance """

    class Meta:
        model = ProductReview
        fields = ('subject', 'content', 'rating')