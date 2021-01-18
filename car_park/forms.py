from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AddCarParkForm(forms.Form):
    name = forms.CharField(label='Nazwa', min_length=2, max_length=100)
    description = forms.CharField(label='Opis', min_length=2, required=False,
                                  widget=forms.Textarea(attrs={'cols': 21, 'placeholder': 'pole nie jest wymagane'}))
    spot_name = forms.CharField(label='Miejscowość', min_length=2, max_length=100)
    street = forms.CharField(label='Ulica', min_length=2, max_length=100, required=False)
    street.widget.attrs.update(placeholder='pole nie jest wymagane')
    street_number = forms.IntegerField(label='Numer', min_value=0)
    free_of_charge = forms.BooleanField(label='Czy jest bezpłatny')
    first_hour_fee = forms.DecimalField(label='Opłata za pierwszą godzinę postoju', max_digits=5, decimal_places=2,
                                        min_value=0, required=False)
    maximum_additional_fee = forms.DecimalField(label='Maksymalna opłata dodatkowa', max_digits=5, decimal_places=2,
                                                min_value=0, required=False)
    additional_fee_description = forms.CharField(label='Opis maksymalnej dopłaty', min_length=2, required=False,
                                                 widget=forms.Textarea)


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Nazwa użytkownika')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email",)
