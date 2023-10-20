from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['contact', 'address']
        widgets = {
            'contact': forms.TextInput(attrs={
                'placeholder': 'Номер телефона, telegram'}),
            'address': forms.Textarea(
                attrs={'placeholder': 'Адрес'}),
        }
