from django import forms
from payment.models import CancelOrder

class CancelOrderForm(forms.ModelForm):
    class Meta:
        model = CancelOrder
        fields = ['reasion']