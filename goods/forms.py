from django import forms


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
