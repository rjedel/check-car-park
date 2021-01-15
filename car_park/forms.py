from django import forms


class AddCarParkForm(forms.Form):
    name = forms.CharField(label='Nazwa', min_length=2, max_length=100)
    description = forms.CharField(label='Opis', min_length=2, required=False, widget=forms.Textarea(attrs={'cols': 21}))
    city = forms.CharField(label='Miasto', min_length=2, max_length=100)
    street = forms.CharField(label='Ulica', min_length=2, max_length=100)
    street_number = forms.IntegerField(label='Numer', min_value=0)
    free_of_charge = forms.BooleanField(label='Czy jest bezpłatny')
    first_hour_fee = forms.DecimalField(label='Opłata za pierwszą godzinę postoju', max_digits=5, decimal_places=2, min_value=0, required=False)
    maximum_additional_fee = forms.DecimalField(label='Maksymalna opłata dodatkowa', max_digits=5, decimal_places=2, min_value=0, required=False)
    additional_fee_description = forms.CharField(label='Opis maksymalnej dopłaty', min_length=2, required=False, widget=forms.Textarea)
