from django import forms

from goods.models import UserShoppingCart


class SortForm(forms.Form):
    SORT_CHOICES = (
        ('name', 'По названию'),
        ('created_at', 'По дате добавления'),
        ('purchase_count', 'По популярности'),
        ('price', 'По цене'),
    )
    DIRECTION_CHOICES = (
        ('asc', 'По возрастанию'),
        ('desc', 'По убыванию')
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label='Сортировать по',
    )
    sort_direction = forms.ChoiceField(
        choices=DIRECTION_CHOICES,
        required=False,
        label='Направление сортировки',
    )


class UserShoppingCartForm(forms.ModelForm):
    class Meta:
        model = UserShoppingCart
        fields = ['good', 'quantity']

    def __init__(self, *args, **kwargs):
        super(UserShoppingCartForm, self).__init__(*args, **kwargs)
        self.fields['good'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

    def clean_good(self):
        return self.instance.good.name


UserShoppingCartFormSet = forms.modelformset_factory(
    UserShoppingCart,
    form=UserShoppingCartForm,
    extra=0,
    can_delete=True,
    edit_only=True,
)
