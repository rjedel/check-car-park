from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AddCarParkForm(forms.Form):
    spot_name = forms.CharField(label='Miejscowość', min_length=2, max_length=100, required=False)
    street = forms.CharField(label='Ulica', min_length=2, max_length=100, required=False)
    street.widget.attrs.update(placeholder='pole nie jest wymagane')
    street_number = forms.IntegerField(label='Numer', widget=forms.TextInput, required=False)
    name = forms.CharField(label='Nazwa parkingu', min_length=2, max_length=100)
    description = forms.CharField(label='Opis', required=False,
                                  widget=forms.Textarea(attrs={'cols': 21, 'placeholder': 'pole nie jest wymagane'}))
    longitude = forms.CharField(widget=forms.HiddenInput())
    latitude = forms.CharField(widget=forms.HiddenInput())
    free_of_charge = forms.BooleanField(label='Czy parking jest bezpłatny', required=False)
    tariffs_name = forms.CharField(label='Nazwa taryfy', required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'pole nie jest wymagane'}))
    first_hour_fee = forms.DecimalField(label='Opłata za pierwszą godzinę postoju', max_digits=5, decimal_places=2,
                                        min_value=0, required=False)
    maximum_additional_fee = forms.DecimalField(label='Maksymalna opłata dodatkowa', max_digits=5, decimal_places=2,
                                                min_value=0, required=False)
    additional_fee_description = forms.CharField(label='Opis maksymalnej dopłaty', required=False,
                                                 widget=forms.Textarea(attrs={'cols': 21}))

    def clean(self):
        cleaned_data = super().clean()
        free_of_charge = cleaned_data.get('free_of_charge')
        first_hour_fee = cleaned_data.get('first_hour_fee')
        maximum_additional_fee = cleaned_data.get('maximum_additional_fee')
        additional_fee_description = cleaned_data.get('additional_fee_description')
        longitude = cleaned_data.get('longitude')
        latitude = cleaned_data.get('latitude')
        if free_of_charge and (first_hour_fee or maximum_additional_fee or additional_fee_description):
            raise forms.ValidationError(
                'Nie zaznaczaj pola "Czy jest bezpłatny" '
                'razem z wypełnionym polem dotyczącym opłat'
            )
        if not free_of_charge and not any([first_hour_fee, maximum_additional_fee, additional_fee_description]):
            raise forms.ValidationError(
                'Proszę wypełnij przynajmniej jedno z czterech pól dotyczących opłaty'
            )
        if not longitude or not latitude:
            raise forms.ValidationError('Nie można dodać parkingu bez jego lokalizacji')
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Nazwa użytkownika')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email",)
