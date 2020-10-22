from django import forms
from django_countries.fields import CountryField
from mptt.forms import TreeNodeChoiceField
from .models import Comment

PAYMENT_CHOICES = (
    ('GP', 'GooglePay'),
    ('P', 'PayTm'),
    ('S', 'Stripe'),
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    home_address = forms.CharField(required=True)
    country= CountryField(blank_label='(Select Country)').formfield()
    zip=forms.IntegerField(max_value=1000000)
    save_billing_address=forms.BooleanField(widget=forms.CheckboxInput)
    save_info=forms.BooleanField(widget=forms.CheckboxInput)
    payment_option=forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=PAYMENT_CHOICES)


class CommentForm(TreeNodeChoiceField):
    parent=TreeNodeChoiceField(queryset=Comment.objects.all())

